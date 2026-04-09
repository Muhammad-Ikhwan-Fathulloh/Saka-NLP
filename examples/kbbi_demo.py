import saka
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

def main():
    logging.info("=== Saka-NLP KBBI Scraper Demo ===\n")
    
    # 1. Dictionary Lookup (KBBI Kemdikbud)
    word = "belajar"
    logging.info(f"🔍 Mencari arti kata: '{word}'")
    result = saka.query_kbbi(word)
    
    if result.get("status") == "found":
        logging.info(f"Ditemukan {len(result['definitions'])} definisi:\n")
        for idx, def_text in enumerate(result["definitions"], 1):
            logging.info(f" [{idx}] {def_text}")
    else:
        logging.info("Kata tidak ditemukan dalam KBBI Daring.")

if __name__ == "__main__":
    main()
