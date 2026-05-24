import re
import asyncio

def tokenize(text: str) -> list[str]:
    return re.findall(r'\b\w+\b', text)

def get_token_count(text: str) -> int:
    """Menghitung jumlah token dalam teks."""
    return len(tokenize(text))

async def async_tokenize(text: str) -> list[str]:
    await asyncio.sleep(0.001)
    return tokenize(text)
