# Saka: Indonesian NLP with Prompting and Agentic AI Support 🇮🇩

[**Bahasa Indonesia**](README.md) | [**English**](README_EN.md)

[![PyPI version](https://img.shields.io/pypi/v/saka-nlp.svg)](https://pypi.org/project/saka-nlp/)
[![Documentation](https://img.shields.io/badge/docs-live-brightgreen)](http://saka-nlp.netlify.app/)
[![Colab](https://img.shields.io/badge/Colab-Playground-orange)](https://colab.research.google.com/drive/1MJ6fwJruR6B-UVT1sqKyqWXukjGe2UCH?usp=sharing)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20092640.svg)](https://doi.org/10.5281/zenodo.20092640)

**Saka** (Javanese/Sundanese: *Pillar*) is a modern architectural framework for Indonesian and regional language processing, built with asynchronous, modular, and intelligent design principles.

---

## 📌 Table of Contents
- [✨ Key Features](#-key-features)
- [🚀 Installation](#-installation)
- [📖 Basic Usage](#-basic-usage)
- [🤖 Agentic AI & Prompting](#-agentic-ai--prompting)
- [📊 Saka-Eval Benchmark](#-saka-eval-benchmark)
- [🌏 Regional Ecosystem](#-regional-ecosystem)
- [🛠️ CLI & Citation](#️-cli--citation)

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

Saka-NLP is designed to be intuitive. Just `import saka`.

<details>
<summary><b>1. Tokenization & Normalization</b></summary>

```python
import saka

# Tokenize
tokens = saka.tokenize("Halo, apa kabar?") 
# ['Halo', ',', 'apa', 'kabar', '?']

# Slang Normalization
normalized = saka.normalize("klo gimana gw") 
# 'kalau bagaimana saya'
```
</details>

<details>
<summary><b>2. Morphology & KBBI</b></summary>

```python
import saka

# Morphological Analysis (Handles compound words & fusion)
print(saka.analyze("menyebarluaskan"))
# {'root': 'sebar luas', ...}

# Live KBBI Search
res = saka.query_kbbi("belajar")
```
</details>

<details>
<summary><b>3. Regional Stopwords</b></summary>

```python
import saka
# Supports: id, sunda, jawa, bali, en, jaksel
stops = saka.get_stopwords("sunda")
```
</details>

---

## 🤖 Agentic AI & Prompting

Build LLM-powered applications with full control over prompts and outputs.

```python
import saka

# 1. Token Optimization via Local Formatting
data = [{"id": 1, "text": "Saka"}]
output = saka.OutputFormatter.format(data, "json")

# 2. Structured Prompt Builder
prompt = saka.build_prompt(role="Analyst", task="Classification", input_data="Text...")

# 3. Agent & Tool Calling
bot = saka.Agent("Assistant", "Helping users")
bot.add_tool(name="calc", desc="Multiply", func=lambda x: x*2)
```

---

## 📊 Saka-Eval Benchmark

Evaluate your NLP models with standard Indonesian datasets asynchronously.

```python
from saka.evaluation.benchmarker import SakaEval

evaluator = SakaEval(task="sentiment")
evaluator.load_hf_dataset("Muhammad-Ikhwan-Fathulloh/Saka-Eval")

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
