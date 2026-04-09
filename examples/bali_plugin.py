import saka

def demo_bali_features():
    print("--- Saka-NLP: Balinese Language Support Demo ---")
    
    # 1. Morphological Analysis with Balinese early stopping
    # 'rahajeng' should be recognized as a Balinese root
    word = "rahajeng"
    print(f"\nAnalyzing word: '{word}'")
    analysis = saka.analyze(word)
    print(f"Result: {analysis}")
    if 'bali' in analysis.get('regional_matches', []):
        print("Success: 'bali' found in regional matches!")

    # 2. Balinese Stopwords
    print("\nRetrieving Balinese stopwords...")
    bali_stops = saka.get_stopwords(lang="bali")
    print(f"Total Balinese stopwords: {len(bali_stops)}")
    print(f"Example stopwords: {list(bali_stops)[:5]}")
    
    # 3. BASAbali Dictionary Lookup (Requires internet if not in seed dict)
    word_to_query = "tiang"
    print(f"\nQuerying BASAbali for: '{word_to_query}'")
    res = saka.query_basabali(word_to_query)
    if res['status'] == 'found':
        print(f"Source: {res['source']}")
        print(f"Meaning: {res['definitions'][0]}")
    else:
        print("Word not found in BASAbali.")

    # Latin <-> Aksara Bali Transliteration (Latin -> Aksara)
    latin_text = "rahajeng, bali 2026."
    print(f"\nTransliterating '{latin_text}' to Aksara Bali...")
    aksara = saka.latin_to_aksara_bali(latin_text)
    try:
        print(f"Output: {aksara}") # Should be ᬭᬳᬚ᭄ᬜ᭞ ᬩᬮᬶ ᭒᭐᭒᭖᭟
    except UnicodeEncodeError:
        print(f"Output (Hex): {[hex(ord(c)) for c in aksara]}")
    
    # Inverse
    print(f"Inverse back to Latin: {saka.aksara_bali_to_latin(aksara)}")

if __name__ == "__main__":
    demo_bali_features()
