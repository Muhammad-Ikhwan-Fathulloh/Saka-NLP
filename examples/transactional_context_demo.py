from saka import normalize, extract_transaction_entities

def demo():
    texts = [
        "bisa ga ya nego jadi 10k aja",
        "boleh banget ka kalau mau 10 pcs kita ada stoknya, harga satuannya 45 ribu",
        "ready stok 50rb unit harga 1jt",
        "nett ya kak 100k gak bisa kurang"
    ]
    
    print("Saka-NLP Transactional Context Demo")
    print("=" * 40)
    
    for text in texts:
        print(f"\nOriginal: {text}")
        normalized = normalize(text)
        print(f"Normalized: {normalized}")
        
        entities = extract_transaction_entities(text)
        print("Detected Entities:")
        for ent in entities:
            print(f"  - Value: {ent['value']}, Type: {ent['type']}")

if __name__ == "__main__":
    demo()
