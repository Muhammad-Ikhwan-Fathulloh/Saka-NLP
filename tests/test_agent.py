import pytest
from saka.core.agent import Agent

def test_agent_output_language():
    """Test if output_language is correctly added to the prompt output in Agent.translate_to"""
    agent = Agent("Bot", "Interpreter")
    prompt_res = agent.translate_to("halo semuanya, apa kabar?", "sunda")
    
    assert "OUTPUT LANGUAGE:" in prompt_res
    assert "Hasilkan atau terjemahkan output ke dalam bahasa daerah: sunda" in prompt_res
    assert "Terjemahkan teks berikut dengan natural ke dalam bahasa: sunda" in prompt_res
    assert "halo semuanya, apa kabar?" in prompt_res

def test_agent_prompt_override():
    """Test if Agent.prompt can accept the output_language variable"""
    agent = Agent("Customer Service", "Menjawab pertanyaan dengan sopan.")
    query = "apakah ada stok untuk ini?"
    prompt_res = agent.prompt(query, output_language="jawa")
    
    assert "OUTPUT LANGUAGE:" in prompt_res
    assert "Hasilkan atau terjemahkan output ke dalam bahasa daerah: jawa" in prompt_res
    assert "apakah ada persediaan untuk ini?" in prompt_res
