import os
import sys

# Add the current directory to sys.path
sys.path.append(r"d:\Saka-NLP")

import saka

def test_kbbi_web_id():
    word = "belajar"
    print(f"Querying KBBI for: {word}")
    result = saka.query_kbbi(word)
    print(f"Status: {result['status']}")
    if result['status'] == 'found':
        print(f"Definitions found: {len(result['definitions'])}")
        for d in result['definitions']:
            print(f"- {d}")
    else:
        print("Word not found.")

if __name__ == "__main__":
    test_kbbi_web_id()
