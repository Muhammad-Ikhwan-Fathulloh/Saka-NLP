import re

def clean_html(text: str) -> str:
    """Removes HTML tags from a string."""
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', text)

def remove_multiple_spaces(text: str) -> str:
    """Replaces multiple spaces with a single space."""
    return re.sub(r'\s+', ' ', text).strip()
