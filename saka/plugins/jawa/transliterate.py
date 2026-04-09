"""
Aksara Jawa (Hanacaraka) transliteration plugin based on Javanese Unicode Block (U+A980-U+A9DF).
"""

# Base Consonants (Aksara Nglegéna) - Inherent 'a'
_NGALAGENA = {
    "ha": "ꦲ", "na": "ꦤ", "ca": "ꦕ", "ra": "ꦫ", "ka": "ꦏ",
    "da": "ꦢ", "ta": "ꦠ", "sa": "ꦱ", "wa": "ꦮ", "la": "ꦭ",
    "pa": "ꦥ", "dha": "ꦝ", "ja": "ꦗ", "ya": "ꦪ", "nya": "ꦚ",
    "ma": "ꦩ", "ga": "ꦒ", "ba": "ꦧ", "tha": "ꦛ", "nga": "ꦔ",
    # Additional basic bindings
    "ny": "ꦚ", "dh": "ꦝ", "th": "ꦛ", "ng": "ꦔ"
}

# Vowel Signs (Sandhangan Swara)
_SANDHANGAN = {
    "i": "ꦶ", # Wulu
    "u": "ꦸ", # Suku
    "é": "ꦺ", # Taling
    "e": "ꦼ", # Pepet
    "è": "ꦺ", # Taling
    "o": "ꦺꦴ" # Taling Tarung
}

# Final Modifiers (Sandhangan Panyigeg)
_FINAL_MOD = {
    "ng": "ꦁ", # Cecak
    "r": "ꦂ",  # Layar
    "h": "ꦃ",  # Wignyan
}

_PANGKON = "꧀" 

_NUMBERS = {
    "0": "꧐", "1": "꧑", "2": "꧒", "3": "꧓", "4": "꧔",
    "5": "꧕", "6": "꧖", "7": "꧗", "8": "꧘", "9": "꧙"
}

def latin_to_aksara_jawa(text: str) -> str:
    """
    Converts Latin text to Aksara Jawa using rule-based phonetic mapping (Simplified).
    """
    text = text.lower()
    result = ""
    i = 0
    while i < len(text):
        if text[i] in _NUMBERS:
            result += _NUMBERS[text[i]]
            i += 1
            continue
            
        match_found = False
        
        # Consonant groups
        for c_len in [3, 2, 1]:
            if i + c_len <= len(text):
                chunk = text[i:i+c_len] + "a" 
                cluster_key = text[i:i+c_len]
                
                # Exclude vowels immediately mapped 
                if cluster_key in "aiuéèo":
                    continue
                
                # Check for final modifiers (e.g. word boundary or specific final)
                is_final = (i + c_len >= len(text) or not text[i+c_len].isalpha())
                if cluster_key in _FINAL_MOD and is_final:
                    result += _FINAL_MOD[cluster_key]
                    i += c_len
                    match_found = True
                    break
                    
                if chunk in _NGALAGENA or cluster_key in _NGALAGENA:
                    base_key = chunk if chunk in _NGALAGENA else cluster_key
                    base = _NGALAGENA[base_key]
                    i += c_len
                    
                    vowel_handled = False
                    if i < len(text):
                        if text[i] in "iuéèo":
                            if text[i] == "o":
                                # Taling Tarung sequence: ꦺ + base + ꦴ 
                                # Unicode standard sometimes prefers ꦺꦴ combined after base
                                result += base + "ꦺꦴ"
                            else:
                                result += base + _SANDHANGAN[text[i]]
                            i += 1
                            vowel_handled = True
                        elif text[i] == "a":
                            result += base
                            i += 1
                            vowel_handled = True
                    
                    if not vowel_handled:
                        if i < len(text) and text[i].isalpha() and text[i] not in "aiuéèo":
                            result += base + _PANGKON
                        else:
                            # End of word without explicit vowel => typically pangkon in standard orthography 
                            # unless default inherent 'a' is intended (rare at word end without explicit 'a' in latin mapping)
                            # Actually, Indonesian/Javanese latin transliteration uses 'a' explicitly if intended.
                            # So consonant at word end gets pangkon.
                            if is_final:
                                result += base + _PANGKON
                            else:
                                result += base

                    match_found = True
                    break
        
        if match_found: 
            continue
            
        # Independent Vowels
        if text[i] in "aiuéèo":
            if text[i] == "a":
                result += _NGALAGENA["ha"]
            elif text[i] in _SANDHANGAN:
                if text[i] == "o":
                    result += _NGALAGENA["ha"] + "ꦺꦴ"
                else:
                    result += _NGALAGENA["ha"] + _SANDHANGAN[text[i]]
            i += 1
            continue
            
        # Fallback for spec
        result += text[i]
        i += 1
        
    return result

def aksara_jawa_to_latin(aksara_text: str) -> str:
    """
    Transliterates Aksara Jawa back to Latin (Highly Simplified mapping).
    """
    rev = {v: k[:-1] if k.endswith('a') and len(k) > 1 else 'h' if k == 'ha' else k 
           for k, v in _NGALAGENA.items() if k not in ["ny","dh","th","ng"]} 
    # Use standard 2-char base mapped
    rev.update({"ꦲ": "ha", "ꦤ": "na", "ꦕ": "ca", "ꦫ": "ra", "ꦏ": "ka",
                "ꦢ": "da", "ꦠ": "ta", "ꦱ": "sa", "ꦮ": "wa", "ꦭ": "la",
                "ꦥ": "pa", "ꦝ": "dha", "ꦗ": "ja", "ꦪ": "ya", "ꦚ": "nya",
                "ꦩ": "ma", "ꦒ": "ga", "ꦧ": "ba", "ꦛ": "tha", "ꦔ": "nga"})

    rev.update({v: k for k, v in _SANDHANGAN.items()})
    rev.update({v: k for k, v in _FINAL_MOD.items()})
    rev.update({v: k for k, v in _NUMBERS.items()})
    rev.update({"ꦺꦴ": "o", "ꦺ": "é"})
    
    res = ""
    for char in aksara_text:
        if char == _PANGKON:
            if res.endswith("a"):
                res = res[:-1]
        elif char in rev:
            val = rev[char]
            if char in _SANDHANGAN.values() or char == "ꦺꦴ":
                if res.endswith("a"):
                    res = res[:-1] + val
                else:
                    res += val
            else:
                res += val
        else:
            res += char
            
    res = res.replace("haa", "a").replace("ae", "e")
    return res

# Aliases
latin_to_aksara = latin_to_aksara_jawa
aksara_to_latin = aksara_jawa_to_latin
