---
annotations_creators:
- found
language:
- id
language_creators:
- found
license:
- mit
multilinguality:
- monolingual
pretty_name: Saka-Eval Benchmark
size_categories:
- n<1K
source_datasets:
- indonlp/indonlu
- Kiuyha/surabaya-ner-dataset
- carant-ai/indonesian_sentiment_dataset
task_categories:
- text-classification
- token-classification
task_ids:
- sentiment-analysis
- named-entity-recognition
---

# Saka-Eval Benchmark Dataset

## Dataset Description
Saka-Eval is a curated benchmark dataset for evaluating Indonesian NLP models, particularly focused on colloquial language, public services, and government entities.

This dataset was generated as part of the `Saka-NLP` ecosystem to provide a standardized way to measure model performance in real-world Indonesian contexts.

### Task Summaries
- **Sentiment Analysis**: 100 samples of public service reviews and general social media text.
- **Named Entity Recognition (NER)**: 100 samples focusing on locations and government administrative entities (Surabaya context).

## How to Use
You can load this dataset directly using the HuggingFace `datasets` library.

### Sentiment Analysis
```python
from datasets import load_dataset

dataset = load_dataset("Muhammad-Ikhwan-Fathulloh/Saka-Eval", data_files="sentiment/saka_sentiment_eval.jsonl")
print(dataset['train'][0])
```

### NER
```python
from datasets import load_dataset

dataset = load_dataset("Muhammad-Ikhwan-Fathulloh/Saka-Eval", data_files="ner/saka_ner_eval.jsonl")
print(dataset['train'][0])
```

## Dataset Structure
### Sentiment
- `text`: The raw text for classification.
- `label`: `positive`, `negative`, or `neutral`.
- `source`: The original source of the data.

### NER
- `text`: The full sentence.
- `entities`: A list of spans containing:
    - `start`: Character start index.
    - `end`: Character end index.
    - `label`: The entity type (LOC, ORG, etc.).

## Contribution & Sources
Special thanks to the original authors of the source datasets:
- **Carant-AI** for Indonesian Sentiment data.
- **Kiuyha** for Surabaya NER data.
- **IndoNLU Team** for benchmarking standards.
