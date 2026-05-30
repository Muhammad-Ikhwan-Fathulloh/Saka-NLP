import re
import asyncio

# Compiled regex for better performance
# This regex handles:
# 1. URLs
# 2. @mentions
# 3. #hashtags
# 4. Words (including underscores and numbers)
# 5. Emojis and other non-ascii symbols (preserved as individual tokens)
# 6. Punctuation (optional, but here we preserve meaningful ones)
TOKEN_PATTERN = re.compile(
    r'https?://\S+|@\w+|#\w+|\w+|[^\w\s]',
    re.UNICODE
)

def tokenize(text: str) -> list[str]:
    """
    Robust tokenizer for Indonesian social media text.
    Preserves URLs, mentions, hashtags, and emojis.
    """
    if not text:
        return []
    return TOKEN_PATTERN.findall(text)

def get_token_count(text: str) -> int:
    """Menghitung jumlah token dalam teks."""
    return len(tokenize(text))

async def async_tokenize(text: str) -> list[str]:
    """Asynchronous tokenization."""
    # Remove artificial sleep for performance
    return tokenize(text)

