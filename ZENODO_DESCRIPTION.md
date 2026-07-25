# Saka-NLP v0.3.0

[![PyPI version](https://img.shields.io/pypi/v/saka-nlp.svg)](https://pypi.org/project/saka-nlp/)
[![Documentation](https://img.shields.io/badge/docs-live-brightgreen)](http://saka-nlp.netlify.app/)
[![Colab](https://img.shields.io/badge/Colab-Playground-orange)](https://colab.research.google.com/drive/1MJ6fwJruR6B-UVT1sqKyqWXukjGe2UCH?usp=sharing)
[![Apify Actor](https://img.shields.io/badge/Apify-Actor-blue)](https://apify.com/ikhwan_fathulloh/saka-nlp-actor)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP/blob/main/LICENSE)

**Saka** (Bahasa Jawa/Bahasa Sunda: *Pilar*) adalah kerangka arsitektural modern untuk pemrosesan bahasa Indonesia dan daerah, dibangun dengan prinsip desain asinkron, modular, dan cerdas.

---

## Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| **Pemrosesan Asinkron** | Mendukung operasi non-blokir untuk memproses dataset berskala besar secara efisien. |
| **Optimasi Performa** | Caching LRU pada `normalize()`, `analyze()`, dan `get_stopwords()` untuk mempercepat eksekusi berulang. |
| **Desain Modular** | Komponen plug-and-play untuk integrasi mudah dengan aplikasi lain. |
| **Penganalisis Morfologi** | Analisis afiks Bahasa Indonesia dan daerah dengan *Restrukturisasi Morfofonemik*. |
| **KBBI Langsung** | Ekstraksi arti kata real-time dari kamus resmi kbbi.web.id. |
| **Stopwords Hibrida** | Bahasa Indonesia, Inggris, Sunda, Jawa, Bali, Minangkabau, Batak (Toba/Karo/Mandailing), dan bahasa gaul Jakarta Selatan. |
| **Leksikon Regional** | Kamus kata yang telah divalidasi untuk bahasa daerah. |
| **Transliterasi Aksara Regional** | Konversi Latin ↔ Aksara Sunda (Ngalagena), Jawa (Nglegena), Bali (Wreastra). |
| **AI Agentik** | Alat untuk mengorkestrasi prompt LLM, multi-agent, dan tool calling. |
| **Saka-Eval** | Suite benchmark asinkron untuk evaluasi model NLP Bahasa Indonesia. |
| **Penanganan Kata Majemuk Dinamis** | Pisahkan kata majemuk Bahasa Indonesia secara otomatis. |
| **Apify Actor** | Jalankan Saka di cloud untuk otomatisasi scraping dan pemrosesan teks. |

---

## Changelog v0.3.0

### Peningkatan Normalisasi & Bahasa Daerah
- **Prioritas Dictionary**: Memperbaiki urutan penggabungan dictionary agar dictionary bahasa daerah yang lebih baik (Minang, Bali, Sunda, Batak) tidak ditimpa secara keliru oleh entri yang lebih pendek dari bahasa lain.
- **Konflik Slang vs Partikel**: Mengatasi tabrakan kata slang dengan partikel bahasa daerah (seperti "ka" dan "teh") dengan menghapusnya dari slang base sebelum penggabungan regional.
- **Penyesuaian Kosakata**:
  - **Sunda**: Menambahkan kata dasar seperti "abdi", "nuju", "ka", dan "bumi" ("rumah"). Menghapus "bumi" dari daftar kata yang dilindungi agar bisa dipetakan.
  - **Jawa**: Memperbaiki arti "bocah" menjadi "anak" dan menambahkan "sopo", "arep", "tuku", "iki".
  - **Bali**: Menambahkan "lakar" dan "jukut" (menjadi "sayur").
  - **Minang**: Memastikan "jo" tetap "dengan" dan "rancak" menjadi "bagus".
- **Format Otomatis**: Normalizer kini secara cerdas mempertahankan huruf kapital (termasuk huruf kapital penuh dan huruf awal kapital) serta merapikan spasi sebelum tanda baca (, . ! ? : ;).

---

## Changelog v0.2.7

### Perbaikan
- **KBBI Scraper**: Perbaikan type hint parameter `cookies` dari `Dict[str, str] = None` menjadi `Optional[Dict[str, str]]` untuk menyesuaikan dengan PEP 484 dan menghindari linter error ([kbbi_scraper.py](https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP/blob/v0.2.7/saka/plugins/kbbi_scraper.py)).

### Peningkatan Performa
- **Caching LRU**: Menambahkan decorator `@lru_cache(maxsize=10000)` pada `normalize()` di `saka/core/normalizer.py` untuk menghindari pemrosesan normalisasi berulang pada teks yang sama ([normalizer.py](https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP/blob/v0.2.7/saka/core/normalizer.py)).
- **Stopwords Caching**: Memperbaiki implementasi caching pada `get_stopwords()` dan menambah cache internal untuk stopwords Bahasa Indonesia agar tidak dibaca berulang dari file ([stopwords.py](https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP/blob/v0.2.7/saka/dict/stopwords.py)).

### Dokumentasi
- **README**: Mengurangi penggunaan emoji berlebih, memperjelas deskripsi fitur, menyelaraskan struktur antara [README.md](https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP/blob/v0.2.7/README.md) (Bahasa Indonesia) dan [README_EN.md](https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP/blob/v0.2.7/README_EN.md) (Bahasa Inggris), dan memperbaiki contoh kode.
- **Dokumentasi HTML**: Memperbarui versi di [index.html](https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP/blob/v0.2.7/index.html) dan [docs.html](https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP/blob/v0.2.7/docs.html).

---

## Instalasi

Membutuhkan **Python 3.8+**.

```bash
# Via PyPI (Direkomendasikan)
pip install saka-nlp

# Via Source (Pengembangan)
git clone https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP.git
cd Saka-NLP
pip install -e .
```

---

## Contoh Penggunaan Cepat

```python
import saka

# Tokenisasi & Normalisasi
text = "Belajar NLP di era 5G, seru banget!"
tokens = saka.tokenize(text)
normalized = saka.normalize(text)

# Analisis Morfologi
analysis = saka.analyze("berlari-lari")

# Ambil Stopwords
stopwords_id = saka.get_stopwords("id")
stopwords_batak = saka.get_stopwords("batak")

# Query KBBI
try:
    kbbi_result = saka.query_kbbi("pilar")
    print(kbbi_result)
except Exception as e:
    print(e)
```

---

## Sitasi

Jika Anda menggunakan Saka-NLP dalam penelitian atau aplikasi Anda, silakan sitasi dengan format berikut:

### BibTeX
```bibtex
@software{saka_nlp_2026_21418577,
  author       = {Fathulloh, Muhammad Ikhwan},
  title        = {{Saka-NLP: Indonesian Language Processing with Prompting and Agentic AI Support}},
  month        = jul,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {0.3.0},
  doi          = {10.5281/zenodo.21418577},
  url          = {https://doi.org/10.5281/zenodo.21418577}
}
```

### APA
Fathulloh, M. I. (2026). *Saka-NLP: Indonesian Language Processing with Prompting and Agentic AI Support* (Version 0.3.0) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.21418577
