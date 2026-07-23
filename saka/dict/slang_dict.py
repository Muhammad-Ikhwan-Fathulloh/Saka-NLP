import json
import os
import re
import glob
from typing import Dict, Optional, Set

def _build_indonesian_wordset(current_dir: str) -> Set[str]:
    """
    Build a comprehensive set of known Indonesian words by:
    1. Collecting all 'arti' values from clean regional dictionaries (bali, minang, sunda)
    2. Including a base set of common Indonesian vocabulary
    3. Including all values from slang.json
    """
    indo_words = {
        # Core function words, pronouns, and particles
        "dan", "atau", "tapi", "tetapi", "karena", "jika", "kalau", "maka",
        "yang", "ini", "itu", "di", "ke", "dari", "untuk", "dengan",
        "pada", "oleh", "akan", "sudah", "belum", "sedang", "telah",
        "tidak", "bukan", "jangan", "sangat", "lebih", "paling", "juga",
        "masih", "lagi", "saja", "semua", "setiap", "beberapa", "banyak",
        "sedikit", "saya", "aku", "kamu", "dia", "kita", "kami", "mereka",
        "apa", "siapa", "mana", "kapan", "mengapa", "bagaimana", "berapa",
        "ya", "baik", "sama", "lain", "antara", "setelah", "sebelum",
        "ada", "punya", "jadi", "seperti", "bisa", "harus", "boleh",
        "mau", "makan", "minum", "tidur", "pergi", "datang", "pulang",
        "beli", "jual", "tulis", "baca", "bicara", "dengar", "lihat",
        "rumah", "air", "tanah", "orang", "anak", "ibu", "ayah",
        "kakak", "adik", "teman", "besar", "kecil", "tinggi", "rendah",
        "hari", "bulan", "tahun", "pagi", "siang", "sore", "malam",
        "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh",
        "delapan", "sembilan", "sepuluh", "ratus", "ribu", "juta",
        "baru", "lama", "tua", "muda", "bagus", "jelek", "cepat", "lambat",
        "dekat", "jauh", "hitam", "putih", "merah", "biru", "hijau", "kuning",
        "umum", "kerja", "cari", "dapat", "tahu", "pikir", "rasa",
        "suka", "cinta", "benci", "takut", "bawa", "kasih", "buat",
        "main", "ambil", "masuk", "keluar", "naik", "turun", "jalan",
        "kau", "engkau", "kamu", "mu", "ku", "nya",
        "berapa", "kemana", "dimana", "kenapa", "mengapa",
        "sudah", "adalah", "merupakan", "menjadi", "sebagai",
        "kepada", "terhadap", "menuju", "tentang", "mengenai",
        "beserta", "bersama", "sendiri", "sebuah", "seorang",
        "budak", "pelayan", "abdi", "hamba",
        "rame", "ramai", "cantik", "indah", "bagus",
        "rumput", "sayur", "sayuran", "daging",
    }
    
    # Collect arti values from clean regional dicts (NOT jawa - too noisy)
    clean_dicts = ['bali_dict.json', 'minang_dict.json', 'sunda_dict.json']
    for dict_file in clean_dicts:
        dict_path = os.path.join(current_dir, dict_file)
        try:
            with open(dict_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for info in data.values():
                    if isinstance(info, dict) and 'arti' in info and info['arti']:
                        raw = info['arti']
                        parts = re.split(r'[;,]', raw)
                        for part in parts:
                            word = part.strip().lower()
                            if word and re.match(r'^[a-z\-]+$', word) and len(word) >= 2:
                                indo_words.add(word)
        except Exception:
            pass
    
    # Also collect all values from slang.json
    slang_path = os.path.join(current_dir, 'slang.json')
    try:
        with open(slang_path, 'r', encoding='utf-8') as f:
            slang_data = json.load(f)
            for value in slang_data.values():
                for word in value.lower().split():
                    clean = word.strip('.,;:!?()[]')
                    if clean and re.match(r'^[a-z\-]+$', clean) and len(clean) >= 2:
                        indo_words.add(clean)
    except Exception:
        pass
    
    return indo_words


def _clean_arti(raw_arti: str, indo_words: Set[str]) -> Optional[str]:
    """
    Cleans a raw 'arti' (meaning) string from regional dictionaries
    and extracts only the clean Indonesian translation word(s).
    """
    if not raw_arti:
        return None
    
    # Step 1: Take the first meaning (before ';')
    arti = raw_arti.split(';')[0].strip()
    
    # Step 2: Take the first part before ',' to get the primary translation
    arti = arti.split(',')[0].strip()
    
    # Step 3: Remove leading numbering like "1 ", "2 "
    arti = re.sub(r'^\d+\s+', '', arti).strip()
    
    # Step 4: Remove content in parentheses
    arti = re.sub(r'\([^)]*\)', '', arti).strip()
    
    # Step 5: Remove common dictionary abbreviation markers
    arti = re.sub(r'\b\w{1,4}\.\s*', '', arti).strip()
    
    # Step 6: Remove trailing/leading punctuation
    arti = arti.strip('.,;:!? -')
    
    # Step 7: Skip if the result contains special regional characters
    if re.search(r'[êéèëôóòöûúùüâáàäîíìï]', arti):
        return None
    
    # Step 8: Skip if the result is too long (more than 3 words)
    words = arti.split()
    if len(words) > 3:
        return None
    
    # Step 9: Skip if empty or single character
    if not arti or len(arti) < 2:
        return None
    
    result = arti.lower()
    
    # Step 10: Only alphabetic characters allowed
    if not re.match(r'^[a-z\s\-]+$', result):
        return None
    
    # Step 11: Verify ALL words in the result are known Indonesian words
    result_words = result.split()
    if not all(w in indo_words for w in result_words):
        return None
    
    return result


# Words that are definitely standard Indonesian and should NEVER be replaced
# These are common words that might also exist in regional dictionaries
# with Javanese/regional translations (the reverse of what we want)
_PROTECTED_INDONESIAN = {
    "makan", "minum", "tidur", "pergi", "datang", "pulang",
    "beli", "jual", "tulis", "baca", "bicara", "dengar", "lihat",
    "ambil", "bawa", "kasih", "buat", "kerja", "main", "cari",
    "dapat", "tahu", "pikir", "rasa", "suka", "cinta", "benci",
    "takut", "mau", "bisa", "harus", "boleh", "masuk", "keluar",
    "naik", "turun", "jalan", "lari", "duduk", "berdiri", "bangun",
    "kirim", "terima", "bayar", "tunggu", "panggil", "jawab",
    "tanya", "tolong", "bantu", "simpan", "buang", "cuci", "masak",
    "potong", "tarik", "dorong", "angkat", "taruh", "pakai", "lepas",
    "buka", "tutup", "mulai", "selesai", "coba", "ingat", "lupa",
    "rumah", "air", "tanah", "api", "angin", "hujan", "awan", "langit",
    "gunung", "laut", "sungai", "pohon", "bunga",
    "buah", "daun", "batu", "pasir", "kayu", "besi", "emas",
    "orang", "anak", "ibu", "ayah", "adik", "teman", "guru",
    "kepala", "tangan", "kaki", "mata", "telinga", "hidung", "mulut",
    "gigi", "rambut", "kulit", "darah", "tulang", "hati", "perut",
    "makanan", "minuman", "pakaian", "sepatu", "buku", "meja", "kursi",
    "pintu", "jendela", "dinding", "lantai", "atap",
    "besar", "kecil", "tinggi", "rendah", "panjang", "pendek", "lebar",
    "panas", "dingin", "basah", "kering", "baru", "lama", "tua", "muda",
    "bagus", "jelek", "cantik", "kaya", "miskin", "pintar",
    "senang", "sedih", "marah", "tenang", "cepat", "lambat",
    "dekat", "jauh", "gelap", "terang", "hitam", "putih",
    "dan", "atau", "tapi", "tetapi", "karena", "jika", "kalau",
    "yang", "ini", "itu", "di", "ke", "dari", "untuk", "dengan",
    "pada", "oleh", "akan", "sudah", "belum", "sedang", "telah",
    "tidak", "bukan", "jangan", "sangat", "lebih", "paling", "juga",
    "masih", "lagi", "saja", "semua", "banyak", "sedikit",
    "saya", "aku", "kamu", "dia", "kita", "kami", "mereka",
    "apa", "siapa", "mana", "kapan", "mengapa", "bagaimana", "berapa",
    "ya", "baik", "sama", "lain", "antara", "setelah", "sebelum",
    "umum", "ada", "punya", "jadi", "seperti",
    "hari", "minggu", "bulan", "tahun", "pagi", "siang", "sore", "malam",
}


def get_slang_dict() -> Dict[str, str]:
    """
    Returns a dictionary of common Indonesian slang words mapped to standard words,
    including words from available regional dictionaries.
    """
    current_dir = os.path.dirname(__file__)
    json_path = os.path.join(current_dir, 'slang.json')
    slang_dict = {}
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            slang_dict = json.load(f)
            # Remove problematic slang words before regional dicts load
            if 'teh' in slang_dict and slang_dict['teh'] == 'kakak perempuan':
                del slang_dict['teh']
            if 'ka' in slang_dict and slang_dict['ka'] == 'kakak':
                del slang_dict['ka']
    except FileNotFoundError:
        print(f"Warning: Slang dictionary not found at {json_path}. Normalization might not work.")
    
    # Build comprehensive Indonesian word set for validation
    indo_words = _build_indonesian_wordset(current_dir)
    
    # Load regional dictionaries and integrate them
    # Priority: minang, bali, sunda, batak first, jawa last. 
    # Do NOT overwrite existing words to prevent noisy dicts from destroying good translations.
    regional_files = [
        'minang_dict.json',
        'bali_dict.json',
        'sunda_dict.json',
        'batak_dict.json',
        'jawa_dict.json'
    ]
    
    for dict_file in regional_files:
        reg_file = os.path.join(current_dir, dict_file)
        if not os.path.exists(reg_file):
            continue
            
        try:
            with open(reg_file, 'r', encoding='utf-8') as f:
                reg_data = json.load(f)
                for word, info in reg_data.items():
                    if isinstance(info, dict) and 'arti' in info:
                        # Only protect core Indonesian words from being overwritten
                        if word.lower() in _PROTECTED_INDONESIAN:
                            continue
                        cleaned = _clean_arti(info['arti'], indo_words)
                        if cleaned:
                            # We keep the first translation we find (highest priority dict first)
                            # Or if it's already in slang.json, we don't overwrite it either unless
                            # we specifically want regional to win. Let's let slang.json win
                            # for common internet slang, but for 'teh' we might have an issue.
                            # For now, do NOT overwrite.
                            if word not in slang_dict:
                                slang_dict[word] = cleaned
        except Exception as e:
            print(f"Warning: Failed to load regional dictionary {reg_file}: {e}")
            
    return slang_dict
