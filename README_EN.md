# Saka: Indonesian Language Processing with Prompting and Agentic AI Support v0.3.0

[**English**](README_EN.md) | [**Bahasa Indonesia**](README.md)

[![PyPI version](https://img.shields.io/pypi/v/saka-nlp.svg)](https://pypi.org/project/saka-nlp/)
[![Documentation](https://img.shields.io/badge/docs-live-brightgreen)](http://saka-nlp.netlify.app/)
[![Colab](https://img.shields.io/badge/Colab-Playground-orange)](https://colab.research.google.com/drive/1MJ6fwJruR6B-UVT1sqKyqWXukjGe2UCH?usp=sharing)
[![Apify Actor](https://img.shields.io/badge/Apify-Actor-blue)](https://apify.com/ikhwan_fathulloh/saka-nlp-actor)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20092640.svg)](https://doi.org/10.5281/zenodo.20092640)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Saka** (Javanese/Sundanese: *Pillar*) is a modern architectural framework for Indonesian and regional language processing, built with asynchronous, modular, and intelligent design principles.

---

## Table of Contents
- [Saka: Indonesian Language Processing with Prompting and Agentic AI Support v0.3.0](#saka-indonesian-language-processing-with-prompting-and-agentic-ai-support-v030)
  - [Table of Contents](#table-of-contents)
  - [Key Features](#key-features)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
  - [Examples Directory](#examples-directory)
  - [Agentic AI \& Prompting](#agentic-ai--prompting)
  - [Saka-Eval Benchmark](#saka-eval-benchmark)
  - [Dynamic Compound Handling](#dynamic-compound-handling)
  - [Regional Ecosystem](#regional-ecosystem)
    - [1. Sundanese, Javanese, and Balinese](#1-sundanese-javanese-and-balinese)
    - [2. Minangkabau](#2-minangkabau)
    - [3. Batak](#3-batak)
    - [Sundanese Script (Ngalagena)](#sundanese-script-ngalagena)
    - [Javanese Script (Nglegena)](#javanese-script-nglegena)
    - [Balinese Script (Wreastra)](#balinese-script-wreastra)
  - [CLI \& Citation](#cli--citation)
    - [CLI Usage](#cli-usage)
    - [Citation](#citation)
  - [Sources \& Credits](#sources--credits)
  - [Support](#support)

---

## Key Features

| Feature                             | Description                                                                                                                                                                                               |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Async Processing**                | Supports non-blocking operations to efficiently process large-scale datasets without waiting for one task to finish first.                                                                                |
| **Performance Optimizations**       | LRU caching on `normalize()`, `analyze()`, and `get_stopwords()` to reduce repeated processing time and improve speed.                                                                                    |
| **Modular Design**                  | Plug-and-play components to simplify integration with other applications or adding new features.                                                                                                          |
| **Morphology Analyzer**             | Hybrid affix analysis of Indonesian and regional languages with *Morphophonemic Restructuring* to separate and understand word structure, including compound words and derived words.                     |
| **Live KBBI**                       | Real-time extraction of word meanings from the official Indonesian Dictionary (KBBI) via web scraping to get accurate definitions.                                                                        |
| **Hybrid Stopwords**                | Supports stopwords for various languages and dialects: Indonesian, English, Sundanese, Javanese, Balinese, Minangkabau, Batak (Toba, Karo, Mandailing), and South Jakarta slang.                          |
| **Regional Lexicons**               | Provides validated word dictionaries for regional languages like Sundanese, Javanese, Balinese, Minangkabau, and Batak.                                                                                   |
| **Regional Script Transliteration** | Enables text conversion between Latin letters and traditional scripts of Sundanese (Ngalagena), Javanese (Nglegena), and Balinese (Wreastra).                                                             |
| **Agentic AI**                      | Provides tools to orchestrate LLM (Large Language Model) prompts, manage multi-agent systems, and perform custom tool calling to build AI-based applications.                                             |
| **Saka-Eval**                       | Asynchronous benchmark suite to evaluate the performance of Indonesian NLP models on tasks like sentiment analysis and Named Entity Recognition (NER).                                                    |
| **Dynamic Compound Handling**       | Automatically splits Indonesian and regional compound words using rules defined in `compounds.json`.                                                                                                      |
| **Apify Actor**                     | Run Saka on the Apify platform for cloud-based Indonesian web scraping and text processing automation, available at [ikhwan_fathulloh/saka-nlp-actor](https://apify.com/ikhwan_fathulloh/saka-nlp-actor). |

---

## Installation

Requires **Python 3.8+**.

```bash
# Via PyPI (Recommended)
pip install saka-nlp

# Via Source (Development)
git clone https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP.git
cd Saka-NLP ; pip install -e .
```

---

## Quick Start

Saka-NLP is designed to be intuitive. Just `import saka`. Complete examples can be found in [basic_usage.py](examples/basic_usage.py).

<details>
<summary><b>1. Tokenization & Normalization</b></summary>

```python
import saka

# Tokenization (Handles affixes, words, punctuation, URLs, mentions, hashtags, and emojis)
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

# Morphological Analysis (Handles compound words and affix fusion)
word = "mempertanggungjawabkan"
analysis = saka.analyze(word)
print(analysis["root"])  # 'tanggung jawab'

# Live KBBI Lookup (Real-time web scraping)
res = saka.query_kbbi("ajar")
# {'status': 'found', 'definitions': [...]}
```
</details>

<details>
<summary><b>3. Regional Stopwords</b></summary>

```python
import saka

# Supported: 'id', 'en', 'sunda', 'jawa', 'bali', 'minang', 'jaksel', 'batak', 'all'

# Get Batak stopwords
stops = saka.get_stopwords("batak")
print("do" in stops)  # True

# Get English stopwords
en_stops = saka.get_stopwords("en")
print("however" in en_stops)  # True
```
</details>

---

## Examples Directory

All reference scripts can be found in the `examples/` directory. Here is a comprehensive overview of their functionalities:

- **1. Core Usage and Utilities**
  - `basic_usage.py` — Introduction to the most frequently used features (tokenization, normalization, KBBI lookup, etc).
  - `full_core_integration_demo.py` — Combining a series of Saka core modules into a complete processing pipeline.
  - `async_usage.py` — Guide to using library features in an _Asynchronous_ environment.
  - `transactional_context_demo.py` — How to use transactional entity extraction functions.
  - `output_demo.py` — Offline formatting features to/from CSV/HTML Markdown using the `OutputFormatter` module.

- **2. Morphology and Analysis**
  - `morphology_advanced.py` — Advanced dissection case of the internal heuristics in Saka's affix *Analyzer*.
  - `stopwords_demo.py` — Advanced application of per-language _stopwords_ mode (including pure punctuation stripping).
  - `dict_translate_demo.py` — Executing literal word translation into custom regional language families.
  - `kbbi_demo.py` — Guide for delegating web KBBI _scraping_ to your terminal for up-to-date definitions.

- **3. Regional Plugin Ecosystem**
  - `sunda_plugin.py` — Full transliteration demo for Ngalagena script and local KBBI site fetching.
  - `jawa_plugin.py` — Use case for Latin transliteration to royal Nglegena alphabet script.
  - `bali_plugin.py` — Demonstration script for the Wreastra archipelago script system programmatically.

- **4. Agentic AI & LLM Parameters**
  - `multi_agent_edu_demo.py` — Environment configuration simulating several LLM intermediary agents cohesively.
  - `tool_calling_edu_demo.py` — AI Assistant wrapped in modular _Function/Tool Calling_ from Saka.
  - `prompt_optimization_demo.py` — Assembling carefully manipulated *prompt* instructions for modern language models (LLMs).

- **5. Saka-Eval (Fast Evaluation and Metrics)**
  - `benchmark_stack.py` — Basic execution mapping for stacked *Benchmark* evaluation schemes on local NLP engines.
  - `saka_eval_demo.py` — Example instantiation of the *Saka Evaluation pipeline* purely offline.
  - `saka_eval_huggingface_demo.py` — Standard accrued metric testing drawing Language NLP datasets from the _Hugging Face Hub_.

---

## Agentic AI & Prompting

Build LLM-based applications with full control. Complete examples: [output_demo.py](examples/output_demo.py) & [multi_agent_edu_demo.py](examples/multi_agent_edu_demo.py).

```python
import saka
from saka import Agent, OutputFormatter

# 1. Output Formatting (Save LLM Tokens)
# Format data to HTML/Markdown/CSV/JSON locally without calling an LLM
data = [{"word": "horas", "pos": "greeting", "meaning": "hello"}]
markdown_table = OutputFormatter.format(data, "markdown")

# 2. Structured Agent & Tool Calling
bot = Agent("Assistant", "Linguistic Expert")
bot.add_tool(name="check_meaning", desc="Check word meaning in KBBI", func=saka.query_kbbi)

# 3. Prompt Builder (Token Optimization)
# Build structured prompts for LLMs with text optimization options
prompt = saka.build_prompt(
    role="Analyst",
    task="Indonesian text classification",
    input_data="Text to classify...",
    optimize_text=True
)
```

---

## Saka-Eval Benchmark

Evaluate your model asynchronously. Example: [saka_eval_huggingface_demo.py](examples/saka_eval_huggingface_demo.py).

```python
import asyncio
from saka.evaluation.benchmarker import SakaEval

async def run():
    evaluator = SakaEval(task="sentiment")
    # Load dataset via config name ("sentiment" or "ner") or from Hugging Face Hub
    evaluator.load_hf_dataset("Muhammad-Ikhwan-Fathulloh/Saka-Eval", name="sentiment")

    # Evaluate model with text data and labels
    results = await evaluator.evaluate(model, text="text", label="label")
    print(f"Accuracy: {results['metrics']['accuracy']:.2%}")

asyncio.run(run())
```

---

## Dynamic Compound Handling

Saka-NLP automatically splits compound words using rules defined in `compounds.json`:

| Input             | Root                           |
| ----------------- | ------------------------------ |
| `menyebarluaskan` | `sebar luas`                   |
| `kerjasama`       | `kerja sama`                   |
| `hulunagara`      | `hulu nagara` (Sundanese)      |
| `bundokanduang`   | `bundo kanduang` (Minangkabau) |

---

## Regional Ecosystem

Saka-NLP provides deep support for various regional language families in Indonesia through literal translation dictionary features, morphology dissection, collections of _stopwords_, web dictionary *scraping* extractors, down to ancient/traditional script transliteration.

### 1. Sundanese, Javanese, and Balinese
These three languages possess the most complete plural feature support in the Saka ecosystem:
- **Lexicon & Specific Stopwords:** Contains internal vocabulary and sets of sentence complementary conjunctions for their respective languages.
- **Traditional Script Transliteration:** Converts sequences of Latin text back and forth to **Ngalagena (Sundanese)**, **Nglegena (Javanese)**, and **Wreastra (Balinese)** scripts.
- **Live Dictionary Scraper Modules:** Interactive compact APIs through `query_sundadigi()`, `query_sastra()`, and `query_basabali()` that dissect direct *backends* and extract grammar parameters from giant local digital treasury sites (SundaDigi, Sastra.org, BASAbali Wiki).

```python
import saka
import asyncio

# 1. Lexicon & Morphology Analysis
print(saka.analyze("geulis")["regional_matches"])     # ['sunda'] (beautiful)
print(saka.analyze("nglegena")["regional_matches"])   # ['jawa']
print(saka.analyze("rahajeng")["regional_matches"])   # ['bali'] (safe/greetings)

# 2. Latin ↔ Traditional Script Transliteration
print(saka.latin_to_aksara_sunda("sampurasun"))       # ᮞᮙ᮪ᮕᮥᮛᮞᮥᮔ᮪

# 3. Actual Dictionary Meaning Scraping
jawa_def = asyncio.run(saka.query_sastra("mangan"))
print(jawa_def["definitions"][0])                     # 'makan; memakan ...' (eat)
```

### 2. Minangkabau
The core morphological analysis support is seamlessly integrated with Minangkabau text functionalities:
- **Lexicon & Special Word Handling:** Automatic *root-word* splitting with regional combined words. The hybrid system natively recognizes cultural consecutive terms.
- **Minang Stopwords Filter:** Feature to reduce popular Minangkabau filler words (*cinto*, *nan*, *jo*, etc).

```python
import saka

# Special / consecutive word analysis (example: bundo kanduang)
print(saka.analyze("bundokanduang")["regional_matches"]) # ['minang']
print(saka.analyze("bundokanduang")["root"])             # 'bundo kanduang'

# Pruning regional functional words (Minang Stopwords)
minang_teks = saka.remove_stopwords("rancak bana pado inyo", lang="minang")
print(minang_teks)                                       # 'rancak bana'
```

### 3. Batak

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
- [KamusBatak.Com](https://www.kamusbatak.com/) — Online Batak–Indonesian Dictionary

<details>
<summary><b>Script Details (Sundanese, Javanese, Balinese)</b></summary>

### Sundanese Script (Ngalagena)
| Latin | Script | Latin | Script |
| ----- | ------ | ----- | ------ |
| ka    | ᮊ      | ga    | ᮌ      |
| nga   | ᮍ      | ca    | ᮎ      |
| ja    | ᮏ      | nya   | ᮑ      |
| ta    | ᮒ      | da    | ᮓ      |
| na    | ᮔ      | pa    | ᮕ      |
| ba    | ᮘ      | ma    | ᮙ      |
| ya    | ᮚ      | ra    | ᮛ      |
| la    | ᮜ      | wa    | ᮝ      |
| sa    | ᮞ      | ha    | ᮠ      |

### Javanese Script (Nglegena)
| Latin | Script | Latin | Script |
| ----- | ------ | ----- | ------ |
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

### Balinese Script (Wreastra)
| Latin | Script | Latin | Script |
| ----- | ------ | ----- | ------ |
| ha    | ᬳ      | na    | ᬦ      |
| ca    | ᬘ      | ra    | ᬭ      |
| ka    | ᬓ      | da    | ᬤ      |
| ta    | ᬢ      | sa    | ᬲ      |
| wa    | ᬯ      | la    | ᬮ      |
| ma    | ᬫ      | ga    | ᬕ      |
| ba    | ᬩ      | nga   | ᬗ      |
| pa    | ᬧ      | ja    | ᬚ      |
| ya    | ᬬ      | nya   | ᬜ      |

*(Full table along with modifiers/vowel signs available in [Web Documentation](http://saka-nlp.netlify.app/))*
</details>

---

## CLI & Citation

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
  version   = {0.3.0},
  doi       = {10.5281/zenodo.20092640},
  url       = {https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP}
}
```

---

## Sources & Credits

Saka-NLP is built on the following open research and datasets. We thank the researchers and contributors:

| Category      | Source                                                                                                                                    | Description                                                                                           |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **Datasets**  | [Carant-AI](https://huggingface.co/datasets/carant-ai/indonesian_sentiment_dataset)                                                       | Indonesian Sentiment Dataset                                                                          |
|               | [Kiuyha](https://huggingface.co/datasets/Kiuyha/surabaya-ner-dataset)                                                                     | Surabaya NER Dataset                                                                                  |
|               | [IndoNLU](https://huggingface.co/datasets/indonlp/indonlu)                                                                                | Indonesian NLP Standard Benchmark                                                                     |
|               | **Stopwords**: [Tala Dataset](https://github.com/masdevid/ID-Stopwords)                                                                   | Adopts the legendary corpus of the Tala Stopwords Dataset.                                            |
|               | **Slang Words**: [Twitter COVID-19 Lexicon](https://github.com/evanmartua34/Twitter-COVID19-Indonesia-Sentiment-Analysis---Lexicon-Based) | Utilizes corpus from the Twitter COVID-19 Sentiment Lexicon.                                          |
| **Lexicons**  | **SundaDigi**: [SundaDigi.com](https://sundadigi.com/)                                                                                    | Uses the digital dictionary SundaDigi for translations & references of regional Sundanese vocabulary. |
|               | **KBBI (Kamus Besar Bahasa Indonesia)**: [KBBI Daring](https://kbbi.kemendikdasmen.go.id/)                                                | Data netted sourced directly from the credential portal of KBBI Daring Kemendikdasmen.                |
|               | [Sastra.org](https://sastra.org)                                                                                                          | Javanese Lexicon                                                                                      |
|               | [BASAbali Wiki](https://basabali.org)                                                                                                     | Balinese Lexicon                                                                                      |
|               | [KamusBatak.Com](https://www.kamusbatak.com)                                                                                              | Batak Dictionary                                                                                      |
| **Grammars**  | Nababan (1981). *A Grammar of Toba-Batak*. [DOI:10.15144/PL-D37](https://doi.org/10.15144/PL-D37)                                         | Toba Batak Grammar                                                                                    |
|               | Woollams (1996). *A Grammar of Karo Batak*. [DOI:10.15144/PL-C130](https://doi.org/10.15144/PL-C130)                                      | Karo Batak Grammar                                                                                    |
|               | Bird et al. (2009). *NLTK*. [nltk.org](https://www.nltk.org/)                                                                             | English Stopwords                                                                                     |
|               | Pedregosa et al. (2011). *Scikit-learn*. JMLR 12.                                                                                         | English Stopwords and Evaluation Metrics                                                              |
| **Libraries** | [HuggingFace](https://huggingface.co)                                                                                                     | Dataset & Model Hub Ecosystem                                                                         |
|               | [scikit-learn](https://scikit-learn.org)                                                                                                  | Evaluation Metrics                                                                                    |
|               | [Emoji/Emot](https://pypi.org/project/emoji/)                                                                                             | Social Media Text Handling                                                                            |

---

## Support
- **Architect:** [Muhammad Ikhwan Fathulloh](https://github.com/Muhammad-Ikhwan-Fathulloh)
- **License:** [MIT License](LICENSE)
- **Support:** [Saweria](https://saweria.co/ikhwanfathulloh) | [Trakteer](https://trakteer.id/kexnp7aorpxyaz70y7gn)
