import asyncio
import os
import json
from saka.evaluation.benchmarker import SakaEval
from saka.core.agent import Agent
from saka.core.normalizer import normalize

# Wrapper for Saka-NLP features to be used in SakaEval
class SakaNLPPredictor:
    def __init__(self, name="SakaAgent"):
        self.name = name
        # We can use Saka Agent to handle reasoning/prediction
        self.agent = Agent(name=name)
        
    def predict(self, text: str) -> str:
        """
        In a real scenario, this would call an LLM via Saka Agent.
        Here we demonstrate the workflow: Normalize -> Analyze -> Predict.
        """
        # 1. Normalize text (handle slang, emoticons, etc.)
        norm_text = normalize(text)
        
        # 2. Heuristic-based prediction for demonstration
        # In a production setup, you'd use self.agent.run(prompt)
        text_lower = norm_text.lower()
        if any(word in text_lower for word in ["bagus", "mantap", "puas", "terima kasih", "cepat", "oke"]):
            return "positive"
        elif any(word in text_lower for word in ["buruk", "kecewa", "lambat", "jelek", "lama", "kurang"]):
            return "negative"
        return "neutral"

    def predict_ner(self, tokens: list) -> list:
        # Placeholder for NER using Saka's morphological analyzer or agent
        return ["O"] * len(tokens)

async def main():
    print("=== Saka-Eval + Saka-NLP Features Demo ===")
    
    # 1. Initialize SakaEval for Sentiment Analysis
    evaluator = SakaEval(task="sentiment")
    
    # 2. Load dataset from the HuggingFace repository using config name
    repo_id = "Muhammad-Ikhwan-Fathulloh/Saka-Eval"
    
    print(f"Syncing with HuggingFace Repo: {repo_id}...")
    try:
        # Use config name "sentiment" instead of data_files to avoid schema issues
        evaluator.load_hf_dataset(path=repo_id, name="sentiment")
    except Exception as e:
        print(f"Error loading remote dataset: {e}")
        # Fallback to local
        if os.path.exists("data/saka_sentiment_eval.jsonl"):
            from datasets import Dataset
            with open("data/saka_sentiment_eval.jsonl", "r", encoding="utf-8") as f:
                data = [json.loads(line) for line in f]
            evaluator.dataset = Dataset.from_list(data)
            print(f"Using local file: data/saka_sentiment_eval.jsonl")
        else:
            return

    # 3. Initialize our Saka-NLP powered predictor
    # This predictor uses Saka's Normalizer and Agent structure
    predictor = SakaNLPPredictor()

    # 4. Run evaluation
    print("\n[Saka-NLP] Running benchmark evaluation...")
    results = await evaluator.evaluate(predictor, text="text", label="label")

    # 5. Result Display
    print("\n" + "="*30)
    print("      BENCHMARK REPORT      ")
    print("="*30)
    print(f"Model/Agent : {predictor.name}")
    print(f"Accuracy    : {results['metrics']['accuracy']:.2%}")
    print(f"F1-Score    : {results['metrics']['f1_score']:.2%}")
    print(f"Processed in: {results['execution_time_seconds']}s")
    print("="*30)

    # 6. Save results
    report_path = "saka_nlp_benchmark_report.json"
    evaluator.save_report(report_path)

if __name__ == "__main__":
    asyncio.run(main())
