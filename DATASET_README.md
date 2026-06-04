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
configs:
  - config_name: sentiment
    data_files:
      - split: train
        path: sentiment/saka_sentiment_eval.jsonl
    default: true
  - config_name: ner
    data_files:
      - split: train
        path: ner/saka_ner_eval.jsonl
---

# Saka-Eval Benchmark Dataset

## Dataset Description
Saka-Eval is a curated benchmark dataset for evaluating Indonesian NLP models, particularly focused on colloquial language, public services, and government entities.

This dataset was generated as part of the [`Saka-NLP`](https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP) ecosystem to provide a standardized way to measure model performance in real-world Indonesian contexts.

### Task Summaries
- **Sentiment Analysis** (`sentiment`): 100 samples of public service reviews and general social media text.
- **Named Entity Recognition** (`ner`): 100 samples focusing on locations and government administrative entities (Surabaya context).

## How to Use
You can load this dataset directly using the HuggingFace `datasets` library.

### Sentiment Analysis
```python
from datasets import load_dataset

dataset = load_dataset("Muhammad-Ikhwan-Fathulloh/Saka-Eval", "sentiment")
print(dataset['train'][0])
```

### NER
```python
from datasets import load_dataset

dataset = load_dataset("Muhammad-Ikhwan-Fathulloh/Saka-Eval", "ner")
print(dataset['train'][0])
```

### Using with Saka-NLP SakaEval
```python
from saka.evaluation.benchmarker import SakaEval

evaluator = SakaEval(task="sentiment")
evaluator.load_hf_dataset(
    path="Muhammad-Ikhwan-Fathulloh/Saka-Eval",
    name="sentiment"
)
```

## Dataset Structure

### Sentiment (`sentiment` config)
| Column   | Type     | Description                           |
| -------- | -------- | ------------------------------------- |
| `text`   | `string` | The raw text for classification.      |
| `label`  | `string` | `positive`, `negative`, or `neutral`. |
| `source` | `string` | The original source of the data.      |

### NER (`ner` config)
| Column     | Type               | Description                                      |
| ---------- | ------------------ | ------------------------------------------------ |
| `text`     | `string`           | The full sentence.                               |
| `entities` | `list` of `struct` | A list of entity spans containing:               |
|            |                    | - `start`: Character start index.                |
|            |                    | - `end`: Character end index.                    |
|            |                    | - `label`: Entity type (LOC, ORG, PERSON, etc.). |
| `source`   | `string`           | The original source of the data.                 |

## Source Datasets & Attribution

This benchmark dataset is curated from the following publicly available datasets and resources. We sincerely thank the original authors for their contributions to Indonesian NLP:

| Source           | Description                                                                                                      | Link                                                                                                             |
| ---------------- | ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Carant-AI**    | Indonesian Sentiment Dataset — multilabel sentiment corpus covering reviews, social media, and public discourse. | [carant-ai/indonesian_sentiment_dataset](https://huggingface.co/datasets/carant-ai/indonesian_sentiment_dataset) |
| **Kiuyha**       | Surabaya NER Dataset — named entity recognition corpus focused on Surabaya-region social media and news text.    | [Kiuyha/surabaya-ner-dataset](https://huggingface.co/datasets/Kiuyha/surabaya-ner-dataset)                       |
| **IndoNLU Team** | IndoNLU benchmark — the foundational Indonesian NLU benchmark establishing evaluation standards.                 | [indonlp/indonlu](https://huggingface.co/datasets/indonlp/indonlu)                                               |

### Libraries & Tools Used
| Library                     | Purpose                                                       | Link                                                                                                                                                                                   |
| --------------------------- | ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🤗 **Hugging Face Datasets** | Dataset hosting, loading, and processing.                     | [huggingface.co/docs/datasets](https://huggingface.co/docs/datasets)                                                                                                                   |
| 🤗 **Hugging Face Hub**      | Dataset repository management and upload.                     | [huggingface.co/docs/huggingface_hub](https://huggingface.co/docs/huggingface_hub)                                                                                                     |
| **scikit-learn**            | Evaluation metrics (accuracy, F1-score).                      | [scikit-learn.org](https://scikit-learn.org)                                                                                                                                           |
| **Saka-NLP**                | Indonesian NLP library with prompting and agentic AI support. | [GitHub](https://github.com/Muhammad-Ikhwan-Fathulloh/Saka-NLP) · [PyPI](https://pypi.org/project/saka-nlp/) · [DOI: 10.5281/zenodo.15308308](https://doi.org/10.5281/zenodo.15308308) |

## Citation

If you use this dataset in your research, please cite:

```bibtex
@dataset{saka_eval_2026,
  title     = {Saka-Eval: Indonesian NLP Benchmark Dataset},
  author    = {Muhammad Ikhwan Fathulloh},
  year      = {2026},
  publisher = {Hugging Face},
  url       = {https://huggingface.co/datasets/Muhammad-Ikhwan-Fathulloh/Saka-Eval}
}
```

## License

This dataset is released under the [MIT License](https://opensource.org/licenses/MIT).
