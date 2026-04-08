"""
Async Usage Example for Saka-NLP
This shows how to run non-blocking NLP operations over a set of texts using asyncio.
"""

import asyncio
import time
import saka

async def process_text(text: str, idx: int):
    print(f"[Tugas {idx}] Memulai pemrosesan...")
    
    # Menjalankan tokenisasi dan normalisasi berturut-turut tanpa membebani event loop utama
    tokens = await saka.async_tokenize(text)
    normalized = await saka.async_normalize(text)
    
    print(f"[Tugas {idx}] Selesai! Hasil Normalisasi: '{normalized}'")
    return tokens, normalized

async def main():
    texts_to_process = [
        "klo gimana kbrnya dngn gw?",
        "ajep-ajep mulu dlu pas di kmpus",
        "gw lg nugas bwt bsk brngkt pagi"
    ]
    
    start_time = time.perf_counter()
    
    # Kumpulkan semua tasks asyncio (ini akan berjalan secara konkuren/bersamaan)
    tasks = [process_text(text, i+1) for i, text in enumerate(texts_to_process)]
    
    # Tunggu semua tasks selesai
    results = await asyncio.gather(*tasks)
    
    end_time = time.perf_counter()
    print(f"\nSelesai memproses {len(texts_to_process)} kalimat dalam {end_time - start_time:.4f} detik.")

if __name__ == "__main__":
    asyncio.run(main())
