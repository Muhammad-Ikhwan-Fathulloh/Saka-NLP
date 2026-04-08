"""
Aksara Sunda transliteration plugin based on SundaDigi.com mapping.
"""

# Independent Vowels (Aksara Swara)
_SWARA = {
    "a": "ᮃ",
    "i": "ᮄ",
    "u": "ᮅ",
    "é": "ᮆ",
    "o": "ᮇ",
    "e": "ᮈ",
    "eu": "ᮉ",
}

# Consonants (Ngalagena) - The base character inherently carries the 'a' sound.
_NGALAGENA = {
    "k": "ᮊ", "g": "ᮌ", "ng": "ᮍ",
    "c": "ᮎ", "j": "ᮏ", "ny": "ᮑ",
    "t": "ᮒ", "d": "ᮓ", "n": "ᮔ",
    "p": "ᮕ", "b": "ᮘ", "m": "ᮙ",
    "y": "ᮚ", "r": "ᮛ", "l": "ᮜ", "w": "ᮝ",
    "s": "ᮞ", "h": "ᮠ",
    "f": "ᮖ", "v": "ᮗ", "q": "ᮋ", "x": "ᮟ", "z": "ᮐ",
    "sy": "ᮯ", "kh": "ᮮ"
}

# Vowel Signs (Rarangken)
_RARANGKEN = {
    "i": "ᮤ",   # Panghulu
    "e": "ᮨ",   # Pamepet
    "eu": "ᮩ",  # Paneuleung
    "é": "ᮦ",   # Panéléng
    "o": "ᮧ",   # Panolong
    "u": "ᮥ",   # Panyuku
}

# Final Consonant Modifiers (Rarangken)
# Note: Usually handled separately in phonetic logic.
_FINAL_MOD = {
    "r": "ᮁ",   # Panglayar
    "h": "ᮂ",   # Pangwisad
    "ng": "ᮀ",  # Panyecek
}

_PATEN = "᮪" # Pamaéh (mutes the inherent 'a')

_NUMBERS = {
    "0": "᮰", "1": "᮱", "2": "᮲", "3": "᮳", "4": "᮴",
    "5": "᮵", "6": "᮶", "7": "᮷", "8": "᮸", "9": "᮹"
}

def latin_to_aksara_sunda(text: str) -> str:
    """
    Converts Latin text to Aksara Sunda using rule-based phonetic mapping.
    """
    text = text.lower()
    result = ""
    i = 0
    while i < len(text):
        # 1. Handle Numbers
        if text[i] in _NUMBERS:
            result += _NUMBERS[text[i]]
            i += 1
            continue
            
        # 2. Handle Consonants (Ngalagena + Rarangken)
        match_found = False
        # Check longest consonant clusters first (e.g. "ng", "ny", "sy", "kh")
        for c_len in [2, 1]:
            if i + c_len <= len(text):
                consonant = text[i:i+c_len]
                if consonant in _NGALAGENA:
                    base = _NGALAGENA[consonant]
                    i += c_len
                    
                    # Peek next for vowels or modifiers
                    # Priority 1: Vowels (iuéoeu) - Note 'eu' is 2 chars
                    vowel_handled = False
                    if i < len(text):
                        if i + 2 <= len(text) and text[i:i+2] == "eu":
                            result += base + _RARANGKEN["eu"]
                            i += 2
                            vowel_handled = True
                        elif text[i] in "iuéoeu":
                            result += base + _RARANGKEN[text[i]]
                            i += 1
                            vowel_handled = True
                        elif text[i] == "a":
                            # Inherent 'a' - just the base
                            result += base
                            i += 1 # Consume 'a'
                            vowel_handled = True
                            
                    if not vowel_handled:
                        # No vowel follows. In Sundanese, if a consonant is followed by 
                        # another consonant (excluding R) or it's the end of word, 
                        # it might need a Paten if we want to mute 'a'.
                        # However, by default, if followed by space/end, it keeps 'a'.
                        # If followed by another consonant, it MUST have Paten.
                        if i < len(text) and text[i].isalpha() and text[i] not in "aiuéoeu":
                             # It's a consonant cluster like "st" -> "ᮞ᮪ᮒ"
                             result += base + _PATEN
                        else:
                             result += base
                             
                    match_found = True
                    break
        
        if match_found: continue
        
        # 3. Handle Independent Vowels (Aksara Swara)
        if text[i] in "aiuéoeu":
            if i + 2 <= len(text) and text[i:i+2] == "eu":
                result += _SWARA["eu"]
                i += 2
            else:
                result += _SWARA[text[i]]
                i += 1
            continue
            
        # 4. Fallback for spaces, symbols, etc.
        result += text[i]
        i += 1
        
    return result

def aksara_sunda_to_latin(aksara_text: str) -> str:
    """
    Transliterates Aksara Sunda back to Latin (Simplified mapping).
    """
    # Create reverse mapping once
    rev = {v: k for k, v in _SWARA.items()}
    rev.update({v: k + "a" for k, v in _NGALAGENA.items()}) # Base Ngalagena ends in 'a'
    rev.update({v: k for k, v in _RARANGKEN.items()})
    rev.update({v: k for k, v in _NUMBERS.items()})
    rev.update({_PATEN: ""}) # mutes 'a'
    
    # Needs smarter logic to remove 'a' if followed by rarangken
    # But for a basic bridge, this is a start.
    res = ""
    for j, char in enumerate(aksara_text):
        if char in rev:
            val = rev[char]
            # If current is rarangken, it should replace the 'a' of previous ngalagena
            if char in _RARANGKEN.values() and res.endswith("a"):
                res = res[:-1] + val
            elif char == _PATEN and res.endswith("a"):
                res = res[:-1]
            else:
                res += val
        else:
            res += char
    return res
# Default export for backward compatibility
def transliterate(aksara_text: str) -> str:
    return aksara_sunda_to_latin(aksara_text)

def latin_to_aksara(text: str) -> str:
    return latin_to_aksara_sunda(text)

def aksara_to_latin(aksara_text: str) -> str:
    return aksara_sunda_to_latin(aksara_text)
