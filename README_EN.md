# Saka: Indonesian NLP with Prompting and Agentic AI Support 🇮🇩 v0.2.5

[**Bahasa Indonesia**](README.md) | [**English**](README_EN.md)

[![PyPI version](https://img.shields.io/pypi/v/saka-nlp.svg)](https://pypi.org/project/saka-nlp/)
[![Documentation](https://img.shields.io/badge/docs-live-brightgreen)](http://saka-nlp.netlify.app/)
[![Colab](https://img.shields.io/badge/Colab-Playground-orange)](https://colab.research.google.com/drive/1MJ6fwJruR6B-UVT1sqKyqWXukjGe2UCH?usp=sharing)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20092640.svg)](https://doi.org/10.5281/zenodo.20092640)

**Saka** (Javanese/Sundanese: *Pillar*) is a modern architectural framework for Indonesian and regional language processing, built with asynchronous, modular, and intelligent design principles.

---

## 📌 Table of Contents
- [Saka: Indonesian NLP with Prompting and Agentic AI Support 🇮🇩 v0.2.5](#saka-indonesian-nlp-with-prompting-and-agentic-ai-support-v025)
  - [📌 Table of Contents](#-table-of-contents)
  - [✨ Key Features](#-key-features)
  - [🚀 Installation](#-installation)
  - [📖 Basic Usage](#-basic-usage)
  - [🤖 Agentic AI \& Prompting](#-agentic-ai--prompting)
  - [📊 Saka-Eval Benchmark](#-saka-eval-benchmark)
  - [🌏 Regional Ecosystem](#-regional-ecosystem)
  - [🛠️ CLI \& Citation](#️-cli--citation)
  - [🗄️ Sources \& Credits](#️-sources--credits)
  - [❤️ Support](#️-support)

---

## ✨ Key Features

| Feature                   | Description                                                         |
| ------------------------- | ------------------------------------------------------------------- |
| ⚡ **Async Processing**    | Non-blocking processing for large-scale datasets.                   |
| 🧩 **Modular Design**      | Plug-and-play components for easy integration.                      |
| 🧠 **Morphology Analyzer** | Hybrid affix analysis with *Morphophonemic Restructuring*.          |
| 📖 **Live KBBI**           | Official Indonesian dictionary (KBBI) word meaning extraction.      |
| 🤖 **Agentic AI**          | LLM prompt orchestration, Multi-Agent management, and Tool Calling. |
| 🔠 **Regional Scripts**    | Sundanese, Javanese, and Balinese (Hanacaraka) transliteration.     |

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

## 📖 Basic Usage

Saka-NLP is designed to be intuitive. Just `import saka`. Complete examples can be found in [**basic_usage.py**](examples/basic_usage.py).

<details>
<summary><b>1. Tokenization & Normalization</b></summary>

```python
import saka

# Tokenize (Handles affixes & punctuation)
text = "Learning NLP in the 5G era is fun!"
tokens = saka.tokenize(text) 
# ['Learning', 'NLP', 'in', 'the', '5G', 'era', 'is', 'fun', '!']

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

# Live KBBI Search (Real-time Web Scraping)
res = saka.query_kbbi("belajar")
# {'status': 'found', 'definitions': [...]}
```
</details>

<details>
<summary><b>3. Regional Stopwords</b></summary>

```python
import saka
# Supports: id, sunda, jawa, bali, minang, en, jaksel, all
stops = saka.get_stopwords("sunda")
print("eta" in stops) # True
```
</details>

---

## 🤖 Agentic AI & Prompting

Build LLM-powered applications with full control. Full examples: [**output_demo.py**](examples/output_demo.py) & [**multi_agent_edu_demo.py**](examples/multi_agent_edu_demo.py).

```python
import saka
from saka import Agent, OutputFormatter

# 1. Output Formatting (Save LLM Tokens!)
data = [{"word": "saka", "pos": "noun"}]
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

Evaluate your models asynchronously. Example: [**saka_eval_huggingface_demo.py**](examples/saka_eval_huggingface_demo.py).

```python
from saka.evaluation.benchmarker import SakaEval

evaluator = SakaEval(task="sentiment")
# Load via config name ("sentiment" or "ner")
evaluator.load_hf_dataset("Muhammad-Ikhwan-Fathulloh/Saka-Eval", name="sentiment")

results = await evaluator.evaluate(model, text="text", label="label")
print(f"Accuracy: {results['metrics']['accuracy']:.2%}")
```

---

## 🌏 Regional Ecosystem

Deep support for regional languages (Dictionaries & Scripts).

<details>
<summary><b>Click to show script details (Sundanese, Javanese, Balinese)</b></summary>

### Sundanese Script (Ngalagena)
| Latin | Script | Latin | Script |
| ----- | ------ | ----- | ------ |
| ha    | ᮠ      | na    | ᮔ      |
| ...   | ...    | ...   | ...    |

### Javanese Script (Nglegena)
| Latin | Script | Latin | Script |
| ----- | ------ | ----- | ------ |
| ha    | ꦲ      | na    | ꦤ      |
| ...   | ...    | ...   | ...    |

*(Full tables available at [Web Documentation](http://saka-nlp.netlify.app/))*
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
  author = {Fathulloh, Muhammad Ikhwan},
  title = {{Saka-NLP: Indonesian NLP Toolkit}},
  year = {2026},
  version = {0.2.5},
  doi = {10.5281/zenodo.20092640},
  url = {https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP}
}
```

---

## 🗄️ Sources & Credits

Saka-NLP is built on the foundation of the following research and open datasets. We are grateful to the researchers and contributors:

| Category      | Source                                                                              | Description                  |
| ------------- | ----------------------------------------------------------------------------------- | ---------------------------- |
| **Datasets**  | [Carant-AI](https://huggingface.co/datasets/carant-ai/indonesian_sentiment_dataset) | Indonesian Sentiment Dataset |
|               | [Kiuyha](https://huggingface.co/datasets/Kiuyha/surabaya-ner-dataset)               | Surabaya NER Dataset         |
|               | [IndoNLU](https://huggingface.co/datasets/indonlp/indonlu)                          | Benchmark Standards          |
|               | [Tala Dataset](https://github.com/masdevid/ID-Stopwords)                            | Indonesian Stopwords         |
| **Lexicons**  | [SundaDigi](https://sundadigi.com)                                                  | Sundanese Digital Dictionary |
|               | [Sastra.org](https://sastra.org)                                                    | Javanese Lexicon             |
|               | [BASAbali Wiki](https://basabali.org)                                               | Balinese Lexicon             |
| **Libraries** | [HuggingFace](https://huggingface.co)                                               | Datasets & Hub Ecoystem      |
|               | [scikit-learn](https://scikit-learn.org)                                            | Evaluation Metrics           |
|               | [Emoji/Emot](https://pypi.org/project/emoji/)                                       | Social Media Text Handling   |

---

## ❤️ Support
- **Architect**: [Muhammad Ikhwan Fathulloh](https://github.com/Muhammad-Ikhwan-Fathulloh)
- **License**: [MIT License](LICENSE)
- **Support**: [Saweria](https://saweria.co/ikhwanfathulloh) | [Trakteer](https://trakteer.id/kexnp7aorpxyaz70y7gn)
