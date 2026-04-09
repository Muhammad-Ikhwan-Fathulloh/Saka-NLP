import saka
import logging
import json

logging.basicConfig(level=logging.INFO, format="%(message)s")

def main():
    logging.info("=== Saka-NLP Advanced Morphology Examples ===\n")
    
    words = [
        "mempertanggungjawabkan",  # Kata Majemuk Serangkai standard
        "menyebarluaskan",         # Morphophonemic Fusion (meny + s)
        "dipikanyaah",             # Validasi Regional (Sunda)
        "ngabageakeun",            # Validasi Regional (Sunda) - Fallback
        "mencampurtangani",        # Kata Majemuk dengan peleburan & suffix double
        "ketidakhadiran"           # Senyawa Negasi
    ]
    
    for word in words:
        logging.info(f"Kata Uji: {word}")
        analysis = saka.analyze(word)
        logging.info(f" Akar Kata: {analysis['root']}")
        logging.info(f" Prefiks  : {analysis['prefixes']}")
        logging.info(f" Sufiks   : {analysis['suffixes']}")
        if analysis['regional_matches']:
            logging.info(f" Regional : {analysis['regional_matches']}")
        logging.info("-" * 40)

if __name__ == "__main__":
    main()
