import re
import asyncio

def tokenize(text: str) -> list[str]:
    """
    Tokenizes text into a list of words, removing basic punctuation.
    """
    # Simple regex to extract words
    return re.findall(r'\b\w+\b', text)

async def async_tokenize(text: str) -> list[str]:
    """
    Asynchronous tokenization for non-blocking operations on large batches.
    """
    # Emulate async work
    await asyncio.sleep(0.001)
    return tokenize(text)
