import asyncio
import json
import time
from typing import List, Dict, Any, Optional, Callable, Union
from datetime import datetime
try:
    from datasets import load_dataset
except ImportError:
    load_dataset = None

class SakaEval:
    """
    SakaEval: Benchmark module for Saka-NLP.
    Supports Sentiment Analysis, NER, and Question Answering tasks.
    """
    
    def __init__(self, task: str = "sentiment"):
        self.task = task.lower()
        if self.task not in ["sentiment", "ner", "qa"]:
            raise ValueError(f"Unsupported task: {self.task}. Choose from: sentiment, ner, qa")
        
        self.dataset = None
        self.results = {}
        self.metrics = {"accuracy": 0.0, "f1_score": 0.0}

    def load_hf_dataset(self, path: str, name: Optional[str] = None, split: str = "train", data_files: Optional[Union[str, List[str]]] = None):
        """Loads a dataset from HuggingFace Hub."""
        if not load_dataset:
            raise ImportError("The 'datasets' library is required. Install it using: pip install datasets")
        
        print(f"[SakaEval] Loading dataset '{path}' (split: {split}, files: {data_files})...")
        self.dataset = load_dataset(path, name, split=split, data_files=data_files)
        print(f"[SakaEval] Successfully loaded {len(self.dataset)} samples.")

    async def _evaluate_sentiment(self, model: Any, input_col: str, label_col: str):
        """Internal async logic for Sentiment Analysis evaluation."""
        total = len(self.dataset)
        correct = 0
        y_true = []
        y_pred = []

        for i, item in enumerate(self.dataset):
            text = item[input_col]
            true_label = item[label_col]
            
            # Non-blocking model inference (assuming model.predict is or can be made async)
            # In a real scenario, we might use run_in_executor if predict is blocking
            loop = asyncio.get_event_loop()
            prediction = await loop.run_in_executor(None, model.predict, text)
            
            y_true.append(true_label)
            y_pred.append(prediction)
            
            if prediction == true_label:
                correct += 1
            
            if (i + 1) % 10 == 0 or (i + 1) == total:
                print(f"[SakaEval] Processed {i+1}/{total} samples...")

        self.metrics["accuracy"] = correct / total
        self.metrics["f1_score"] = self._calculate_f1(y_true, y_pred)

    async def _evaluate_ner(self, model: Any, input_col: str, label_col: str):
        """Internal async logic for NER evaluation."""
        # Simplified NER evaluation logic
        # In practice, this would involve sequence labeling metrics
        total_tokens = 0
        correct_tokens = 0
        
        for item in self.dataset:
            tokens = item[input_col]
            true_tags = item[label_col]
            
            loop = asyncio.get_event_loop()
            pred_tags = await loop.run_in_executor(None, model.predict_ner, tokens)
            
            total_tokens += len(true_tags)
            for t, p in zip(true_tags, pred_tags):
                if t == p:
                    correct_tokens += 1
                    
        self.metrics["accuracy"] = correct_tokens / total_tokens if total_tokens > 0 else 0
        self.metrics["f1_score"] = self.metrics["accuracy"] # Placeholder for complex NER F1

    async def _evaluate_qa(self, model: Any, context_col: str, question_col: str, answer_col: str):
        """Internal async logic for QA evaluation."""
        exact_match = 0
        total = len(self.dataset)
        
        for item in self.dataset:
            context = item[context_col]
            question = item[question_col]
            true_answer = item[answer_col]
            
            loop = asyncio.get_event_loop()
            pred_answer = await loop.run_in_executor(None, model.answer_question, context, question)
            
            if pred_answer.strip().lower() == true_answer.strip().lower():
                exact_match += 1
                
        self.metrics["accuracy"] = exact_match / total
        self.metrics["f1_score"] = exact_match / total # Placeholder for SQuAD-style F1

    def _calculate_f1(self, y_true: list, y_pred: list) -> float:
        """Manual F1-score calculation (Weighted) to avoid heavy dependencies if possible."""
        # This is a simplified version. For production use scikit-learn.
        try:
            from sklearn.metrics import f1_score
            return float(f1_score(y_true, y_pred, average='weighted'))
        except ImportError:
            # Fallback to accuracy if sklearn is missing (not ideal but safe for structure)
            return self.metrics["accuracy"]

    async def evaluate(self, model: Any, **column_mapping):
        """
        Main entry point for evaluation.
        column_mapping: mapping of expected columns (e.g. text='sentence', label='label').
        """
        if not self.dataset:
            raise ValueError("Dataset not loaded. Call load_hf_dataset() first.")
        
        start_time = time.time()
        
        if self.task == "sentiment":
            await self._evaluate_sentiment(model, column_mapping['text'], column_mapping['label'])
        elif self.task == "ner":
            await self._evaluate_ner(model, column_mapping['text'], column_mapping['label'])
        elif self.task == "qa":
            await self._evaluate_qa(model, column_mapping['context'], column_mapping['question'], column_mapping['answer'])
        
        end_time = time.time()
        self.results = {
            "task": self.task,
            "timestamp": datetime.now().isoformat(),
            "execution_time_seconds": round(end_time - start_time, 4),
            "metrics": self.metrics
        }
        return self.results

    def save_report(self, filename: str = "benchmark_report.json"):
        """Saves evaluation results to a JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=4, ensure_ascii=False)
        print(f"[SakaEval] Report saved to '{filename}'.")
