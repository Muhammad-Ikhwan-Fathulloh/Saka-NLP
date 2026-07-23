import asyncio
from typing import Dict
from functools import lru_cache
from ..dict.slang_dict import get_slang_dict

# Load slang dictionary into memory
_SLANG_DICT: Dict[str, str] = get_slang_dict()

@lru_cache(maxsize=10000)
def normalize(text: str) -> str:
    """
    Normalizes slang / informal words into standard Indonesian.
    """
    from .tokenizer import tokenize
    from .transaction import parse_transaction_units
    
    # Pre-normalization: handle transactional units (10k -> 10000)
    text = parse_transaction_units(text)
    
    tokens = tokenize(text)
    normalized_tokens = []
    
    for token in tokens:
        lower_token = token.lower()
        if lower_token in _SLANG_DICT:
            mapped_val = _SLANG_DICT[lower_token]
            # Preserve original casing
            if token.isupper():
                normalized_tokens.append(mapped_val.upper())
            elif token.istitle():
                normalized_tokens.append(mapped_val.title())
            else:
                normalized_tokens.append(mapped_val)
        else:
            normalized_tokens.append(token)
            
    # Simple detokenizer to handle punctuation better
    import re
    reconstructed = " ".join(normalized_tokens)
    # Remove spaces before punctuation marks
    reconstructed = re.sub(r'\s+([.,!?:;])', r'\1', reconstructed)
    return reconstructed

async def async_normalize(text: str) -> str:
    """
    Asynchronous normalization.
    """
    return normalize(text)
