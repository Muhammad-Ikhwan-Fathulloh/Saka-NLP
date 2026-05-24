import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from saka.core.agent import Agent

# 1. Definisi Fungsi Lokal (Tools)
def get_student_grade(name: str, subject: str):
    # Simulasi data dari database
    data = {"Budi": {"Matematika": 90, "Fisika": 85}, "Siti": {"Matematika": 95, "Fisika": 88}}
    score = data.get(name, {}).get(subject, "Data tidak ditemukan")
    return f"Nilai {name} di pelajaran {subject} adalah {score}."

def calculate_average(scores: list):
    return sum(scores) / len(scores) if scores else 0

def demo_tool_calling():
    # 2. Inisialisasi Agent
    bot = Agent("Asisten Nilai Akademik", "Bantu guru mengecek nilai siswa.")
    
    # 3. Registrasi Tool secara Dinamis
    bot.add_tool(
        name="get_grade",
        desc="Ambil nilai siswa berdasarkan nama dan pelajaran.",
        params={"name": {"type": "string"}, "subject": {"type": "string"}},
        func=get_student_grade
    )
    
    bot.add_tool(
        name="calc_avg",
        desc="Hitung rata-rata dari daftar nilai.",
        params={"scores": {"type": "array", "items": {"type": "number"}}},
        func=calculate_average
    )
    
    print("=== Agent Prompt with Dynamic Tools ===")
    query = "Berapa nilai Budi di Fisika?"
    print(bot.prompt(query))
    
    # 4. Simulasi Pemanggilan Tool (Biasanya parse hasil LLM -> Call Tool)
    print("\n=== Tool Execution Simulation ===")
    # Anggap LLM memberikan: Action: get_grade | Action Input: {"name": "Budi", "subject": "Fisika"}
    observation = bot.call_tool("get_grade", {"name": "Budi", "subject": "Fisika"})
    print(f"Observation: {observation}")
    
    # Contoh lain
    print(f"Observation Avg: {bot.call_tool('calc_avg', {'scores': [80, 90, 70]})}")

if __name__ == "__main__":
    demo_tool_calling()
