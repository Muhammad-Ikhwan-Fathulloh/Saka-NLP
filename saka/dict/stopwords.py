import os
from typing import Set

def get_stopwords() -> Set[str]:
    """
    Returns a set of Indonesian stopwords (Tala dataset).
    """
    current_dir = os.path.dirname(__file__)
    txt_path = os.path.join(current_dir, 'stopwords.txt')
    stopwords = set()
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word:
                    stopwords.add(word)
    except FileNotFoundError:
        print(f"Warning: Stopwords file not found at {txt_path}. get_stopwords() will return empty set.")
        pass
    return stopwords
