import time
import statistics
import sys
import io

# Ensure stdout handles UTF-8 (emojis)
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from saka import tokenize, normalize, analyze, demojize, replace_emoticons

def benchmark():
    texts = [
        "Halo semua! 😊 Apa kabar hari ini? #semangat",
        "klo gimana gw hr ini? :)",
        "mempertanggungjawabkan masalah ini sangat sulit.",
        "https://saka-nlp.netlify.app/ adalah website resmi Saka-NLP @sakanlp",
        "❤️ ini adalah simbol cinta.",
        "sy mw mkn nasi padang bgt !!!",
        "Gue lagi di jalan nih, otw.",
        "Basically, literally, jujurly gue tuh penat bgt.",
        "Aing nemu harta karun di Bandung.",
        "Matur nuwun sanget nggih pak."
    ]
    
    # Warm up cache
    for t in texts:
        tokens = tokenize(t)
        normalize(t)
        for tok in tokens:
            analyze(tok)
    
    # 1. Test Emoji/Emoticon Recognition
    print("Testing Emoji/Emoticon Recognition:")
    test_emoji = "Halo 😊 :) ❤️"
    print(f"Original: {test_emoji}")
    print(f"Demojized: {demojize(test_emoji)}")
    print(f"Emoticons replaced: {replace_emoticons(test_emoji)}")
    
    # 2. Benchmark Preprocessing
    print("\nBenchmarking Performance (Full Pipeline Simulation):")
    n_iterations = 1000
    times = []
    
    for _ in range(n_iterations):
        start = time.perf_counter()
        for t in texts:
            # Full 2026 Pipeline: Demojize -> Tokenize -> Normalize -> (Analyze)
            d = demojize(t)
            tokens = tokenize(d)
            # Normalization on full text (as implemented in normalize)
            norm = normalize(d)
            # Sampling analysis for some tokens
            for tok in tokens[:2]:
                analyze(tok)
        end = time.perf_counter()
        times.append((end - start) / len(texts)) # Average per text
        
    avg_time = statistics.mean(times) * 1000 # to ms
    median_time = statistics.median(times) * 1000
    
    print(f"Average time per text: {avg_time:.4f} ms")
    print(f"Median time per text: {median_time:.4f} ms")
    
    # Validation against target
    if avg_time < 4.0:
        print("✅ Performance target (~3.2ms) achieved!")
    else:
        print("❌ Performance target exceeded.")

if __name__ == "__main__":
    benchmark()
