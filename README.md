# Saka: Indonesian NLP with Prompting and Agentic AI Support 🇮🇩 v0.2.5

[**Bahasa Indonesia**](README.md) | [**English**](README_EN.md)

[![PyPI version](https://img.shields.io/pypi/v/saka-nlp.svg)](https://pypi.org/project/saka-nlp/)
[![Documentation](https://img.shields.io/badge/docs-live-brightgreen)](http://saka-nlp.netlify.app/)
[![Colab](https://img.shields.io/badge/Colab-Playground-orange)](https://colab.research.google.com/drive/1MJ6fwJruR6B-UVT1sqKyqWXukjGe2UCH?usp=sharing)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20092640.svg)](https://doi.org/10.5281/zenodo.20092640)

**Saka** (Bahasa Jawa/Sunda: *Tiang Penyangga*) adalah sebuah *architectural framework* modern untuk pemrosesan teks Bahasa Indonesia dan daerah yang dibangun dengan prinsip asinkron, modular, dan cerdas.

---

## 📌 Daftar Isi
- [Saka: Indonesian NLP with Prompting and Agentic AI Support 🇮🇩 v0.2.5](#saka-indonesian-nlp-with-prompting-and-agentic-ai-support-v025)
  - [📌 Daftar Isi](#-daftar-isi)
  - [✨ Fitur Unggulan](#-fitur-unggulan)
  - [🚀 Instalasi](#-instalasi)
  - [📖 Penggunaan Dasar](#-penggunaan-dasar)
  - [🤖 Agentic AI \& Prompting](#-agentic-ai--prompting)
  - [📊 Saka-Eval Benchmark](#-saka-eval-benchmark)
  - [🌏 Ekosistem Nusantara](#-ekosistem-nusantara)
  - [🛠️ CLI \& Sitasi](#️-cli--sitasi)
  - [🗄️ Sumber \& Kredit](#️-sumber--kredit)
  - [❤️ Support](#️-support)
    - [CLI Usage](#cli-usage)
    - [Citation](#citation)
  - [❤️ Credits \& Support](#️-credits--support)

---

## ✨ Fitur Unggulan

| Fitur                     | Deskripsi                                                       |
| ------------------------- | --------------------------------------------------------------- |
| ⚡ **Async Processing**    | Pemrosesan non-blocking untuk dataset skala besar.              |
| 🧩 **Modular Design**      | Komponen *plug-and-play* yang mudah diintegrasikan.             |
| 🧠 **Morphology Analyzer** | Analisis imbuhan hibrida dengan *Morphophonemic Restructuring*. |
| 📖 **Live KBBI**           | Ekstraksi arti kata langsung dari situs resmi KBBI.             |
| 🤖 **Agentic AI**          | Orchestration prompt LLM, Multi-Agent, dan Tool Calling.        |
| 🔠 **Aksara Nusantara**    | Transliterasi Aksara Sunda, Jawa, dan Bali.                     |
| 🔗 **Dynamic Compounds**   | Pemisahan kata majemuk otomatis via dataset JSON dinamis.       |

---

## 🚀 Instalasi

Pastikan menggunakan **Python 3.8+**.

```bash
# Via PyPI (Rekomendasi)
pip install saka-nlp

# Via Source (Development)
git clone https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP.git
cd Saka-NLP && pip install -e .
```

---

## 📖 Penggunaan Dasar

Saka-NLP didesain agar intuitif. Cukup `import saka`. Contoh lengkap dapat dilihat di [**basic_usage.py**](examples/basic_usage.py).

<details>
<summary><b>1. Tokenisasi & Normalisasi</b></summary>

```python
import saka

# Tokenisasi (Handle imbuhan & tanda baca)
text = "Belajar NLP di era 5G, seru bgt!"
tokens = saka.tokenize(text) 
# ['Belajar', 'NLP', 'di', 'era', '5G', ',', 'seru', 'bgt', '!']

# Normalisasi Slang (Social Media Text)
normalized = saka.normalize("klo gimana ntar gw k kampus") 
# 'kalau bagaimana nanti saya ke kampus'
```
</details>

<details>
<summary><b>2. Morfologi & KBBI</b></summary>

```python
import saka

# Analisis Morfologi (Handle kata majemuk & peleburan)
word = "mempertanggungjawabkan"
analysis = saka.analyze(word)
print(analysis["root"]) # 'tanggung jawab'

# Live KBBI Search (Web Scraping Real-time)
res = saka.query_kbbi("belajar")
# {'status': 'found', 'definitions': [...]}
```
</details>

<details>
<summary><b>3. Stopwords Nusantara</b></summary>

```python
import saka
# Mendukung: id, sunda, jawa, bali, minang, en, jaksel, all
stops = saka.get_stopwords("minang")
print("ampek" in stops) # True
```
</details>

---

## 🤖 Agentic AI & Prompting

Membangun aplikasi berbasis LLM dengan kontrol penuh. Contoh lengkap: [**output_demo.py**](examples/output_demo.py) & [**multi_agent_edu_demo.py**](examples/multi_agent_edu_demo.py).

```python
import saka
from saka import Agent, OutputFormatter

# 1. Output Formatting (Hemat Token LLM!)
data = [{"word": "saka", "pos": "noun"}]
# Format ke HTML/Markdown secara lokal
markdown_table = OutputFormatter.format(data, "markdown")

# 2. Structured Agent & Tool Calling
bot = Agent("Asisten", "Pakar Bahasa")
bot.add_tool(name="cek_arti", desc="Cek KBBI", func=saka.query_kbbi)

# 3. Prompt Builder (Optimasi Token)
prompt = saka.build_prompt(
    role="Analist", 
    task="Klasifikasi", 
    input_data="Teks...",
    optimize_text=True
)
```

---

## 📊 Saka-Eval Benchmark

Evaluasi model Anda secara asinkron. Contoh: [**saka_eval_huggingface_demo.py**](examples/saka_eval_huggingface_demo.py).

```python
from saka.evaluation.benchmarker import SakaEval

evaluator = SakaEval(task="sentiment")
# Load via config name ("sentiment" atau "ner")
evaluator.load_hf_dataset("Muhammad-Ikhwan-Fathulloh/Saka-Eval", name="sentiment")

results = await evaluator.evaluate(model, text="text", label="label")
print(f"Accuracy: {results['metrics']['accuracy']:.2%}")
```

---

## 🌏 Ekosistem Nusantara

Dukungan mendalam untuk bahasa daerah (Kamus & Aksara).

<details>
<summary><b>Klik untuk melihat detail Aksara (Sunda, Jawa, Bali)</b></summary>

### Aksara Sunda (Ngalagena)
| Latin | Aksara | Latin | Aksara |
| ----- | ------ | ----- | ------ |
| ha    | ᮠ      | na    | ᮔ      |
| ca    | ᮎ      | ra    | ᮛ      |
| ...   | ...    | ...   | ...    |

### Aksara Jawa (Nglegena)
| Latin | Aksara | Latin | Aksara |
| ----- | ------ | ----- | ------ |
| ha    | ꦲ      | na    | ꦤ      |
| ...   | ...    | ...   | ...    |

*(Tabel lengkap tersedia di [Dokumentasi Web](http://saka-nlp.netlify.app/))*

### 🔗 Dynamic Compound Handling
Saka-NLP kini mendukung pemisahan kata majemuk secara dinamis melalui `compounds.json`.
- **Indonesian**: `menyebarluaskan` → `sebar luas`, `kerjasama` → `kerja sama`
- **Sunda**: `hulunagara` → `hulu nagara`, `indungsuku` → `indung suku`
- **Minang**: `bundokanduang` → `bundo kanduang`, `ranahminang` → `ranah minang`
</details>

---

## 🛠️ CLI & Sitasi

### CLI Usage
```bash
saka --help
saka --normalize "ngapain ke kampus klo libur"
```

### Citation
```bibtex
@software{Fathulloh_Saka-NLP_2026,
  author = {Fathulloh, Muhammad Ikhwan},
  title = {{Saka-NLP: Indonesian NLP Toolkit}},
  year = {2026},
  version = {0.2.5},
  doi = {10.5281/zenodo.20092640},
  url = {https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP}
}
```

---

## 🗄️ Sumber & Kredit

Saka-NLP dibangun di atas fondasi riset dan dataset terbuka berikut. Kami berterima kasih kepada para peneliti dan kontributor:

| Kategori     | Sumber                                                                              | Deskripsi                    |
| ------------ | ----------------------------------------------------------------------------------- | ---------------------------- |
| **Dataset**  | [Carant-AI](https://huggingface.co/datasets/carant-ai/indonesian_sentiment_dataset) | Indonesian Sentiment Dataset |
|              | [Kiuyha](https://huggingface.co/datasets/Kiuyha/surabaya-ner-dataset)               | Surabaya NER Dataset         |
|              | [IndoNLU](https://huggingface.co/datasets/indonlp/indonlu)                          | Benchmark Standards          |
|              | [Tala Dataset](https://github.com/masdevid/ID-Stopwords)                            | Indonesian Stopwords         |
| **Leksikon** | [SundaDigi](https://sundadigi.com)                                                  | Kamus Digital Bahasa Sunda   |
|              | [Sastra.org](https://sastra.org)                                                    | Leksikon Bahasa Jawa         |
|              | [BASAbali Wiki](https://basabali.org)                                               | Kamus Bahasa Bali            |
| **Library**  | [HuggingFace](https://huggingface.co)                                               | Datasets & Hub Ecoystem      |
|              | [scikit-learn](https://scikit-learn.org)                                            | Evaluation Metrics           |
|              | [Emoji/Emot](https://pypi.org/project/emoji/)                                       | Social Media Text Handling   |

---

## ❤️ Support
- **Architect**: [Muhammad Ikhwan Fathulloh](https://github.com/Muhammad-Ikhwan-Fathulloh)
- **License**: [MIT License](LICENSE)
- **Support**: [Saweria](https://saweria.co/ikhwanfathulloh) | [Trakteer](https://trakteer.id/kexnp7aorpxyaz70y7gn)
