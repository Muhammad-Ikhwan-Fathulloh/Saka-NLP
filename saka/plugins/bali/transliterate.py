"""
Aksara Bali transliteration plugin based on Balinese Unicode Block (U+1B00-U+1B7F).
"""

# Independent Vowels (Aksara Swara)
_SWARA = {
    "a": "ᬅ",
    "i": "ᬇ",
    "u": "ᬉ",
    "e": "ᬏ",
    "o": "ᬑ",
}

# Consonants (Wreastra) - Base characters inherently carry 'a'
_WREASTRA = {
    "ha": "ᬳ", "na": "ᬦ", "ca": "ᬘ", "ra": "ᬭ", "ka": "ᬓ",
    "da": "ᬤ", "ta": "ᬢ", "sa": "ᬲ", "wa": "ᬯ", "la": "ᬮ",
    "ma": "ᬫ", "ga": "ᬕ", "ba": "ᬩ", "nga": "ᬗ",
    "pa": "ᬧ", "ja": "ᬚ", "ya": "ᬬ", "ny": "ᬜ", "nya": "ᬜ"
}

# Vowel Signs (Pangangge Suara)
_PANGANGGE_SUARA = {
    "i": "ᬶ",   # Ulu
    "u": "ᬸ",   # Suku
    "é": "ᬾ",   # Taling
    "o": "ᭀ",   # Taling Detia
    "e": "ᬺ",   # Pepet
    "ě": "ᬺ",  # Pepet
}

# Final Consonant Modifiers (Pangangge Tengenan)
_TENGANAN = {
    "r": "ᬃ",   # Surang
    "h": "ᬄ",   # Bisah
    "ng": "ᬂ",  # Cecek
}

_ADEG_ADEG = "᭄" # Mutes the inherent 'a'

_NUMBERS = {
    "0": "᭐", "1": "᭑", "2": "᭒", "3": "᭓", "4": "᭔",
    "5": "᭕", "6": "᭖", "7": "᭗", "8": "᭘", "9": "᭙"
}

_PUNCTUATION = {
    ",": "᭞", # Carik Siki
    ".": "᭟", # Carik Pareren
}

def latin_to_aksara_bali(text: str) -> str:
    """
    Converts Latin text to Aksara Bali using rule-based phonetic mapping.
    """
    text = text.lower()
    result = ""
    i = 0
    while i < len(text):
        if text[i] == " ":
            result += " "
            i += 1
            continue
            
        if text[i] in _NUMBERS:
            result += _NUMBERS[text[i]]
            i += 1
            continue
            
        if text[i] in _PUNCTUATION:
            result += _PUNCTUATION[text[i]]
            i += 1
            continue
            
        match_found = False
        
        # Consonant groups
        for c_len in [3, 2, 1]:
            if i + c_len <= len(text):
                cluster = text[i:i+c_len]
                # If cluster is like 'ba', it already has 'a'
                if cluster in _WREASTRA:
                   result += _WREASTRA[cluster]
                   i += c_len
                   match_found = True
                   break
                
                # Check for final modifiers (r, h, ng)
                is_end = (i + c_len >= len(text) or not text[i+c_len].isalpha())
                if cluster in _TENGANAN and is_end:
                   result += _TENGANAN[cluster]
                   i += c_len
                   match_found = True
                   break
                
                # Check for consonant + inherent 'a' logic (e.g. 'b' followed by something)
                chunk = cluster + "a"
                if chunk in _WREASTRA:
                    base = _WREASTRA[chunk]
                    i += c_len
                    
                    found_vowel = False
                    if i < len(text):
                        if text[i] in "iuéeo":
                            result += base + _PANGANGGE_SUARA[text[i]]
                            i += 1
                            found_vowel = True
                        elif text[i] == "a":
                            result += base
                            i += 1
                            found_vowel = True
                        elif text[i] == "e":
                            # Pepet
                            result += base + _PANGANGGE_SUARA["e"]
                            i += 1
                            found_vowel = True
                            
                    if not found_vowel:
                        # If followed by another alpha (consonant), mute this one
                        if i < len(text) and text[i].isalpha():
                           result += base + _ADEG_ADEG
                        elif is_end:
                           result += base + _ADEG_ADEG
                        else:
                           # Alone at end or something
                           result += base
                    
                    match_found = True
                    break
                    
        if match_found: continue
        
        # Independent Vowels
        if text[i] in "aiuéeo":
            if text[i] == "a":
                result += _SWARA["a"]
            elif text[i] in _SWARA:
                result += _SWARA[text[i]]
            else:
                result += _WREASTRA["ha"] + _PANGANGGE_SUARA.get(text[i], "")
            i += 1
            continue
            
        result += text[i]
        i += 1
        
    return result

def aksara_bali_to_latin(aksara_text: str) -> str:
    """
    Reverse transliteration for Aksara Bali.
    """
    # Inverse map
    rev = {v: k for k, v in _WREASTRA.items()}
    rev.update({v: k for k, v in _SWARA.items()})
    rev.update({v: k for k, v in _PANGANGGE_SUARA.items()})
    rev.update({v: k for k, v in _TENGANAN.items()})
    rev.update({v: k for k, v in _NUMBERS.items()})
    rev.update({v: k for k, v in _PUNCTUATION.items()})
    
    # Specific repairs
    rev["ᬳ"] = "ha"
    
    res = ""
    for char in aksara_text:
        if char == _ADEG_ADEG:
            if res.endswith("a"):
                res = res[:-1]
        elif char in rev:
            val = rev[char]
            if char in _PANGANGGE_SUARA.values() or char in _TENGANAN.values():
                if res.endswith("a"):
                    res = res[:-1] + val
                else:
                    res += val
            else:
                res += val
        else:
            res += char
            
    # Cleanup 'ha' -> 'a' for start
    res = res.replace("haa", "a")
    return res

# Aliases
latin_to_aksara = latin_to_aksara_bali
aksara_to_latin = aksara_bali_to_latin
