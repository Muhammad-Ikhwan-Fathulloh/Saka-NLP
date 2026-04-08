import os
import sys

# Add the current directory to sys.path
sys.path.append(r"d:\Saka-NLP")
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import saka

def test_sunda_transliteration():
    # Test simple mapping
    latin = "saka"
    aksara = saka.latin_to_aksara_sunda(latin)
    print(f"Latin: {latin} -> Aksara: {aksara}")
    
    latin_back = saka.aksara_sunda_to_latin(aksara)
    print(f"Aksara: {aksara} -> Latin: {latin_back}")
    
    # Test with vowels
    words = ["ka", "ki", "ku", "ké", "ko", "ke", "keu"]
    for w in words:
        a = saka.latin_to_aksara(w)
        print(f"{w} -> {a}")

if __name__ == "__main__":
    test_sunda_transliteration()
