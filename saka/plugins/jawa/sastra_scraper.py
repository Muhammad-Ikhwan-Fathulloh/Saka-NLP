import os
import json
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List

class SastraException(Exception):
    pass

_DICT_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'dict', 'jawa_dict.json')
_JAWA_DICT = {}
if os.path.exists(_DICT_PATH):
    with open(_DICT_PATH, 'r', encoding='utf-8') as f:
        _JAWA_DICT = json.load(f)

def query_sastra(word: str, use_online: bool = False) -> Dict[str, Any]:
    """
    Queries the Javanese dictionary. Primary uses the offline sastra-jawa dataset.
    Optionally attempts to scrape sastra.org if the word is not found locally.
    """
    word_lower = word.lower()
    
    # Check Offline First
    if word_lower in _JAWA_DICT:
        return {
            "query": word,
            "status": "found",
            "source": "offline_sastra_database",
            "definitions": [_JAWA_DICT[word_lower]]
        }
    
    # Try searching keys that contain the word
    matches = []
    for k, v in _JAWA_DICT.items():
        if isinstance(v, dict):
            arti_v = v.get("arti", "").lower()
            ket_v = v.get("keterangan", "").lower()
            if word_lower in k or word_lower in arti_v or word_lower in ket_v:
                matches.append(v)
                if len(matches) >= 5:
                    break
        elif isinstance(v, str):
            if word_lower in k or word_lower in v:
                matches.append({ "arti": v, "keterangan": "" })
                if len(matches) >= 5:
                    break
                
    if matches:
        return {
            "query": word,
            "status": "found",
            "source": "offline_sastra_database_fuzzy",
            "definitions": matches
        }

    # Attempt Online (Sastra.org) if requested
    if use_online:
        url = f"https://www.sastra.org/katalog?q={word}"
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('td')
            if results:
                defs = [r.get_text(separator=" ").strip() for r in results[:5] if word_lower in r.get_text().lower()]
                if defs:
                    return {
                        "query": word,
                        "status": "found",
                        "source": "https://www.sastra.org",
                        "definitions": defs
                    }
        except Exception as e:
            pass # Fallthrough if site is down

    return {
        "query": word,
        "status": "not_found",
        "source": "database_and_online"
    }
