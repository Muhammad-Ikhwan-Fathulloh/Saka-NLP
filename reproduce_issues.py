import os
import sys

# Add the current directory to sys.path so we can import saka
# Using the corpus path from metadata: d:\Saka-NLP
sys.path.append(r"d:\Saka-NLP")

import saka

def test_slang():
    text = "klo gimana gw"
    normalized = saka.normalize(text)
    print(f"Original: {text}")
    print(f"Normalized: {normalized}")
    if normalized == "kalau bagaimana saya":
        print("Slang test PASSED")
    else:
        print("Slang test FAILED: normalized output mismatch")

def test_stopwords():
    sw = saka.get_stopwords()
    print(f"Stopwords count: {len(sw)}")
    if len(sw) > 0:
        print("Stopwords test PASSED")
    else:
        print("Stopwords test FAILED: count is 0")

if __name__ == "__main__":
    test_slang()
    test_stopwords()
