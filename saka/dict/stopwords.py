import os
import json
from typing import Set

_SUNDA_STOPWORDS = {
    "teu", "na", "ka", "ti", "ku", "di", "nu", "anu", "oge", "wae", 
    "bae", "mah", "teh", "tea", "jeung", "sareng", "naon", "saha", 
    "mana", "kumaha", "iraha", "naha", "pikeun", "kanggo", "pisan", 
    "kacida", "pasti", "tangtu", "bisa", "tiasa", "aya", "euweuh", "kunaon", "ieu", "éta",
    "ari", "nya", "atuh", "apan", "sok", "geura", "tuh", "kieu", "kitu", "engke", 
    "ayeuna", "duka", "teuing", "pangna", "basa", "mun", "lamun", "saupama", "sanaos", 
    "najan", "kawas", "jiga", "lir", "da", "dong", "ge", "wé", "weh"
}

_JAWA_STOPWORDS = {
    "lan", "utawa", "ing", "kang", "sing", "seng", "iki", "iku", 
    "kuwi", "apa", "opo", "sapa", "sopo", "piye", "kepiye", 
    "pira", "piro", "kapan", "nyang", "karo", "kalebet", "menawa", 
    "menawi", "bisa", "iso", "uga", "ugi", "ora", "mboten", "wis", "wes", "dudu", 
    "kene", "kono", "kui", "kae", "saka", "saking", "dadi", "dados", "amarga", "amargi", 
    "nanging", "ananging", "supaya", "supados", "yen", "yèn", "bilih", "nuli", "lajeng", 
    "banjur", "kados", "kaya", "kajaba", "kejawi", "malah", "satemah", "senajan", 
    "sanadyan", "enggal", "ndang", "akeh", "akèh", "kathah"
}

_BALI_STOPWORDS = {
    "di", "ke", "teken", "apang", "saja", "ada", "ene", "ento", "i", "ni",
    "tiang", "iraga", "ia", "cai", "nyai", "nanging", "laut", "suba", "tusing",
    "ngajeng", "mandaer", "neda", "keto", "kena", "be", "ne", "mare",
    "ring", "saking", "antuk", "tur", "lan", "miwah", "yening", "yen", "pinaka", "buat", 
    "kanti", "sadurung", "sampun", "wau", "mangda", "ipun", "dane", "ida", "niki", "nika", 
    "puniki", "punika", "sane", "ane", "indik", "kadi", "buka"
}

_EN_STOPWORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are",
    "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
    "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about",
    "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up",
    "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when",
    "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor",
    "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now",
    "also", "could", "would", "might", "must", "however", "therefore", "thus", "instead", "anyway", "cannot"
}

_JAKSEL_STOPWORDS = {
    "literally", "basically", "which", "which is", "whichis", "like", "tbh", "fyi", "jujurly", "at least", "so", 
    "as in", "btw", "anyway", "somehow", "even", "actually", "well", "cmiiw", "asap", "make sense", "worth it",
    "end of the day", "at the end of the day", "i mean", "you know", "in terms of", "let's say", "to be honest", 
    "not gonna lie", "ngl", "lowkey", "highkey", "for real", "fr", "periodt", "kinda", "sorta", "dunno", "lemme", 
    "gimme", "gonna", "wanna", "gotta", "obviously", "seriously", "prefer", "vibes", "relate", "cringe", "awkward"
}

_MINANG_STOPWORDS = {
    "nan", "jo", "dek", "di", "ko", "iko", "tu", "dari", "dan", "atau",
    "pado", "juo", "untuak", "ka", "dalam", "pulo", "lai", "lah",
    "adolah", "marupokan", "sabagai", "indak", "alah", "ado",
    "kini", "inyo", "nyo", "itu", "pun", "tapi", "namun",
    "karano", "basamo", "sarato", "sacaro", "sahinggo", "sainggo",
    "baitu", "mako", "supayo", "sadangkan", "tatapi", "walaupun",
    "ataupun", "maupun", "bahwa", "kalau", "dima", "katiko",
    "akan", "bisa", "harus", "masih", "bagi", "sarajo",
    "surang", "sajo", "hanyo", "biaso", "biasonyo", "umumnyo",
    "sangaik", "bana", "labiah", "paliang", "alun", "mangko"
}

def get_stopwords(lang: str = "all") -> Set[str]:
    """
    Returns a set of stopwords. 
    Lang options: 'id' (Indonesian), 'sunda', 'jawa', 'bali', 'minang' (Minangkabau), 'en' (English), 'jaksel' (South Jakarta Slang), 'all' (combined).
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
        
    if lang in ['en', 'all']:
        stopwords.update(_EN_STOPWORDS)
        
    if lang in ['jaksel', 'all']:
        stopwords.update(_JAKSEL_STOPWORDS)
        
    if lang in ['minang', 'all']:
        stopwords.update(_MINANG_STOPWORDS)
        
    return stopwords
