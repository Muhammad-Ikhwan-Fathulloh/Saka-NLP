import re
from typing import Dict, Any, List, Optional

# Constants for transactional context
PRICE_KEYWORDS = {'harga', 'nego', 'rp', 'jadi', 'pas', 'nett', 'bayar', 'biaya'}
QUANTITY_KEYWORDS = {'pcs', 'buah', 'biji', 'stok', 'unit', 'kuantitas', 'set', 'pax'}

def parse_transaction_units(text: str) -> str:
    """
    Normalizes numeric suffixes common in Indonesian transactions.
    Example: 10k -> 10000, 50rb -> 50000, 1jt -> 1000000.
    """
    def replace_suffix(match):
        num = match.group(1)
        suffix = match.group(2).lower()
        if suffix in ['k', 'rb', 'ribu']:
            return str(int(num) * 1000)
        elif suffix in ['jt', 'juta']:
            return str(int(num) * 1000000)
        return match.group(0)

    # Patterns like 10k, 10rb, 10 rb, 1jt, 1 jt
    pattern = r'(\d+)\s*(k|rb|ribu|jt|juta)\b'
    return re.sub(pattern, replace_suffix, text, flags=re.IGNORECASE)

def extract_transaction_entities(text: str) -> List[Dict[str, Any]]:
    """
    Identifies transaction entities (Price, Quantity) based on context.
    Returns a list of detected entities.
    """
    from .tokenizer import tokenize
    
    # First normalize the units so we have clean numbers
    normalized_text = parse_transaction_units(text)
    tokens = tokenize(normalized_text)
    
    entities = []
    
    for i, token in enumerate(tokens):
        if token.isdigit():
            val = int(token)
            context_type = "UNKNOWN"
            
            # Check context (window of 2 tokens before and after)
            window_start = max(0, i - 2)
            window_end = min(len(tokens), i + 3)
            context_tokens = [t.lower() for t in tokens[window_start:window_end]]
            
            # Heuristics
            # Check immediate neighbors for explicit units
            prev_token = tokens[i-1].lower() if i > 0 else ""
            next_token = tokens[i+1].lower() if i < len(tokens) - 1 else ""
            
            is_immediate_qty = prev_token in QUANTITY_KEYWORDS or next_token in QUANTITY_KEYWORDS
            is_price_kw = any(kw in context_tokens for kw in PRICE_KEYWORDS)
            is_qty_kw = any(kw in context_tokens for kw in QUANTITY_KEYWORDS)
            
            if is_immediate_qty:
                context_type = "QUANTITY"
            elif is_price_kw:
                context_type = "PRICE"
            elif is_qty_kw:
                context_type = "QUANTITY"
            elif val >= 1000:
                context_type = "PRICE"
            elif val > 0:
                context_type = "QUANTITY"

            entities.append({
                "value": val,
                "type": context_type,
                "original_token": tokens[i]
            })
            
    return entities
