import os
from typing import Set

_SUNDA_STOPWORDS = {
    "teu", "na", "ka", "ti", "ku", "di", "nu", "anu", "oge", "wae", 
    "bae", "mah", "teh", "tea", "jeung", "sareng", "naon", "saha", 
    "mana", "kumaha", "iraha", "naha", "pikeun", "kanggo", "pisan", 
    "kacida", "pasti", "tangtu", "bisa", "tiasa", "aya", "euweuh", "kunaon", "ieu", "éta", "ieu"
}

_JAWA_STOPWORDS = {
    "lan", "utawa", "ing", "kang", "sing", "seng", "iki", "iku", 
    "kuwi", "apa", "opo", "sapa", "sopo", "piye", "kepiye", 
    "pira", "piro", "kapan", "nyang", "karo", "kalebet", "menawa", 
    "menawi", "bisa", "iso", "uga", "ugi", "ora", "mboten", "wis", "wes", "dudu", "iku"
}

_BALI_STOPWORDS = {
    "di", "ke", "teken", "apang", "saja", "ada", "ene", "ento", "i", "ni",
    "tiang", "iraga", "ia", "cai", "nyai", "nanging", "laut", "suba", "tusing",
    "ngajeng", "mandaer", "neda", "keto", "kena", "be", "ne", "ento", "mare"
}

def get_stopwords(lang: str = "all") -> Set[str]:
    """
    Returns a set of stopwords. 
    Lang options: 'id' (Indonesian), 'sunda', 'jawa', 'bali', 'all' (combined).
    Defaults to 'all' for maximum coverage of Nusantara text.
    """
    stopwords = set()
    
    if lang in ['id', 'all']:
        current_dir = os.path.dirname(__file__)
        txt_path = os.path.join(current_dir, 'stopwords.txt')
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        stopwords.add(word)
        except FileNotFoundError:
            print(f"Warning: Stopwords file not found at {txt_path}.")
            
    if lang in ['sunda', 'all']:
        stopwords.update(_SUNDA_STOPWORDS)
        
    if lang in ['jawa', 'all']:
        stopwords.update(_JAWA_STOPWORDS)
        
    if lang in ['bali', 'all']:
        stopwords.update(_BALI_STOPWORDS)
        
    return stopwords
