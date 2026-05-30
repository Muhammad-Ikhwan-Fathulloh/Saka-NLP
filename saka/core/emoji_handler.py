import emoji
from emot.core import emot

# Initialize emot
_EMOT_OBJ = emot()

def demojize(text: str) -> str:
    """
    Converts Unicode emojis to Indonesian text aliases.
    Example: ❤️ -> cinta
    """
    # Use emoji library to demojize with 'id' language
    demojized = emoji.demojize(text, language='id')
    
    # Remove colons from the output (e.g., :jempol_ke_atas: -> jempol_ke_atas)
    # and replace underscores with spaces
    import re
    # Match patterns like :alias:
    result = re.sub(r':([a-z0-9_]+):', lambda m: m.group(1).replace('_', ' '), demojized)
    
    return result

def replace_emoticons(text: str) -> str:
    """
    Converts standard emoticons to text.
    Example: :) -> smiley
    """
    results = _EMOT_OBJ.emoticons(text)
    if not results or not results.get('flag'):
        return text
        
    # We replace from right to left to avoid index shift issues
    new_text = text
    # emot returns lists of values, meanings, and positions
    # example structure: {'value': [':)'], 'mean': ['Happy face or smiley'], 'location': [[5, 7]], 'flag': True}
    
    # We'll use a simple strategy: replace each occurrence found
    # Note: emot meanings are currently in English. 
    # For a perfect Indonesian pipeline, we'd need a translation map,
    # but the user said "emot (same)", implying using it as is or as it was used before.
    
    for i in range(len(results['value'])-1, -1, -1):
        start, end = results['location'][i]
        meaning = results['mean'][i]
        # Basic mapping for common English meanings to Indonesian if possible
        # but let's stick to the simplest implementation first.
        new_text = new_text[:start] + f" {meaning} " + new_text[end:]
        
    return " ".join(new_text.split()) # Clean up extra spaces
