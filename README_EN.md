# Saka: Indonesian NLP with Prompting and Agentic AI Support 🇮🇩

[**Bahasa Indonesia**](README.md) | [**English**](README_EN.md)

[![PyPI version](https://img.shields.io/pypi/v/saka-nlp.svg)](https://pypi.org/project/saka-nlp/)
[![Documentation](https://img.shields.io/badge/docs-live-brightgreen)](http://saka-nlp.netlify.app/)
[![Colab](https://img.shields.io/badge/Colab-Playground-orange)](https://colab.research.google.com/drive/1MJ6fwJruR6B-UVT1sqKyqWXukjGe2UCH?usp=sharing)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20092640.svg)](https://doi.org/10.5281/zenodo.20092640)

Philosophically, **Saka** (in Javanese/Sundanese) means "pillar" or "support". **Saka-NLP** is built to be a solid modern *architectural framework* for Indonesian and regional language processing.

Saka-NLP supports *asynchronous processing*, has modular *plug-and-play* components, and utilizes heuristic functions with integration from various trusted data sources (slang lexicons, stopwords, and direct official KBBI extraction).

---

### 🌐 Links
*   **Official Website**: [saka-nlp.netlify.app](http://saka-nlp.netlify.app/)
*   **Google Colab Playground**: [Try it on Colab](https://colab.research.google.com/drive/1MJ6fwJruR6B-UVT1sqKyqWXukjGe2UCH?usp=sharing)
*   **PyPI Package**: [saka-nlp on PyPI](https://pypi.org/project/saka-nlp/)

---

## ✨ Key Features

*   **Asynchronous Processing**: Equipped with `async_*` companion methods (e.g., `async_tokenize`) using `asyncio` for efficient large dataset processing without blocking.
*   **Plug-and-Play Components**: Flexible choice for stemming engines, tokenization, or integrating third-party plugins.
*   **Heuristic Morphology Analyzer**: Detects prefix and suffix patterns using Indonesian grammar rules with **Early Stopping Validation** against regional lexicons and **Morphophonemic Restructuring**.
*   **Live KBBI Scraper**: Direct extraction of word meanings from the official *Kamus Besar Bahasa Indonesia (KBBI)*.
*   **Advanced Prompting & Agentic AI**: Tools for building structured LLM prompts (Role, Task, Context, Constraint) with support for **Multi-Agent Orchestration** and **Dynamic Tool Calling**.
*   **Regional Language Support**: Includes support for regional scripts like **Sundanese**, **Javanese**, and **Balinese** (Hanacaraka) transliteration.
*   **Emoji & Emoticon Handling**: Full support for converting Unicode emojis (3,800+) and standard emoticons to Indonesian text.

---

## 🚀 Installation Guide

Ensure you are using **Python 3.8 or newer**.

### Option 1: Install via PyPI (Recommended)
```bash
pip install saka-nlp
```

### Option 2: Install from Source
```bash
git clone https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP.git
cd Saka-NLP
pip install -e .
```

---

## 📖 Core Module Usage

### 0. Check Version
```python
import saka
print(saka.__version__)
# Output: 0.2.3
```

### 1. Smart Tokenization
```python
import saka
text = "Learning while sharing in the connectivity era."
tokens = saka.tokenize(text)
print(tokens)
# Output: ['Learning', 'while', 'sharing', 'in', 'the', 'connectivity', 'era']
```

### 2. Slang Normalization
```python
import saka
normalized = saka.normalize("klo gimana gw")
print(normalized)
# Output: 'kalau bagaimana saya'
```

### 3. Morphological Analysis
```python
import saka
print(saka.analyze("menyebarluaskan"))
# Output: {'root': 'sebar luas', 'prefixes': ['meny'], 'suffixes': ['kan'], 'type': 'unknown', 'regional_matches': []}
```

### 4. Emoji & Emoticon Handling
```python
import saka
text = "Bilingual README is ready! 😊 :)"
print(saka.demojize(text))
# Output: 'Bilingual README is ready! wajah tersenyum dengan mata bahagia :)'

print(saka.replace_emoticons(text))
# Output: 'Bilingual README is ready! 😊 Happy face or smiley'
```

### 5. Advanced Prompting & Agentic AI
```python
from saka import Agent

bot = Agent("Assistant", "Help students.")
bot.add_tool(
    name="get_grade",
    desc="Fetch grade",
    params={"name": "string"},
    func=lambda name: f"Grade for {name}: 90"
)
print(bot.call_tool("get_grade", {"name": "Budi"}))
```

---

## 🏛️ Regional Scripts Detail
*(See primary README.md for full Hanacaraka tables)*

---

## 🛠️ Performance Benchmarks
Run the benchmark script:
```powershell
$env:PYTHONPATH = "."; python examples/benchmark_stack.py
```
**Results (v0.2.3):** Average **0.08ms** per text.

---

## 📚 Citation

If you use **Saka-NLP** in your research, please cite it as:

### BibTeX
```bibtex
@software{Fathulloh_Saka-NLP_2026,
  author = {Fathulloh, Muhammad Ikhwan},
  title = {{Saka-NLP: Indonesian Language Processing with Prompting and Agentic AI Support}},
  year = {2026},
  version = {0.2.3},
  doi = {10.5281/zenodo.20092640},
  url = {https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP}
}
```

---

## ❤️ Credits & Support
* **Framework Architect**: [Muhammad Ikhwan Fathulloh](https://github.com/Muhammad-Ikhwan-Fathulloh)
* **License**: [MIT License](LICENSE)
