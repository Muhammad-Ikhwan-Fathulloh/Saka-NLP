import asyncio
from typing import Dict, Any, List
import json
import os

# Load regional dictionaries
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    with open(os.path.join(BASE_DIR, 'dict', 'sunda_dict.json'), 'r', encoding='utf-8') as f:
        _SUNDA_DICT = json.load(f)
except Exception:
    _SUNDA_DICT = {}

try:
    with open(os.path.join(BASE_DIR, 'dict', 'jawa_dict.json'), 'r', encoding='utf-8') as f:
        _JAWA_DICT = json.load(f)
except Exception:
    _JAWA_DICT = {}

try:
    with open(os.path.join(BASE_DIR, 'dict', 'bali_dict.json'), 'r', encoding='utf-8') as f:
        _BALI_DICT = json.load(f)
except Exception:
    _BALI_DICT = {}

def check_dict(w: str) -> List[str]:
    langs = []
    if w in _SUNDA_DICT:
        langs.append('sunda')
    if w in _JAWA_DICT:
        langs.append('jawa')
    if w in _BALI_DICT:
        langs.append('bali')
    return langs

def analyze(word: str) -> Dict[str, Any]:
    """
    Analyzes the morphology of an Indonesian word using a hybrid approach.
    Uses regional dictionaries for validation and early stopping, and falls back
    to a greedy heuristic stemmer for unknown limits.
    """
    word = word.lower()
    original_word = word
    
    prefixes = []
    suffixes = []
    regional_matches = check_dict(word)
    
    # If the base word is already valid, no need to stem!
    if regional_matches:
        return {
            'root': word, 'prefixes': [], 'suffixes': [],
            'type': 'regional', 'regional_matches': regional_matches
        }

    # 1. Particles and Pronouns
    for p in ['kah', 'lah', 'pun']:
        if word.endswith(p) and len(word) >= len(p) + 3:
            suffixes.insert(0, p)
            word = word[:-len(p)]
            break
            
    for p in ['ku', 'mu', 'nya']:
        if word.endswith(p) and len(word) >= len(p) + 3:
            suffixes.insert(0, p)
            word = word[:-len(p)]
            break

    # 2. Derivational Suffixes
    # We attempt derivation, check dictionary.
    valid_suffixes = ['kan', 'an', 'i', 'keun', 'eun', 'na', 'aken', 'ake', 'ana', 'en', 'ne', 'e']
    valid_suffixes.sort(key=len, reverse=True)

    for p in valid_suffixes:
        if word.endswith(p) and len(word) >= len(p) + 3:
            suffixes.insert(0, p)
            word = word[:-len(p)]
            regional_matches = check_dict(word)
            break

    if regional_matches:
        return {
            'root': word, 'prefixes': prefixes, 'suffixes': suffixes,
            'type': 'regional', 'regional_matches': regional_matches
        }

    # 3. Prefix stripping with morphophonemic rules validation
    indo_prefix_rules = [
        ('meny', 's'), ('peny', 's'),
        ('meng', 'k'), ('peng', 'k'), ('meng', ''), ('peng', ''),
        ('mem', 'p'), ('pem', 'p'), ('mem', ''), ('pem', ''),
        ('men', 't'), ('pen', 't'), ('men', ''), ('pen', ''),
        ('ber', ''), ('bel', ''), ('per', ''), ('ter', ''), ('me', ''), ('pe', ''), ('di', ''), ('ke', ''), ('se', ''), ('be', '')
    ]
    regional_prefix_rules = [
        ('dipika', ''), ('pika', ''), ('barang', ''), ('silih', ''), ('mipa', ''), ('nga', ''), 
        ('dak', ''), ('kok', ''), ('tak', ''), ('mbok', ''), ('sa', ''), ('pa', ''), ('pi', ''), ('ka', ''), ('ti', ''), ('ba', '')
    ]
    all_prefix_rules = indo_prefix_rules + regional_prefix_rules

    # Pre-sort fallback prefixes by length descending (only Indonesian for purely blind stripping)
    fallback_prefixes = list(dict.fromkeys([p for p, _ in indo_prefix_rules]))
    fallback_prefixes.sort(key=len, reverse=True)

    for _ in range(2):
        stripped = False
        
        # Phase A: Try stripping and check if it yields a valid dictionary root
        for p, replacement in all_prefix_rules:
            if word.startswith(p) and len(word) >= len(p) + 3:
                candidate = replacement + word[len(p):]
                m = check_dict(candidate)
                if m:
                    word = candidate
                    prefixes.append(p)
                    regional_matches = m
                    stripped = True
                    break
                    
        # Phase B: Greedily strip without phonemic reconstruction (Indonesian V1 fallback)
        if not stripped and not regional_matches:
            for p in fallback_prefixes:
                if word.startswith(p) and len(word) >= len(p) + 3:
                    word = word[len(p):]
                    prefixes.append(p)
                    stripped = True
                    break

        if regional_matches or not stripped:
            break

    # 4. Handle Compound Words (Kata Majemuk Serangkai)
    # Check if the fallback root needs to be split
    compound_prefixes = {
        "tidak": "tidak ", "tanggung": "tanggung ", "garis": "garis ", 
        "hancur": "hancur ", "lipat": "lipat ", "sebar": "sebar ", 
        "ebar": "sebar ", "tanda": "tanda ", "anda": "tanda ", 
        "beri": "beri ", "ikut": "ikut ", "campur": "campur ", "ampur": "campur ",
        "salah": "salah ", "alah": "salah ", "alih": "alih ", 
        "uji": "uji ", "anak": "anak ", "kerja": "kerja ", 
        "tata": "tata ", "mata": "mata ", "jual": "jual ", 
        "beli": "beli ", "guna": "guna ", "daya": "daya ", 
        "budi": "budi ", "temu": "temu ", "ambil": "ambil ", "pindah": "pindah "
    }
    
    if not regional_matches:
        for cp, replacement in compound_prefixes.items():
            if word.startswith(cp) and len(word) >= len(cp) + 3:
                if cp == "sebar" and word == "sebarang":
                    continue
                word = f"{replacement}{word[len(cp):]}"
                break

    # Re-check in case the compound resolution formed a known word 
    # (Though highly unlikely for regional, good standard practice)
    if not regional_matches:
        regional_matches = check_dict(word)

    word_type = 'regional' if regional_matches else 'unknown'

    return {
        'root': word,
        'prefixes': prefixes,
        'suffixes': suffixes,
        'type': word_type,
        'regional_matches': regional_matches
    }

async def async_analyze(word: str) -> Dict[str, Any]:
    """
    Asynchronous morphological analysis.
    """
    await asyncio.sleep(0.001)
    return analyze(word)
