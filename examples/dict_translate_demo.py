"""
Contoh penggunaan dict_translate - Terjemahan Bahasa Daerah berbasis Kamus Lokal

Menerjemahkan teks Bahasa Indonesia ke bahasa daerah (Sunda, Jawa, Bali, Minang, Batak)
secara word-by-word menggunakan kamus yang tersedia di package, tanpa memerlukan LLM.
"""
import saka

# --- 1. Terjemahan Sederhana ---
print("=== Terjemahan Sederhana ===")
text = "saya makan nasi"
print(f"Input (Indonesia): {text}\n")

for lang in ['sunda', 'jawa', 'bali', 'minang', 'batak']:
    result = saka.dict_translate(text, lang)
    print(f"  {lang.capitalize():10s} → {result}")

# --- 2. Terjemahan Kalimat Lebih Panjang ---
print("\n=== Kalimat Lebih Panjang ===")
kalimat = "air itu bagus dan bersih"
print(f"Input (Indonesia): {kalimat}\n")

for lang in ['sunda', 'jawa', 'bali']:
    result = saka.dict_translate(kalimat, lang)
    print(f"  {lang.capitalize():10s} → {result}")

# --- 3. Kata yang Tidak Ada di Kamus (Tetap Dipertahankan) ---
print("\n=== Kata Tidak Dikenal (Preserved) ===")
campuran = "laptop saya bagus"
for lang in ['sunda', 'jawa']:
    result = saka.dict_translate(campuran, lang)
    print(f"  {lang.capitalize():10s} → {result}")

# --- 4. Integrasi dengan Agent ---
print("\n=== Integrasi dengan Agent ===")
from saka import Agent
agent = Agent("Bot", "Penerjemah")

# Agent juga bisa menggunakan dict_translate langsung
text_agent = "rumah itu besar"
for lang in ['sunda', 'bali']:
    result = saka.dict_translate(text_agent, lang)
    print(f"  {lang.capitalize():10s} → {result}")
