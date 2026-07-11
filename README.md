# Saka: Pemrosesan Bahasa Indonesia dengan Prompting dan Dukungan AI Agentik 🇮🇩 v0.2.6

[**English**](README_EN.md) | [**Bahasa Indonesia**](README.md)

[![PyPI version](https://img.shields.io/pypi/v/saka-nlp.svg)](https://pypi.org/project/saka-nlp/)
[![Documentation](https://img.shields.io/badge/docs-live-brightgreen)](http://saka-nlp.netlify.app/)
[![Colab](https://img.shields.io/badge/Colab-Playground-orange)](https://colab.research.google.com/drive/1MJ6fwJruR6B-UVT1sqKyqWXukjGe2UCH?usp=sharing)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20092640.svg)](https://doi.org/10.5281/zenodo.20092640)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Saka** (Bahasa Jawa/Bahasa Sunda: *Pilar*) adalah kerangka arsitektural modern untuk pemrosesan bahasa Indonesia dan daerah, dibangun dengan prinsip desain asinkron, modular, dan cerdas.

---

## 📌 Daftar Isi
- [Saka: Pemrosesan Bahasa Indonesia dengan Prompting dan Dukungan AI Agentik 🇮🇩 v0.2.6](#saka-pemrosesan-bahasa-indonesia-dengan-prompting-dan-dukungan-ai-agentik-v026)
  - [📌 Daftar Isi](#-daftar-isi)
  - [✨ Fitur Utama](#-fitur-utama)
  - [🚀 Instalasi](#-instalasi)
  - [📖 Penggunaan Dasar](#-penggunaan-dasar)
  - [🤖 AI Agentik & Prompting](#-ai-agentik--prompting)
  - [📊 Benchmark Saka-Eval](#-benchmark-saka-eval)
  - [🔗 Penanganan Kata Majemuk Dinamis](#-penanganan-kata-majemuk-dinamis)
  - [🌏 Ekosistem Regional](#-ekosistem-regional)
  - [🛠️ CLI & Sitasi](#-cli--sitasi)
  - [🗄️ Sumber & Kredit](#-sumber--kredit)
  - [❤️ Dukungan](#-dukungan)

---

## ✨ Fitur Utama

| Fitur                   | Deskripsi                                                         |
| ------------------------- | ------------------------------------------------------------------- |
| ⚡ **Pemrosesan Asinkron**    | Pemrosesan non-blokir untuk dataset berskala besar.                   |
| 🧩 **Desain Modular**      | Komponen plug-and-play untuk integrasi yang mudah.                      |
| 🧠 **Penganalisis Morfologi** | Analisis afiks hibrida dengan *Restrukturisasi Morfofonemik*.          |
| 📖 **KBBI Langsung**           | Ekstraksi arti kata dari kamus resmi Bahasa Indonesia (KBBI).      |
|  **Stopwords Hibrida** | Bahasa Indonesia, Inggris, Sunda, Jawa, Bali, Minangkabau, **Batak** (Toba · Karo · Mandailing), dan bahasa gaul Jakarta Selatan |
| 🗺️ **Leksikon Regional** | Kamus kata yang tervalidasi: Sunda, Jawa, Bali, Minang, **Batak** |
| 🔠 **Aksara Regional**    | Transliterasi Bahasa Sunda, Jawa, dan Bali (Hanacaraka).     |
| 🤖 **AI Agentik**          | Orkestrasi prompt LLM, manajemen Multi-Agent, dan Pemanggilan Alat. |
| 📊 **Saka-Eval**           | Benchmark asinkron untuk model NLP Bahasa Indonesia (Sentimen / NER) |
| 🔗 **Kata Majemuk Dinamis** | Pemecahan kata majemuk secara otomatis via `compounds.json` |

---

## 🚀 Instalasi

Membutuhkan **Python 3.8+**.

```bash
# Via PyPI (Direkomendasikan)
pip install saka-nlp

# Via Source (Pengembangan)
git clone https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP.git
cd Saka-NLP && pip install -e .
```

---

## 📖 Penggunaan Dasar

Saka-NLP dirancang agar intuitif. Cukup `import saka`. Contoh lengkap dapat ditemukan di [**basic_usage.py**](examples/basic_usage.py).

<details>
<summary><b>1. Tokenisasi & Normalisasi</b></summary>

```python
import saka

# Tokenisasi (Menangani afiks & tanda baca)
text = "Belajar NLP di era 5G, seru banget!"
tokens = saka.tokenize(text)
# ['Belajar', 'NLP', 'di', 'era', '5G', ',', 'seru', 'banget', '!']

# Normalisasi Bahasa Gaul (Bahasa Indonesia)
normalized = saka.normalize("klo gimana ntar gw k kampus")
# 'kalau bagaimana nanti saya ke kampus'
```
</details>

<details>
<summary><b>2. Morfologi & KBBI</b></summary>

```python
import saka

# Analisis Morfologi (Menangani kata majemuk & fusi)
word = "mempertanggungjawabkan"
analysis = saka.analyze(word)
print(analysis["root"]) # 'tanggung jawab'

# Pencarian Langsung KBBI (Web Scraping Real-time)
res = saka.query_kbbi("belajar")
# {'status': 'found', 'definitions': [...]}
```
</details>

<details>
<summary><b>3. Stopwords Regional</b></summary>

```python
import saka
# Mendukung: 'id', 'en', 'sunda', 'jawa', 'bali', 'minang', 'jaksel', 'batak', 'all'

stops = saka.get_stopwords("batak")
print("do" in stops) # True

en_stops = saka.get_stopwords("en")
print("however" in en_stops) # True
```
</details>

---

## 🤖 AI Agentik & Prompting

Bangun aplikasi berbasis LLM dengan kendali penuh. Contoh lengkap: [**output_demo.py**](examples/output_demo.py) & [**multi_agent_edu_demo.py**](examples/multi_agent_edu_demo.py).

```python
import saka
from saka import Agent, OutputFormatter

# 1. Pemformatan Output (Hemat Token LLM!)
data = [{"word": "horas", "pos": "kata sapaan", "meaning": "halo"}]
# Format ke HTML/Markdown secara lokal
markdown_table = OutputFormatter.format(data, "markdown")

# 2. Agent Terstruktur & Pemanggilan Alat
bot = Agent("Asisten", "Ahli Linguistik")
bot.add_tool(name="cek_arti", desc="Cek KBBI", func=saka.query_kbbi)

# 3. Pembuat Prompt (Optimasi Token)
prompt = saka.build_prompt(
    role="Analis",
    task="Klasifikasi",
    input_data="Teks...",
    optimize_text=True
)
```

---

## 📊 Benchmark Saka-Eval

Evaluasi model Anda secara asinkron. Contoh: [**saka_eval_huggingface_demo.py**](examples/saka_eval_huggingface_demo.py).

```python
from saka.evaluation.benchmarker import SakaEval

evaluator = SakaEval(task="sentiment")
# Muat via nama konfigurasi ("sentiment" atau "ner")
evaluator.load_hf_dataset("Muhammad-Ikhwan-Fathulloh/Saka-Eval", name="sentiment")

results = await evaluator.evaluate(model, text="text", label="label")
print(f"Akurasi: {results['metrics']['accuracy']:.2%}")
```

---

## 🔗 Penanganan Kata Majemuk Dinamis

Saka-NLP memecah kata majemuk secara otomatis via `compounds.json`:

| Input | Root |
|---|---|
| `menyebarluaskan` | `sebar luas` |
| `kerjasama` | `kerja sama` |
| `hulunagara` | `hulu nagara` (Sunda) |
| `bundokanduang` | `bundo kanduang` (Minang) |

---

## 🌏 Ekosistem Regional

Dukungan mendalam untuk bahasa daerah (Kamus & Aksara).

### Batak *(Baru di v0.2.6)*

Saka-NLP sekarang mendukung **Batak** lintas tiga dialek — Toba, Karo, dan Mandailing — dengan leksikon **780+ kata** bersumber dari tata bahasa akademis dan KamusBatak.com.

```python
import saka
from saka.core.analyzer import _BATAK_DICT

# Kata Batak dalam pipeline morfologi
print(saka.analyze("holong")["regional_matches"])   # ['batak']  ← kasih/cinta (Toba)
print(saka.analyze("mangan")["regional_matches"])   # ['batak']  ← makan (Toba)

# Stopwords Batak
sw = saka.get_stopwords("batak")
print(f"{len(sw)} kata fungsi Batak dimuat")

# Pencarian kamus langsung
print(_BATAK_DICT["horas"]["arti"])      # 'halo, selamat (salam khas Batak Toba)'
print(_BATAK_DICT["denggan"]["arti"])    # 'baik, bagus'
```

**Sumber:**
- Nababan, P.W.J. (1981). *A Grammar of Toba-Batak* (D-37). Pacific Linguistics, ANU. [DOI:10.15144/PL-D37](https://doi.org/10.15144/PL-D37)
- Woollams, G. (1996). *A Grammar of Karo Batak, Sumatra* (C-130). Pacific Linguistics, ANU. [DOI:10.15144/PL-C130](https://doi.org/10.15144/PL-C130)
- [KamusBatak.Com](https://www.kamusbatak.com/) — Kamus Batak–Indonesia Daring

<details>
<summary><b>Klik untuk melihat detail aksara (Bahasa Sunda, Jawa, Bali)</b></summary>

### Aksara Sunda (Ngalagena)
| Latin | Aksara | Latin | Aksara |
| ----- | ------ | ----- | ------ |
| ha    | ᮠ      | na    | ᮔ      |
| ...   | ...    | ...   | ...    |

### Aksara Jawa (Nglegena)
| Latin | Aksara | Latin | Aksara |
| ----- | ------ | ----- | ------ |
| ha    | ꦲ      | na    | ꦤ      |
| ...   | ...    | ...   | ...    |

### Aksara Bali (Wreastra)
| Latin | Aksara | Latin | Aksara |
| ----- | ------ | ----- | ------ |
| ...   | ...    | ...   | ...    |

*(Tabel lengkap tersedia di [Dokumentasi Web](http://saka-nlp.netlify.app/))*
</details>

---

## 🛠️ CLI & Sitasi

### Penggunaan CLI
```bash
saka --help
saka --normalize "ngapain ke kampus klo libur"
```

### Sitasi
```bibtex
@software{Fathulloh_Saka-NLP_2026,
  author = {Fathulloh, Muhammad Ikhwan},
  title = {{Saka-NLP: Indonesian NLP Toolkit for Tokenization, Slang Normalization, and Agentic AI Support}},
  month = {5},
  year = {2026},
  publisher = {Zenodo},
  version = {0.2.6},
  doi = {10.5281/zenodo.20092640},
  url = {https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP}
}
```

---

## 🗄️ Sumber & Kredit

Saka-NLP dibangun di atas fondasi penelitian dan dataset terbuka berikut. Kami berterima kasih kepada para peneliti dan kontributor:

| Kategori      | Sumber                                                                              | Deskripsi                  |
| ------------- | ----------------------------------------------------------------------------------- | ---------------------------- |
| **Dataset**  | [Carant-AI](https://huggingface.co/datasets/carant-ai/indonesian_sentiment_dataset) | Dataset Sentimen Indonesia |
|               | [Kiuyha](https://huggingface.co/datasets/Kiuyha/surabaya-ner-dataset)               | Dataset NER Surabaya         |
|               | [IndoNLU](https://huggingface.co/datasets/indonlp/indonlu)                          | Standar Benchmark          |
|               | [Tala Dataset](https://github.com/masdevid/ID-Stopwords)                            | Stopwords Indonesia         |
| **Leksikon**  | [SundaDigi](https://sundadigi.com)                                                  | Kamus Digital Sunda |
|               | [Sastra.org](https://sastra.org)                                                    | Leksikon Jawa             |
|               | [BASAbali Wiki](https://basabali.org)                                               | Leksikon Bali             |
|               | [KamusBatak.Com](https://www.kamusbatak.com) | Kamus Batak |
| **Tata Bahasa** | Nababan (1981). *A Grammar of Toba-Batak*. [DOI:10.15144/PL-D37](https://doi.org/10.15144/PL-D37) | Batak Toba |
|               | Woollams (1996). *A Grammar of Karo Batak*. [DOI:10.15144/PL-C130](https://doi.org/10.15144/PL-C130) | Batak Karo |
|               | Bird et al. (2009). *NLTK*. [nltk.org](https://www.nltk.org/) | Stopwords Inggris |
|               | Pedregosa et al. (2011). *Scikit-learn*. JMLR 12. | Stopwords Inggris |
| **Perpustakaan** | [HuggingFace](https://huggingface.co)                                               | Dataset & Hub Ecoystem      |
|               | [scikit-learn](https://scikit-learn.org)                                            | Metrik Evaluasi           |
|               | [Emoji/Emot](https://pypi.org/project/emoji/)                                       | Penanganan Teks Media Sosial   |

---

## ❤️ Dukungan
- **Arsitek:** [Muhammad Ikhwan Fathulloh](https://github.com/Muhammad-Ikhwan-Fathulloh)
- **Lisensi:** [MIT License](LICENSE)
- **Dukungan:** [Saweria](https://saweria.co/ikhwanfathulloh) | [Trakteer](https://trakteer.id/kexnp7aorpxyaz70y7gn)
