import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import saka
from saka import MultiAgentManager, Agent

def full_integration_demo():
    print(f"=== Saka-NLP v{saka.__version__} Full Integration Demo ===\n")
    
    # 1. Input kotor (slang)
    raw_query = "Gw mw tnya gmn cranya bljr kalkulus yg sru?"
    print(f"Raw Query: {raw_query}")
    
    # 2. Normalization
    clean_query = saka.normalize(raw_query)
    print(f"Normalized: {clean_query}")
    
    # 3. Morphology Analysis (Contoh kata tertentu)
    analysis = saka.analyze("belajarnya")
    print(f"Analysis 'belajarnya': {analysis}")
    
    # 4. Multi-Agent Setup
    mgr = MultiAgentManager()
    
    # Agent 1: Math Expert
    math_bot = mgr.add_agent("math_bot", "Guru Matematika", "Bantu belajar kalkulus.")
    math_bot.add_tool(
        name="solve_integral",
        desc="Selesaikan persoalan integral.",
        params={"equation": {"type": "string"}},
        func=lambda equation: f"Hasil integral {equation} adalah [X] + C"
    )
    
    # 5. Build Structured Prompt with Token Meta
    # Kita gunakan Router Prompt dari Manager
    router_data = mgr.route_prompt(clean_query)
    # router_prompt adalah string jika return_meta=False (default)
    # Kita manual cek token count untuk evaluasi
    
    print("\n=== Initial Routing Prompt ===")
    print(router_data)
    print(f"Token Count: {saka.get_token_count(router_data)}")
    
    # 6. Specialist Prompt with Full Meta
    specialist_data = math_bot.prompt(clean_query)
    # Manual check token count
    token_eval = saka.get_token_count(specialist_data)
    
    print("\n=== Specialist Prompt (Math Bot) ===")
    print(specialist_data)
    print(f"Token Evaluation: {token_eval} tokens")
    
    # 7. Tool Execution Simulation
    print("\n=== Tool Execution ===")
    obs = math_bot.call_tool("solve_integral", {"equation": "x^2"})
    print(f"Observation: {obs}")

if __name__ == "__main__":
    full_integration_demo()
