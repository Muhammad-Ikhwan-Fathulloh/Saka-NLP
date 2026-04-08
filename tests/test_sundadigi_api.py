import os
import sys

# Add the current directory to sys.path
sys.path.append(r"d:\Saka-NLP")

import saka

def test_sundadigi_api():
    word = "wilujeng"
    print(f"Querying SundaDigi for: {word}")
    try:
        result = saka.query_sundadigi(word)
        print(f"Status: {result['status']}")
        if result['status'] == 'found':
            print(f"Definitions found: {len(result['definitions'])}")
            for d in result['definitions']:
                print(f"- {d}")
        else:
            print(f"Word not found. Full result: {result}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_sundadigi_api()
