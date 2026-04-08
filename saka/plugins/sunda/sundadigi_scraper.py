import requests
from typing import Dict, Any, List

class SundaDigiException(Exception):
    pass

def query_sundadigi(word: str) -> Dict[str, Any]:
    """
    Queries the SundaDigi dictionary for a given Sundanese word.
    Note: Requires an active internet connection.
    This scraper uses the background Meilisearch API of SundaDigi for accuracy.
    """
    url = "https://vps.sundadigi.com/indexes/kamus/search"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Authorization': 'Bearer 5cce4f723b5da38498d0907d96afce5459cd3369f3162bb5f74bb02fc0592d6e',
        'Content-Type': 'application/json'
    }
    
    # Meilisearch standard payload
    payload = {
        "q": word,
        "limit": 5
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        raise SundaDigiException(f"Failed to fetch from SundaDigi API: {e}")
        
    hits = data.get('hits', [])
    
    if not hits:
        return {
            "query": word,
            "status": "not_found",
            "source": "https://sundadigi.com/"
        }
        
    definitions = []
    for hit in hits:
        # Actual SundaDigi Meilisearch fields: 'entry', 'definition', 'tipe', 'sumber'
        entry_word = hit.get('entry', '')
        definition = hit.get('definition', '')
        tipe = hit.get('tipe', '')
        
        if definition:
            entry = f"[{tipe}] {entry_word}: {definition}" if tipe else f"{entry_word}: {definition}"
            definitions.append(entry.strip())
            
    if not definitions:
        # Final fallback
        for hit in hits:
            definitions.append(str(hit))

    return {
        "query": word,
        "status": "found",
        "source": "https://sundadigi.com/",
        "definitions": definitions[:5]
    }
