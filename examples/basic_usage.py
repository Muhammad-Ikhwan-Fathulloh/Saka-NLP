"""
Basic Usage Example for Saka-NLP
This file demonstrates how to use the core features of the Saka-NLP framework synchronously.
"""

import saka

def main():
    print("=== 1. Tokenization ===")
    text = "Belajar NLP sambil rebahan di era konektivitas 5G."
    tokens = saka.tokenize(text)
    print("Teks Asli:", text)
    print("Tokens:", tokens)
    print()

    print("=== 2. Normalization (Slang) ===")
    slang_text = "gw lg ngapain ya klo kyk gini"
    normalized = saka.normalize(slang_text)
    print("Slang:", slang_text)
    print("Baku:", normalized)
    print()

    print("=== 3. Morphological Analysis ===")
    word = "mempertanggungjawabkan"
    analysis = saka.analyze(word)
    print("Kata:", word)
    print("Root (Kata Dasar):", analysis["root"])
    print("Prefiks (Awalan):", analysis["prefixes"])
    print("Sufiks (Akhiran):", analysis["suffixes"])
    print()

    print("=== 4. KBBI Query ===")
    kbbi_query = "belajar"
    print(f"Mengambil definisi KBBI untuk kata '{kbbi_query}'...")
    try:
        kbbi_result = saka.query_kbbi(kbbi_query)
        if kbbi_result.get("status") == "found":
            print("Definisi ditemukan:")
            for index, arti in enumerate(kbbi_result.get("definitions", []), 1):
                safe_arti = arti.encode('ascii', 'ignore').decode()
                print(f"  {index}. {safe_arti}")
        else:
            print("Kata tidak ditemukan di KBBI.")
    except Exception as e:
        print(f"Gagal mengambil definisi dari KBBI: {e}")
    print()

    print("=== 5. Stopwords ===")
    stopwords = saka.get_stopwords()
    print("Jumlah Stopwords dalam dataset:", len(stopwords))
    sample_words = ["yang", "di", "nlp", "teknologi", "karena"]
    for w in sample_words:
        print(f"Apakah '{w}' termasuk stopword? {'Ya' if w in stopwords else 'Tidak'}")


if __name__ == "__main__":
    main()
