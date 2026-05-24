import sys, os, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from saka.core.prompt import build_prompt, PromptTemplate, parse_llm_output
from saka.core.agent import get_react_prompt

def demo_edu_structured():
    print("=== Demo Education Prompt ===")
    prompt = build_prompt(
        role="Asisten Akademik Virtual",
        task="Menganalisis kebutuhan belajar siswa dan memberikan rencana studi.",
        constraint="1. Fokus pada materi kurikulum nasional.\n2. Jika subjek tidak jelas, minta klarifikasi.",
        output_contract={"subjek": "...", "rencana": ["...", "..."], "durasi": "2 jam"},
        fallback_rule="Jika siswa cuma bilang 'halo' tanpa subjek, minta dia pilih pelajaran.",
        input_data="Gw bingung nih mau belajar fisika bagian mekanika, gimana ya?",
    )
    print(prompt)

def demo_edu_template():
    print("\n=== Demo Education Template ===")
    t = PromptTemplate("Pelajaran: {{mapel}} | Topik: {{topik}} | Level: {{level}}")
    print(t.render(mapel="Matematika", topik="Aljabar", level="SMA"))

def demo_edu_agent():
    print("\n=== Demo Education Agent ===")
    tools = [{
        "name": "get_exam_schedule",
        "description": "Cek jadwal ujian",
        "parameters": {"type": "object", "properties": {"kelas": {"type": "string"}}}
    }]
    print(get_react_prompt("Kapan jadwal ujian kelas 12?", tools))

if __name__ == "__main__":
    demo_edu_structured()
    demo_edu_template()
    demo_edu_agent()
    print("\nParsed:", parse_llm_output('```json\n{"ok": true}\n```'))
