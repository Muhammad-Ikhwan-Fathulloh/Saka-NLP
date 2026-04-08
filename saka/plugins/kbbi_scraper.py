import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List

class KBBIException(Exception):
    pass

def query_kbbi(word: str) -> Dict[str, Any]:
    """
    Queries the unofficial but popular kbbi.web.id dictionary for a given word.
    Note: Requires an active internet connection.
    """
    url = f"https://kbbi.web.id/{word}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise KBBIException(f"Failed to fetch from KBBI: {e}")
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # In kbbi.web.id, the content is in <div id="desc"> and specifically <div id="d1">
    desc_div = soup.find('div', id='desc')
    if not desc_div:
        return {
            "query": word,
            "status": "not_found",
            "source": "https://kbbi.web.id/"
        }
    
    d1_div = desc_div.find('div', id='d1')
    if not d1_div:
        # Fallback to the whole desc div if d1 is missing
        d1_div = desc_div
        
    # Check if there's any bold word entry (headword or derivative)
    has_entry = d1_div.find('b')
    if not has_entry:
        return {
            "query": word,
            "status": "not_found",
            "source": "https://kbbi.web.id/"
        }
        
    definitions = []
    
    # Extraction logic:
    # kbbi.web.id structure: <b>word</b> <em>pos</em> definition; <b>2</b> <em>pos</em> definition
    # We want to extract parts that follow <em> tags.
    
    # Simple heuristic: Split by ';' which usually separates meanings on kbbi.web.id
    # but cleanup the word/pos tags.
    
    # We'll iterate through child elements of d1_div
    current_def = ""
    for element in d1_div.children:
        if element.name == 'em':
            # POS tag found, following text is likely definition
            continue
        elif element.name == 'b':
            # New word or number found, might indicate start of new definition
            if current_def:
                definitions.append(current_def.strip())
                current_def = ""
            continue
        elif isinstance(element, str):
            # Text node, potentially the definition content
            content = element.strip()
            if content:
                # Remove leading punctuation like ':' or numbers if any
                if content.startswith(': '):
                    content = content[2:]
                elif content.startswith(':'):
                    content = content[1:]
                
                current_def += " " + content
    
    if current_def:
        definitions.append(current_def.strip())
        
    # Final cleanup of definitions (remove empty, limit result)
    # Often definitions are separated by ';' in one text block
    final_definitions = []
    for d in definitions:
        if ";" in d:
             for sub_d in d.split(";"):
                 sub_d = sub_d.strip()
                 if sub_d and len(sub_d) > 2:
                     final_definitions.append(sub_d)
        else:
            d = d.strip()
            if d and len(d) > 2:
                final_definitions.append(d)
                
    if not final_definitions:
         # One more fallback: just get the cleaned text if extraction was too aggressive
         text = d1_div.get_text(separator=' ').strip()
         if ":" in text:
             text = text.split(":", 1)[1]
         final_definitions = [d.strip() for d in text.split(";") if d.strip()]

    return {
        "query": word,
        "status": "found",
        "source": f"https://kbbi.web.id/{word}",
        "definitions": final_definitions[:5]
    }
