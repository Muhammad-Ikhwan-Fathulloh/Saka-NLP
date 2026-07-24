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
                    inverted[m] = region_word
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
            if lower_t in lang_dict:
                repl = lang_dict[lower_t]
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
