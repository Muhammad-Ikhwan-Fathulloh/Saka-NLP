import requests
from bs4 import BeautifulSoup
from typing import Dict, Any

class SundaDigiException(Exception):
    pass

def query_sundadigi(word: str) -> Dict[str, Any]:
    """
    Queries the SundaDigi dictionary for a given Sundanese word.
    Note: Requires an active internet connection.
    This scraper acts as a bridge for the Sunda plugin to fetch meanings.
    """
    # Assuming standard path. Actual SundaDigi paths may vary based on exact endpoints.
    url = f"https://sundadigi.com/kamus?q={word}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise SundaDigiException(f"Failed to fetch from SundaDigi: {e}")
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Minimal skeleton scraper for SundaDigi.
    # We will grab all text blocks and try a heuristic match for meaning lines.
    definitions = []
    
    # Many modern dictionary sites enclose search results in standard DOM elements.
    # As SundaDigi implementation varies, we fall back to generic extraction for initialization.
    for para in soup.find_all('p'):
        text = para.text.strip()
        if text and len(text) > 3 and word.lower() in text.lower():
            definitions.append(text)
            
    if not definitions:
         return {
            "query": word,
            "status": "not_found_or_cannot_parse",
            "source": "https://sundadigi.com/"
        }
            
    return {
        "query": word,
        "status": "found",
        "source": "https://sundadigi.com/",
        "definitions": definitions[:3] # Batasi hasil untuk mencegah overload UI
    }
