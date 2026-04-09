import saka
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

def main():
    logging.info("=== Saka-NLP Javanese Plugin Examples ===\n")

    # 1. Dictionary Lookup (Sastra API + Local Dict Fallback)
    word = "sugeng"
    logging.info(f"🔍 Mencari arti kata Jawa: '{word}'")
    result = saka.query_sastra(word)
    
    if result.get("status") == "found":
        logging.info(f"Ditemukan {len(result['definitions'])} definisi:")
        for idx, def_obj in enumerate(result["definitions"], 1):
            logging.info(f" {idx}. {def_obj['arti']} (Info: {def_obj.get('keterangan', '-')})")
    else:
        logging.info("Kata tidak ditemukan dalam Leksikon Jawa.")
    
    logging.info("\n" + "="*40 + "\n")

    # 2. Transliteration (Latin to Aksara Jawa)
    latin_text = "hanacaraka datasawala padhajayanya magabathanga"
    logging.info(f"✍️ Latin: {latin_text}")
    aksara = saka.latin_to_aksara_jawa(latin_text)
    logging.info(f"📖 Aksara Jawa: {aksara}")
    
    logging.info("\n" + "="*40 + "\n")

    # 3. Transliteration (Aksara Jawa to Latin)
    recovered_latin = saka.aksara_jawa_to_latin(aksara)
    logging.info(f"🔄 Aksara -> Latin: {recovered_latin}")

if __name__ == "__main__":
    main()
