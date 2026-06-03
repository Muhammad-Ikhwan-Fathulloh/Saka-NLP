import asyncio
from saka.evaluation import SakaEval

class DummyModel:
    """A dummy model for demonstration purposes."""
    def predict(self, text: str) -> int:
        # Returns a random label (0 or 1)
        import random
        return random.randint(0, 1)

async def main():
    # 1. Initialize SakaEval for Sentiment Analysis
    evaluator = SakaEval(task="sentiment")
    
    # 2. Load a sample dataset from HuggingFace
    # Using 'tyqiangz/multilingual-sentiments' as a placeholder for Indonesian sentiment
    try:
        evaluator.load_hf_dataset("tyqiangz/multilingual-sentiments", name="indonesian", split="test")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    # 3. Initialize Model
    model = DummyModel()

    # 4. Run Asynchronous Evaluation
    print("\nStarting evaluation...")
    results = await evaluator.evaluate(
        model, 
        text="text", 
        label="label"
    )

    # 5. Show Results
    print("\nBenchmark Results:")
    print(f"Task: {results['task']}")
    print(f"Accuracy: {results['metrics']['accuracy']:.4f}")
    print(f"F1-Score: {results['metrics']['f1_score']:.4f}")
    print(f"Execution Time: {results['execution_time_seconds']}s")

    # 6. Save Report
    evaluator.save_report("sentiment_benchmark_report.json")

if __name__ == "__main__":
    asyncio.run(main())
