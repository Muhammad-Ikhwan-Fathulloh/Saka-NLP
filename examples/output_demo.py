from saka import OutputFormatter, Agent

# Sample data mimicking LLM output
llm_data = [
    {"Word": "mangga", "Lang": "Indonesian/Javanese", "Pos": "Noun"},
    {"Word": "daharan", "Lang": "Javanese (Krama)", "Pos": "Verb"},
    {"Word": "abdi", "Lang": "Sundanese", "Pos": "Pronoun"}
]

print("--- Markdown Table ---")
print(OutputFormatter.format(llm_data, "markdown"))

print("\n--- HTML Table (Local conversion) ---")
print(OutputFormatter.format(llm_data, "html"))

print("\n--- CSV Output ---")
print(OutputFormatter.format(llm_data, "csv"))

print("\n--- Plain Text Table ---")
print(OutputFormatter.format(llm_data, "table"))

# Demo with Agent
agent = Agent(role="Linguistic Assistant", task="Analyze words")
# You can now format any data using the agent directly
result = agent.format_output(llm_data, "markdown")
print("\n--- Formatted via Agent ---")
print(result)
