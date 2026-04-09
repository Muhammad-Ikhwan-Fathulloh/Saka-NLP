import saka
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

def main():
    logging.info("=== Saka-NLP Stopwords Framework ===\n")
    
    # 1. Fetching specific Javanese Stopwords
    jawa_stops = saka.get_stopwords(lang="jawa")
    logging.info(f"📚 Total Stopwords Jawa : {len(jawa_stops)}")
    logging.info(f"   Contoh: 'kepiye' ada di stopwords Jawa? {'kepiye' in jawa_stops}")
    logging.info(f"   Contoh: 'saha' ada di stopwords Jawa? {'saha' in jawa_stops}") # Saha is Sundanese
    logging.info("-" * 40)

    # 2. Fetching specific Sundanese Stopwords
    sunda_stops = saka.get_stopwords(lang="sunda")
    logging.info(f"📚 Total Stopwords Sunda: {len(sunda_stops)}")
    logging.info(f"   Contoh: 'saha' ada di stopwords Sunda? {'saha' in sunda_stops}")
    logging.info("-" * 40)

    # 3. Fetching combined Stopwords (Default)
    all_stops = saka.get_stopwords(lang="all")
    logging.info(f"📚 Total Stopwords Gabungan (Indo+Sunda+Jawa): {len(all_stops)}")
    logging.info(f"   Contoh: 'adalah' ada? {'adalah' in all_stops}")
    logging.info(f"   Contoh: 'kepiye' ada? {'kepiye' in all_stops}")
    logging.info(f"   Contoh: 'saha' ada? {'saha' in all_stops}")

if __name__ == "__main__":
    main()
