# Saka: Indonesian Language Processing with Prompting and Agentic AI Support 🇮🇩 v0.2.6

[**English**](README_EN.md) | [**Bahasa Indonesia**](README.md)

[![PyPI version](https://img.shields.io/pypi/v/saka-nlp.svg)](https://pypi.org/project/saka-nlp/)
[![Documentation](https://img.shields.io/badge/docs-live-brightgreen)](http://saka-nlp.netlify.app/)
[![Colab](https://img.shields.io/badge/Colab-Playground-orange)](https://colab.research.google.com/drive/1MJ6fwJruR6B-UVT1sqKyqWXukjGe2UCH?usp=sharing)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20092640.svg)](https://doi.org/10.5281/zenodo.20092640)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Saka** (Javanese/Sundanese: *Pillar*) is a modern architectural framework for Indonesian and regional language processing, built with asynchronous, modular, and intelligent design principles.

---

## 📌 Table of Contents
- [Saka: Indonesian Language Processing with Prompting and Agentic AI Support 🇮🇩 v0.2.6](#saka-indonesian-language-processing-with-prompting-and-agentic-ai-support--v026)
  - [📌 Table of Contents](#-table-of-contents)
  - [✨ Key Features](#-key-features)
  - [🚀 Installation](#-installation)
  - [📖 Quick Start](#-quick-start)
  - [🤖 Agentic AI & Prompting](#-agentic-ai--prompting)
  - [📊 Saka-Eval Benchmark](#-saka-eval-benchmark)
  - [🔗 Dynamic Compound Handling](#-dynamic-compound-handling)
  - [🌏 Regional Ecosystem](#-regional-ecosystem)
  - [🛠️ CLI & Citation](#️-cli--citation)
  - [🗄️ Sources & Credits](#️-sources--credits)
  - [❤️ Support](#-support)

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| ⚡ **Async Processing** | Non-blocking processing for large-scale datasets. |
| 🧩 **Modular Design** | Plug-and-play components for easy integration. |
| 🧠 **Morphology Analyzer** | Hybrid affix analysis with *Morphophonemic Restructuring*. |
| 📖 **Live KBBI** | Extract word meanings from the official Indonesian Dictionary (KBBI). |
| 🛑 **Hybrid Stopwords** | Indonesian, English, Sundanese, Javanese, Balinese, Minangkabau, **Batak** (Toba · Karo · Mandailing), and South Jakarta slang |
| 🗺️ **Regional Lexicons** | Validated word dictionaries: Sundanese, Javanese, Balinese, Minangkabau, **Batak** |
| 🔠 **Regional Scripts** | Transliteration for Sundanese, Javanese, and Balinese (Hanacaraka). |
| 🤖 **Agentic AI** | LLM prompt orchestration, Multi-Agent management, and Tool Calling. |
| 📊 **Saka-Eval** | Async benchmark suite for Indonesian NLP models (Sentiment / NER) |
| 🔗 **Dynamic Compounds** | Automatic compound word splitting via `compounds.json` |

---

## 🚀 Installation

Requires **Python 3.8+**.

```bash
# Via PyPI (Recommended)
pip install saka-nlp

# Via Source (Development)
git clone https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP.git
cd Saka-NLP && pip install -e .
```

---

## 📖 Quick Start

Saka-NLP is designed to be intuitive. Just `import saka`. Complete examples can be found in [**basic_usage.py**](examples/basic_usage.py).

<details>
<summary><b>1. Tokenization & Normalization</b></summary>

```python
import saka

# Tokenization (Handles affixes & punctuation)
text = "Belajar NLP di era 5G, seru banget!"
tokens = saka.tokenize(text)
# ['Belajar', 'NLP', 'di', 'era', '5G', ',', 'seru', 'banget', '!']

# Slang Normalization (Indonesian)
normalized = saka.normalize("klo gimana ntar gw k kampus")
# 'kalau bagaimana nanti saya ke kampus'
```
</details>

<details>
<summary><b>2. Morphology & KBBI</b></summary>

```python
import saka

# Morphological Analysis (Handles compound words & fusion)
word = "mempertanggungjawabkan"
analysis = saka.analyze(word)
print(analysis["root"]) # 'tanggung jawab'

# Live KBBI Lookup (Real-time web scraping)
res = saka.query_kbbi("belajar")
# {'status': 'found', 'definitions': [...]}
```
</details>

<details>
<summary><b>3. Regional Stopwords</b></summary>

```python
import saka
# Supported: 'id', 'en', 'sunda', 'jawa', 'bali', 'minang', 'jaksel', 'batak', 'all'

stops = saka.get_stopwords("batak")
print("do" in stops) # True

en_stops = saka.get_stopwords("en")
print("however" in en_stops) # True
```
</details>

---

## 🤖 Agentic AI & Prompting

Build LLM-based applications with full control. Complete examples: [**output_demo.py**](examples/output_demo.py) & [**multi_agent_edu_demo.py**](examples/multi_agent_edu_demo.py).

```python
import saka
from saka import Agent, OutputFormatter

# 1. Output Formatting (Save LLM Tokens!)
data = [{"word": "horas", "pos": "greeting", "meaning": "hello"}]
# Format to HTML/Markdown locally
markdown_table = OutputFormatter.format(data, "markdown")

# 2. Structured Agent & Tool Calling
bot = Agent("Assistant", "Linguistic Expert")
bot.add_tool(name="check_meaning", desc="Check KBBI", func=saka.query_kbbi)

# 3. Prompt Builder (Token Optimization)
prompt = saka.build_prompt(
    role="Analyst",
    task="Classification",
    input_data="Text...",
    optimize_text=True
)
```

---

## 📊 Saka-Eval Benchmark

Evaluate your model asynchronously. Example: [**saka_eval_huggingface_demo.py**](examples/saka_eval_huggingface_demo.py).

```python
import asyncio
from saka.evaluation.benchmarker import SakaEval

async def run():
    evaluator = SakaEval(task="sentiment")
    # Load via config name ("sentiment" or "ner")
    evaluator.load_hf_dataset("Muhammad-Ikhwan-Fathulloh/Saka-Eval", name="sentiment")
    results = await evaluator.evaluate(model, text="text", label="label")
    print(f"Accuracy: {results['metrics']['accuracy']:.2%}")

asyncio.run(run())
```

---

## 🔗 Dynamic Compound Handling

Saka-NLP resolves compound words automatically via `compounds.json`:

| Input | Root |
|-------|------|
| `menyebarluaskan` | `sebar luas` |
| `kerjasama` | `kerja sama` |
| `hulunagara` | `hulu nagara` (Sundanese) |
| `bundokanduang` | `bundo kanduang` (Minangkabau) |

---

## 🌏 Regional Ecosystem

Deep support for regional languages (Dictionaries & Scripts).

### Batak *(New in v0.2.6)*

Saka-NLP now supports **Batak** across three dialects — Toba, Karo, and Mandailing — with a lexicon of **780+ words** sourced from academic grammars and KamusBatak.com.

```python
import saka
from saka.core.analyzer import _BATAK_DICT

# Batak word in morphology pipeline
print(saka.analyze("holong")["regional_matches"])   # ['batak']  ← love (Toba)
print(saka.analyze("mangan")["regional_matches"])   # ['batak']  ← eat (Toba)

# Batak stopwords
sw = saka.get_stopwords("batak")
print(f"{len(sw)} Batak function words loaded")

# Dictionary lookup
print(_BATAK_DICT["horas"]["arti"])      # 'halo, selamat (salam khas Batak Toba)'
print(_BATAK_DICT["denggan"]["arti"])    # 'baik, bagus'
```

**Sources:**
- Nababan, P.W.J. (1981). *A Grammar of Toba-Batak* (D-37). Pacific Linguistics, ANU. [DOI:10.15144/PL-D37](https://doi.org/10.15144/PL-D37)
- Woollams, G. (1996). *A Grammar of Karo Batak, Sumatra* (C-130). Pacific Linguistics, ANU. [DOI:10.15144/PL-C130](https://doi.org/10.15144/PL-C130)
- [KamusBatak.Com](https://www.kamusbatak.com/) — Online Batak–Indonesian dictionary

<details>
<summary><b>Click to view script details (Sundanese, Javanese, Balinese)</b></summary>

### Sundanese Script (Ngalagena)
| Latin | Script | Latin | Script |
|-------|--------|-------|--------|
| ha    | ᮠ     | na    | ᮔ     |
| ...   | ...    | ...   | ...    |

### Javanese Script (Nglegena)
| Latin | Script | Latin | Script |
|-------|--------|-------|--------|
| ha    | ꦲ     | na    | ꦤ     |
| ...   | ...    | ...   | ...    |

*(Full table available in the [Web Documentation](http://saka-nlp.netlify.app/))*
</details>

---

## 🛠️ CLI & Citation

### CLI Usage
```bash
saka --help
saka --normalize "ngapain ke kampus klo libur"
```

### Citation
```bibtex
@software{Fathulloh_Saka-NLP_2026,
  author    = {Fathulloh, Muhammad Ikhwan},
  title     = {{Saka-NLP: Indonesian NLP Toolkit for Tokenization, Slang
                Normalization, and Agentic AI Support}},
  month     = {5},
  year      = {2026},
  publisher = {Zenodo},
  version   = {0.2.6},
  doi       = {10.5281/zenodo.20092640},
  url       = {https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP}
}
```

---

## 🗄️ Sources & Credits

Saka-NLP is built on the following open research and datasets. We thank the researchers and contributors:

| Category | Source | Description |
|----------|--------|-------------|
| **Datasets** | [Carant-AI](https://huggingface.co/datasets/carant-ai/indonesian_sentiment_dataset) | Indonesian Sentiment Dataset |
| | [Kiuyha](https://huggingface.co/datasets/Kiuyha/surabaya-ner-dataset) | Surabaya NER Dataset |
| | [IndoNLU](https://huggingface.co/datasets/indonlp/indonlu) | Standard Benchmark |
| | [Tala Dataset](https://github.com/masdevid/ID-Stopwords) | Indonesian Stopwords |
| **Lexicons** | [SundaDigi](https://sundadigi.com) | Sundanese Digital Dictionary |
| | [Sastra.org](https://sastra.org) | Javanese Lexicon |
| | [BASAbali Wiki](https://basabali.org) | Balinese Lexicon |
| | [KamusBatak.Com](https://www.kamusbatak.com) | Batak Dictionary |
| **Grammars** | Nababan (1981). *A Grammar of Toba-Batak*. [DOI:10.15144/PL-D37](https://doi.org/10.15144/PL-D37) | Toba Batak |
| | Woollams (1996). *A Grammar of Karo Batak*. [DOI:10.15144/PL-C130](https://doi.org/10.15144/PL-C130) | Karo Batak |
| | Bird et al. (2009). *NLTK*. [nltk.org](https://www.nltk.org/) | English Stopwords |
| | Pedregosa et al. (2011). *Scikit-learn*. JMLR 12. | English Stopwords |
| **Libraries** | [HuggingFace](https://huggingface.co) | Datasets & Hub Ecosystem |
| | [scikit-learn](https://scikit-learn.org) | Evaluation Metrics |
| | [Emoji/Emot](https://pypi.org/project/emoji/) | Social Media Text Handling |

---

## ❤️ Support
- **Architect:** [Muhammad Ikhwan Fathulloh](https://github.com/Muhammad-Ikhwan-Fathulloh)
- **License:** [MIT License](LICENSE)
- **Support:** [Saweria](https://saweria.co/ikhwanfathulloh) | [Trakteer](https://trakteer.id/kexnp7aorpxyaz70y7gn)
