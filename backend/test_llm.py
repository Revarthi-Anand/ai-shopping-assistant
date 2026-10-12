from llm import ask_llm

print(ask_llm(
    "What should I check before buying wireless earbuds?",
    system="You are a shopping expert. Answer in 3 short bullet points.",
))