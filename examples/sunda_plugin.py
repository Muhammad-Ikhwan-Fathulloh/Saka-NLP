"""
Plugin Example: Aksara Sunda Transliteration
Demonstrates how to use plugins integrated in the framework.
"""

from saka.plugins.sunda.transliterate import transliterate
from saka.plugins.sunda.sundadigi_scraper import query_sundadigi

def main():
    print("=== 1. Transliterasi Aksara Sunda ===")
    
    # Karakter Vokal Mandiri Aksara Sunda
    aksara_text = "ᮃᮄᮅᮆᮇᮈᮉ" 
    
    latin_text = transliterate(aksara_text)
    
    print("Teks Aksara (Raw UTF-8):", aksara_text.encode('utf-8'))
    print("Teks Latin Output:", latin_text)
    print()

    print("=== 2. Dictionary Search (SundaDigi) ===")
    word = "dahar"
    print(f"Mengambil definisi bahasa Sunda untuk kata '{word}'...")
    try:
        sd_result = query_sundadigi(word)
        if sd_result.get("status") == "found":
            print("Definisi ditemukan:")
            for index, arti in enumerate(sd_result.get("definitions", []), 1):
                safe_arti = arti.encode('ascii', 'ignore').decode()
                print(f"  {index}. {safe_arti}")
        else:
            print("Kata tidak ditemukan atau scraper gagal diekstrak parameternya dari SundaDigi.")
    except Exception as e:
        print(f"Gagal memanggil portal SundaDigi: {e}")

    
if __name__ == "__main__":
    main()
