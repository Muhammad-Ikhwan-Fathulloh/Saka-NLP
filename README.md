# Saka: Indonesian NLP with Prompting and Agentic AI Support 🇮🇩

[**Bahasa Indonesia**](README.md) | [**English**](README_EN.md)

[![PyPI version](https://img.shields.io/pypi/v/saka-nlp.svg)](https://pypi.org/project/saka-nlp/)
[![Documentation](https://img.shields.io/badge/docs-live-brightgreen)](http://saka-nlp.netlify.app/)
[![Colab](https://img.shields.io/badge/Colab-Playground-orange)](https://colab.research.google.com/drive/1MJ6fwJruR6B-UVT1sqKyqWXukjGe2UCH?usp=sharing)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20092640.svg)](https://doi.org/10.5281/zenodo.20092640)

**Saka** (Bahasa Jawa/Sunda: *Tiang Penyangga*) adalah sebuah *architectural framework* modern untuk pemrosesan teks Bahasa Indonesia dan daerah yang dibangun dengan prinsip asinkron, modular, dan cerdas.

---

## 📌 Daftar Isi
- [Saka: Indonesian NLP with Prompting and Agentic AI Support 🇮🇩](#saka-indonesian-nlp-with-prompting-and-agentic-ai-support-)
  - [📌 Daftar Isi](#-daftar-isi)
  - [✨ Fitur Unggulan](#-fitur-unggulan)
  - [🚀 Instalasi](#-instalasi)
  - [📖 Penggunaan Dasar](#-penggunaan-dasar)
  - [🤖 Agentic AI \& Prompting](#-agentic-ai--prompting)
  - [📊 Saka-Eval Benchmark](#-saka-eval-benchmark)
  - [🌏 Ekosistem Nusantara](#-ekosistem-nusantara)
    - [Aksara Sunda (Ngalagena)](#aksara-sunda-ngalagena)
    - [Aksara Jawa (Nglegena)](#aksara-jawa-nglegena)
  - [🛠️ CLI \& Sitasi](#️-cli--sitasi)
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

Saka-NLP didesain agar intuitif. Cukup `import saka`.

<details>
<summary><b>1. Tokenisasi & Normalisasi</b></summary>

```python
import saka

# Tokenisasi
tokens = saka.tokenize("Halo, apa kabar?") 
# ['Halo', ',', 'apa', 'kabar', '?']

# Normalisasi Slang
normalized = saka.normalize("klo gimana gw") 
# 'kalau bagaimana saya'
```
</details>

<details>
<summary><b>2. Morfologi & KBBI</b></summary>

```python
import saka

# Analisis Morfologi (Handle kata majemuk & peleburan)
print(saka.analyze("menyebarluaskan"))
# {'root': 'sebar luas', ...}

# Live KBBI Search
res = saka.query_kbbi("belajar")
```
</details>

<details>
<summary><b>3. Stopwords Nusantara</b></summary>

```python
import saka
# Mendukung: id, sunda, jawa, bali, minang, en, jaksel
stops = saka.get_stopwords("minang")
```
</details>

---

## 🤖 Agentic AI & Prompting

Membangun aplikasi berbasis LLM dengan kontrol penuh atas prompt dan output.

```python
import saka

# 1. Token Optimization via Local Formatting
data = [{"id": 1, "text": "Saka"}]
output = saka.OutputFormatter.format(data, "json")

# 2. Structured Prompt Builder
prompt = saka.build_prompt(role="Analist", task="Klasifikasi", input_data="Teks...")

# 3. Agent & Tool Calling
bot = saka.Agent("Asisten", "Membantu user")
bot.add_tool(name="calc", desc="Hitung", func=lambda x: x*2)
```

---

## 📊 Saka-Eval Benchmark

Evaluasi model NLP Anda dengan dataset standar Indonesia secara asinkron.

```python
from saka.evaluation.benchmarker import SakaEval

evaluator = SakaEval(task="sentiment")
evaluator.load_hf_dataset("Muhammad-Ikhwan-Fathulloh/Saka-Eval")

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
  version = {0.2.4},
  doi = {10.5281/zenodo.20092640},
  url = {https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP}
}
```

---

## ❤️ Credits & Support
- **Architect**: [Muhammad Ikhwan Fathulloh](https://github.com/Muhammad-Ikhwan-Fathulloh)
- **License**: [MIT License](LICENSE)
- **Support**: [Saweria](https://saweria.co/ikhwanfathulloh) | [Trakteer](https://trakteer.id/kexnp7aorpxyaz70y7gn)
