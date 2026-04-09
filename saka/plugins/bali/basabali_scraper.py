import os
import json
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List

class BasaBaliException(Exception):
    pass

_DICT_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'dict', 'bali_dict.json')
_BALI_DICT = {}
if os.path.exists(_DICT_PATH):
    with open(_DICT_PATH, 'r', encoding='utf-8') as f:
        _BALI_DICT = json.load(f)

def query_basabali(word: str, use_online: bool = True) -> Dict[str, Any]:
    """
    Queries the Balinese dictionary. Primary uses the offline bali_dict dataset.
    Optionally attempts to scrape dictionary.basabali.org if the word is not found locally.
    """
    word_lower = word.lower().capitalize() # BASAbali often uses Capitalized titles
    word_key = word.lower()
    
    # Check Offline First
    if word_key in _BALI_DICT:
        entry = _BALI_DICT[word_key]
        return {
            "query": word,
            "status": "found",
            "source": "offline_bali_database",
            "definitions": [entry]
        }
    
    if not use_online:
        return {
            "query": word,
            "status": "not_found",
            "source": "offline_bali_database"
        }

    # Attempt Online (BASAbali Wiki)
    url = f"https://dictionary.basabali.org/{word_lower}"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        # If not found with capitalized, try exact lower
        if response.status_code == 404:
            url = f"https://dictionary.basabali.org/{word.lower()}"
            response = requests.get(url, headers=headers, timeout=10)
            
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('div', {'id': 'mw-content-text'})
        
        if not content:
            return {
                "query": word,
                "status": "not_found",
                "source": "https://dictionary.basabali.org"
            }
            
        # BASAbali Wiki structure: Definitions are often in tables or specific paragraphs
        # We'll extract text from paragraphs and list items as a fallback for general definitions
        definitions = []
        
        # Look for English and Indonesian definitions
        # Often they are in a table with classes or identified by labels
        for p in content.find_all(['p', 'li']):
            text = p.get_text().strip()
            if text and len(text) > 5:
                # Basic heuristic: avoid Wikipedia-like metadata
                if not text.startswith(('Jump to', 'Navigation', 'Search')):
                    definitions.append(text)
                    if len(definitions) >= 5:
                        break
        
        if definitions:
            return {
                "query": word,
                "status": "found",
                "source": "https://dictionary.basabali.org",
                "definitions": definitions
            }
            
    except Exception as e:
        # Fallback to fuzzy offline if online fails
        pass

    # Try fuzzy offline as last resort
    matches = []
    for k, v in _BALI_DICT.items():
        if isinstance(v, dict):
            arti_v = v.get("arti", "").lower()
            ket_v = v.get("keterangan", "").lower()
            if word_key in k or word_key in arti_v or word_key in ket_v:
                matches.append(v)
                if len(matches) >= 5:
                    break
        elif isinstance(v, str):
            if word_key in k or word_key in v.lower():
                matches.append({"arti": v, "keterangan": ""})
                if len(matches) >= 5:
                    break
                
    if matches:
        return {
            "query": word,
            "status": "found",
            "source": "offline_bali_database_fuzzy",
            "definitions": matches
        }

    return {
        "query": word,
        "status": "not_found",
        "source": "https://dictionary.basabali.org"
    }
