import json
import os
import re
from typing import Dict, Any
from .tokenizer import tokenize

# Load and invert regional dictionaries for word-by-word translation
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _invert_dict(raw_dict: Dict[str, Any]) -> Dict[str, str]:
    inverted = {}
    for region_word, data in raw_dict.items():
        if isinstance(data, dict) and 'arti' in data:
            # Clean the region_word to remove numbers and parenthetical notes
            cleaned_rw = re.sub(r'\(.*?\)', '', region_word)
            cleaned_rw = re.sub(r'\d+', '', cleaned_rw)
            cleaned_rw = cleaned_rw.strip(' -:').strip()
            # If completely empty after cleaning, use the original without spaces
            if not cleaned_rw:
                cleaned_rw = region_word.strip()
                
            meanings_str = data['arti']
            # Split multiple meanings
            meanings = re.split(r'[,;\/]', meanings_str)
            for m in meanings:
                m = m.strip().lower()
                # Often dictionaries have formats like "bahasa - mengindonesia" or "kata ganti"
                # This simple heuristic strips explanations if separated by hyphen
                if " - " in m:
                    m = m.split(" - ")[-1].strip()
                
                # Take only single words or short phrases
                if m and m not in inverted:
                    inverted[m] = cleaned_rw
    return inverted

def _load_and_invert(filename: str) -> Dict[str, str]:
    try:
        with open(os.path.join(BASE_DIR, 'dict', filename), 'r', encoding='utf-8') as f:
            raw = json.load(f)
            # Remove metadata block if present (e.g. _meta in batak_dict)
            if '_meta' in raw:
                del raw['_meta']
            return _invert_dict(raw)
    except Exception:
        return {}

# Preload the inverse dictionaries
_INDO_TO_SUNDA = _load_and_invert('sunda_dict.json')
_INDO_TO_JAWA = _load_and_invert('jawa_dict.json')
_INDO_TO_BALI = _load_and_invert('bali_dict.json')
_INDO_TO_MINANG = _load_and_invert('minang_dict.json')
_INDO_TO_BATAK = _load_and_invert('batak_dict.json')

_LANG_MAP = {
    'sunda': _INDO_TO_SUNDA,
    'jawa': _INDO_TO_JAWA,
    'bali': _INDO_TO_BALI,
    'minang': _INDO_TO_MINANG,
    'batak': _INDO_TO_BATAK
}

def dict_translate(text: str, target_lang: str) -> str:
    """
    Menerjemahkan teks Bahasa Indonesia secara harfiah (word-by-word) ke bahasa daerah.
    Berdasarkan data dictionary (kamus) lokal yang tersedia di package.
    Bahasa yang didukung: sunda, jawa, bali, minang, batak
    """
    target_lang = target_lang.lower().strip()
    if target_lang not in _LANG_MAP:
        return text 
        
    lang_dict = _LANG_MAP[target_lang]
    if not lang_dict:
        return text 

    # Split to tokens to preserve punctuations and structure
    tokens = tokenize(text)
    translated_pieces = []
    
    for t in tokens:
        if re.match(r'^[A-Za-z\-]+$', t):
            lower_t = t.lower()
            repl = None
            if lower_t in lang_dict:
                repl = lang_dict[lower_t]
            else:
                # Basic Affix fallback
                prefixes = ['meng', 'meny', 'mem', 'men', 'me', 'peng', 'peny', 'pem', 'pen', 'pe', 'ber', 'ter', 'di', 'ke', 'se']
                suffixes = ['kannya', 'annya', 'nya', 'kan', 'an', 'lah', 'kah', 'pun', 'ku', 'mu']
                
                # Check suffix
                for suf in suffixes:
                    if lower_t.endswith(suf) and len(lower_t) > len(suf) + 2:
                        root = lower_t[:-len(suf)]
                        if root in lang_dict:
                            # Try to localize suffix if possible
                            if suf == 'nya' and target_lang == 'sunda': suf = 'na'
                            elif suf == 'nya' and target_lang in ['jawa', 'bali']: suf = 'ne'
                            elif suf == 'nya' and target_lang == 'minang': suf = 'nyo'
                            elif suf == 'nya' and target_lang == 'batak': suf = 'na'
                            
                            if suf == 'ku' and target_lang == 'batak': suf = 'hu'
                            elif suf == 'mu' and target_lang == 'batak': suf = 'mi'
                            
                            repl = lang_dict[root] + suf
                            break
                            
                # Check prefix
                if not repl:
                    for pre in prefixes:
                        if lower_t.startswith(pre) and len(lower_t) > len(pre) + 2:
                            root = lower_t[len(pre):]
                            if root in lang_dict:
                                repl = pre + lang_dict[root]
                                break
                                
                # Check prefix + suffix
                if not repl:
                    for pre in prefixes:
                        for suf in suffixes:
                            if lower_t.startswith(pre) and lower_t.endswith(suf) and len(lower_t) > len(pre) + len(suf) + 2:
                                root = lower_t[len(pre):-len(suf)]
                                if root in lang_dict:
                                    # Localize suffix
                                    if suf == 'nya' and target_lang == 'sunda': suf = 'na'
                                    elif suf == 'nya' and target_lang in ['jawa', 'bali']: suf = 'ne'
                                    elif suf == 'nya' and target_lang == 'minang': suf = 'nyo'
                                    elif suf == 'nya' and target_lang == 'batak': suf = 'na'
                                    
                                    repl = pre + lang_dict[root] + suf
                                    break
                        if repl:
                            break

            if repl:
                # Match casing
                if t.isupper():
                    repl = repl.upper()
                elif t.istitle():
                    repl = repl.title()
                translated_pieces.append(repl)
            else:
                translated_pieces.append(t)
        else:
            translated_pieces.append(t)
            
    # Simple detokenization (handling spaces for punctuation)
    res = ""
    for i, token in enumerate(translated_pieces):
        if re.match(r'^[.,!?;:]$', token) or token.startswith('\''):
            res += token
        else:
            if i > 0 and res and not res.endswith(' '):
                res += ' ' + token
            else:
                res += token
                
    return res.strip()
