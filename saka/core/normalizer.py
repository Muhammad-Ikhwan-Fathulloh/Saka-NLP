import asyncio
from typing import Dict
from ..dict.slang_dict import get_slang_dict

# Load slang dictionary into memory
_SLANG_DICT: Dict[str, str] = get_slang_dict()

def normalize(text: str) -> str:
    """
    Normalizes slang / informal words into standard Indonesian.
    """
    from .tokenizer import tokenize
    
    tokens = tokenize(text)
    normalized_tokens = []
    
    for token in tokens:
        lower_token = token.lower()
        if lower_token in _SLANG_DICT:
            # Preserve original casing roughly if it was title case
            if token.istitle():
                normalized_tokens.append(_SLANG_DICT[lower_token].title())
            else:
                normalized_tokens.append(_SLANG_DICT[lower_token])
        else:
            normalized_tokens.append(token)
            
    # Simple reconstruction
    # A true detokenizer would handle punctuation better
    return " ".join(normalized_tokens)

async def async_normalize(text: str) -> str:
    """
    Asynchronous normalization.
    """
    await asyncio.sleep(0.001)
    return normalize(text)
