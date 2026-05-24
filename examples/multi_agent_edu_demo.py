import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from saka.core.agent import MultiAgentManager

def demo_multi_agent():
    mgr = MultiAgentManager()
    
    # 1. Tambah Agent Spesialis
    mgr.add_agent("math_expert", "Guru Matematika SMA", "Bantu jawab soal aljabar dan kalkulus.")
    mgr.add_agent("science_expert", "Guru Fisika & Kimia", "Bantu jawab soal mekanika, optik, dan reaksi kimia.")
    
    # 2. Case: Siswa bertanya tentang Fisika
    query = "Gimana cara ngitung gaya gravitasi antara dua benda?"
    
    # 3. Route Query (Biasanya ini diumpan ke LLM dulu)
    router_prompt = mgr.route_prompt(query)
    print("=== Router Prompt (Token Efficient) ===")
    print(router_prompt)
    
    # Simulasi hasil Router (mocking output LLM)
    selected_agent_name = "science_expert"
    
    # 4. Generate Specialist Prompt
    specialist_agent = mgr.agents[selected_agent_name]
    specialist_prompt = specialist_agent.prompt(query)
    
    print("\n=== Specialist Prompt ===")
    print(specialist_prompt)

if __name__ == "__main__":
    demo_multi_agent()
