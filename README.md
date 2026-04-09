# Saka: The Foundation of Indonesian NLP 🇮🇩

[![PyPI version](https://img.shields.io/pypi/v/saka-nlp.svg)](https://pypi.org/project/saka-nlp/)
[![Documentation](https://img.shields.io/badge/docs-live-brightgreen)](http://saka-nlp.netlify.app/)
[![Colab](https://img.shields.io/badge/Colab-Playground-orange)](https://colab.research.google.com/drive/1MJ6fwJruR6B-UVT1sqKyqWXukjGe2UCH?usp=sharing)

Secara filosofis, **Saka** (dalam bahasa Jawa/Sunda) berarti "tiang penyangga" atau "pilar". **Saka-NLP** dibangun untuk menjadi sebuah *architectural framework* modern yang solid bagi pemrosesan teks bahasa Indonesia dan daerah.

Saka-NLP mendukung *asynchronous processing*, memiliki komponen yang dijaga terpisah secara modular (*plug-and-play*), serta menggunakan fungsi heuristik dan integrasi banyak sumber data terpercaya (seperti leksikon bahasa gaul, integrasi stopword, hingga ekstraksi KBBI resmi secara langsung).

---

### 🌐 Links
*   **Website Resmi**: [saka-nlp.netlify.app](http://saka-nlp.netlify.app/)
*   **Google Colab Playground**: [Coba Sekarang di Colab](https://colab.research.google.com/drive/1MJ6fwJruR6B-UVT1sqKyqWXukjGe2UCH?usp=sharing)
*   **PyPI Package**: [saka-nlp on PyPI](https://pypi.org/project/saka-nlp/)

---

## ✨ Fitur Unggulan

*   **Asynchronous Processing**: Dilengkapi method pendamping `async_*` (contoh: `async_tokenize`) menggunakan `asyncio` untuk pemrosesan dataset besar secara efisien tanpa *blocking*.
*   **Plug-and-Play Components**: Fleksibel dalam memilih mesin stemming, tokenisasi, atau mengintegrasikan plugin pihak ketiga.
*   **Heuristic Morphology Analyzer**: Mendeteksi susunan pola awalan dan akhiran menggunakan aturan tata bahasa Indonesia yang dibekali dengan **Early Stopping Validation** ke dalam leksikon bahasa daerah dan pemulihan leburan huruf (Morphophonemic).
*   **Live KBBI Scraper**: Ekstraksi arti kata langsung mendompleng ke *Kamus Besar Bahasa Indonesia Daring* dari Kemendikbudristekdikti.
*   **Agnostic Script Support**: Termasuk dukungan untuk skrip bahasa daerah seperti Transliterasi **Aksara Sunda**, **Aksara Jawa**, dan **Aksara Bali** (Hanacaraka).

---

## 🚀 Panduan Instalasi

Library `saka-nlp` menggunakan `pyproject.toml` dengan *bundler* `setuptools` terbaru sehingga proses distribusinya sangat mudah. 

Pastikan versi Python Anda adalah **Python 3.8 atau lebih baru**.

### Opsi 1: Instalasi Via PyPI (Direkomendasikan)
Untuk menggunakan rilis stabil Saka-NLP, instal langsung melalui PyPI:
```bash
pip install saka-nlp
```

### Opsi 2: Instalasi dari Source Code (Versi Deployment/Development)
Gunakan langkah ini jika Anda ingin turut berkontribusi, memodifikasi script mesin Saka-NLP, ataupun menggunakan *snapshot* git yang belum dirilis:
```bash
# 1. Clone repository
git clone https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP.git
cd Saka-NLP

# 2. Instal library beserta seluruh dependency-nya
pip install -e .
```

---

## 📖 Panduan Penggunaan Modul Inti

Saka-NLP didesain agar kode Python Anda menjadi bersih. Cukup lakukan satu baris `import saka` untuk mengeluarkan beragam utilitas tanpa membuang *namespace*.

### 0. Cek Versi
```python
import saka

print(saka.__version__)
# Output: 0.1.9
```

### 1. Tokenisasi Cerdas 
```python
import saka

text = "Belajar sambil beramal di era konektivitas."
tokens = saka.tokenize(text)
print(tokens)
# Output: ['Belajar', 'sambil', 'beramal', 'di', 'era', 'konektivitas']
```

### 2. Normalisasi Bahasa Gaul (Slang)
Menggunakan *slang lexicon* yang kuat dan lengkap dari data sosial media.
```python
import saka

normalized = saka.normalize("klo gimana gw")
print(normalized)
# Output: 'kalau bagaimana saya'
```

### 3. Analisis Morfologi Teks
Saka dilengkapi dengan *Heuristic Morphology Analyzer* mutakhir. Modul ini bukan hanya sekedar memotong imbuhan secara serakah layaknya *Stemming* pada umumnya. Saka mampu merekonstruksi peleburan huruf (*Morphophonemic Restructuring*) dari imbuhan, menyelesaikan akar bentuk *Kata Majemuk Serangkai*, bahkan tervalidasi secara hibrida dengan pangkalan data daerah.

```python
import saka

# Menangani kata majemuk & afiks luluh
print(saka.analyze("menyebarluaskan"))
# Output: {'root': 'sebar luas', 'prefixes': ['meny'], 'suffixes': ['kan'], 'type': 'unknown', 'regional_matches': []}

# Memanfaatkan validasi kamus daerah (*Early Stopping*)
print(saka.analyze("dipikanyaah"))
# Output: {'root': 'nyaah', 'prefixes': ['dipika'], 'suffixes': [], 'type': 'regional', 'regional_matches': ['sunda']}
```

### 4. Live Integrasi Pencarian KBBI
Saka menggunakan library pendukung (`requests` & `bs4`) untuk mengurai jawaban dari situs [kbbi.web.id](https://kbbi.web.id/). Ini wajib menggunakan akses jaringan internet.

```python
import saka

kbbi_result = saka.query_kbbi("belajar")

if kbbi_result["status"] == "found":
    for arti in kbbi_result["definitions"]:
        print(f"Arti: {arti}")
else:
    print("Kata tidak terdaftar di KBBI Daring.")

# Output:
# Arti: petunjuk yang diberikan kepada orang supaya diketahui (diturut)
# Arti: ilmu yang dituntut secara tidak sempurna, tidak akan berfaedah
# Arti: berusaha memperoleh kepandaian atau ilmu:
# Arti: berlatih:
# Arti: berubah tingkah laku atau tanggapan yang disebabkan oleh pengalaman
```

### 5. Koleksi Stopwords Nusantara (Hybrid)
Kumpulan Stopwords yang langsung dirender ke dalam object `Set` Python agar latensinya O(1) untuk kebutuhan ML. Mendukung corpus Indonesia (Tala), Sunda, dan Jawa.
```python
import saka

# 1. Mengambil semua stopword (Indonesia, Sunda, Jawa digabung)
all_stops = saka.get_stopwords(lang="all") # "all" adalah parameter default
print(f"Total Stopwords Gabungan: {len(all_stops)}") # Output: 817

# 2. Mengambil stopword khusus bahasa Sunda
sunda_stops = saka.get_stopwords(lang="sunda")
print(f"Apakah 'saha' stopword Sunda? {'saha' in sunda_stops}") # Output: True

# 3. Mengambil stopword khusus Jawa ('jawa') atau Bali ('bali')
jawa_stops = saka.get_stopwords(lang="jawa")
bali_stops = saka.get_stopwords(lang="bali")
```

#### 1. Ekosistem Sunda
Dukungan penuh untuk kamus digital SundaDigi dan transliterasi Aksara Sunda.

```python
import saka

# Kamus Sunda
res = saka.query_sundadigi("wilujeng")
print(res["definitions"]["arti"]) # Output: selamat

# Aksara Sunda
print(saka.latin_to_aksara_sunda("saka")) # Output: ᮞᮊ
```

#### 2. Ekosistem Jawa
Integrasi Leksikon Sastra.org dan mesin transliterasi Hanacaraka (Nglegena).

```python
import saka

# Kamus Jawa
res = saka.query_sastra("sugeng")
print(res["definitions"][0]["arti"]) # Output: selamat

# Aksara Jawa
print(saka.latin_to_aksara_jawa("hanacaraka")) # Output: ꦲꦤꦕꦫꦏ
```

#### 3. Ekosistem Bali
Pemanfaatan BASAbali Wiki dan dukungan penuh Aksara Bali (Wreastra).

```python
import saka

# Kamus Bali
res = saka.query_basabali("rahajeng")
print(res["definitions"][0]["arti"]) # Output: selamat

# Aksara Bali
print(saka.latin_to_aksara_bali("bali 2026.")) 
# Output: ᬩᬮᬶ ᭒᭐᭒᭖᭟
```

---

## 🏛️ Detail Aksara Nusantara

Saka-NLP menggunakan pemetaan standar untuk transliterasi dasar bahasa daerah.

### 1. Aksara Sunda (Ngalagena)
| Latin | Aksara | Latin | Aksara |
| :---- | :----- | :---- | :----- |
| ha    | ᮠ      | na    | ᮔ      |
| ca    | ᮎ      | ra    | ᮛ      |
| ka    | ᮊ      | da    | ᮓ      |
| ta    | ᮒ      | sa    | ᮞ      |
| wa    | ᮝ      | la    | ᮜ      |
| pa    | ᮕ      | ja    | ᮏ      |
| ya    | ᮚ      | nya   | ᮑ      |
| ma    | ᮙ      | ga    | ᮌ      |
| ba    | ᮘ      | nga   | ᮍ      |

### 2. Aksara Jawa (Nglegena)
| Latin | Aksara | Latin | Aksara |
| :---- | :----- | :---- | :----- |
| ha    | ꦲ      | na    | ꦤ      |
| ca    | ꦕ      | ra    | ꦫ      |
| ka    | ꦏ      | da    | ꦢ      |
| ta    | ꦠ      | sa    | ꦱ      |
| wa    | ꦮ      | la    | ꦭ      |
| pa    | ꦥ      | dha   | ꦝ      |
| ja    | ꦗ      | ya    | ꦪ      |
| nya   | ꦚ      | ma    | ꦩ      |
| ga    | ꦒ      | ba    | ꦧ      |
| tha   | ꦛ      | nga   | ꦔ      |

### 3. Aksara Bali (Wreastra)
#### Konsonan (Wreastra)
| Latin | Aksara | Latin | Aksara |
| :---- | :----- | :---- | :----- |
| ha    | ᬳ      | da    | ᬤ      |
| na    | ᬦ      | ta    | ᬢ      |
| ca    | ᬘ      | sa    | ᬲ      |
| ra    | ᬭ      | wa    | ᬯ      |
| ka    | ᬓ      | la    | ᬮ      |
| ma    | ᬫ      | pa    | ᬧ      |
| ga    | ᬕ      | ja    | ᬚ      |
| ba    | ᬩ      | ya    | ᬬ      |
| nga   | ᬗ      | nya   | ᬜ      |

#### Angka Bali
| Angka | Aksara | Angka | Aksara |
| :---- | :----- | :---- | :----- |
| 0     | ᭐      | 5     | ᭕      |
| 1     | ᭑      | 6     | ᭖      |
| 2     | ᭒      | 7     | ᭗      |
| 3     | ᭓      | 8     | ᭘      |
| 4     | ᭔      | 9     | ᭙      |

#### Pangangge Suara (Sandhangan Bali)
| Bunyi   | Aksara | Nama         |
| :------ | :----- | :----------- |
| -i      | ᬶ      | Ulu          |
| -u      | ᬸ      | Suku         |
| -é      | ᬾ      | Taling       |
| -o      | ᭀ      | Taling Detia |
| -e / -ě | ᬺ      | Pepet        |

---

## 🛠️ Penggunaan Melalui Command Line (CLI)

Saka-NLP menyertakan perintah langsung alias di dalam instalasinya. Anda dapat mengakses ini langsung di terminal!

```bash
# Melihat bantuan list CLI
saka --help

# Membedah morfologi kata secara cepat di Shell/CMD Anda
saka --stem "dimakan"

# Melakukan Normalisasi
saka --normalize "ngapain ke kampus klo libur"
```

---

## 🗄️ Referensi & Sumber Data

* **KBBI (Kamus Besar Bahasa Indonesia)**: Data yang dijaring bersumber dari [KBBI Online (kbbi.web.id)](https://kbbi.web.id/).
* **Slang Words**: Memanfaatkan corpus dari [Twitter COVID-19 Sentiment Lexicon](https://github.com/evanmartua34/Twitter-COVID19-Indonesia-Sentiment-Analysis---Lexicon-Based).
* **Ekosistem Sunda**: Menggunakan kamus digital [SundaDigi](https://sundadigi.com/) untuk terjemahan serta [Panduan Aksara Sunda](https://sundadigi.com/panduan) untuk sistem transliterasi dan Wiktionary Appendix.
* **Ekosistem Jawa**: Menyadur secara komprehensif repositori dari [sastra.org](https://www.sastra.org/) baik leksikon kosa kata Jawa maupun sistem validasi Aksara Jawa.
* **Ekosistem Bali**: Integrasi dengan [BASAbali Wiki](https://dictionary.basabali.org/) untuk kamus multi-bahasa dan pemetaan Aksara Bali (Hanacaraka).
* **Stopwords**: Mengadopsi corpus legendaris [Tala Stopwords Dataset](https://github.com/masdevid/ID-Stopwords).

## ❤️ Credits
* **Framework Architect**: [Muhammad Ikhwan Fathulloh](https://github.com/Muhammad-Ikhwan-Fathulloh)
* Lisensi Terbuka di bawah [MIT License](LICENSE). 
