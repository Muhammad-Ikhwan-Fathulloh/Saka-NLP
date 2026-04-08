import requests
from bs4 import BeautifulSoup
from typing import Dict, Any

class KBBIException(Exception):
    pass

def query_kbbi(word: str, cookies: Dict[str, str] = None) -> Dict[str, Any]:
    """
    Queries the official Kemendikdasmen KBBI dictionary for a given word.
    Note: Requires an active internet connection.
    You can provide session cookies if you have a KBBI account.
    """
    url = f"https://kbbi.kemendikdasmen.go.id/entri/{word}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise KBBIException(f"Failed to fetch from KBBI: {e}")
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # KBBI marks 'Entri tidak ditemukan' if not found
    not_found = soup.find(string=lambda text: text and "Entri tidak ditemukan" in text)
    if not_found:
        return {
            "query": word,
            "status": "not_found",
            "source": "https://kbbi.kemendikdasmen.go.id/"
        }
        
    definitions = []
    
    # Try parsing definition lists from KBBI structure
    # Usually definitions are inside <ul class="adjusted-par"> or raw text blocks
    ul_par = soup.find('ul', class_='adjusted-par')
    if ul_par:
        list_items = ul_par.find_all('li')
        for li in list_items:
            if li.text.strip():
                definitions.append(li.text.strip())
            
    # As a fallback if the structure is just paragraphs
    if not definitions:
        paras = soup.find_all('p')
        for p in paras:
            definitions.append(p.text.strip())
            
    return {
        "query": word,
        "status": "found",
        "source": "https://kbbi.kemendikdasmen.go.id/",
        "definitions": definitions[:5] # Return top 5 elements
    }
