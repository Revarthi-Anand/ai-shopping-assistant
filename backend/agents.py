from dataclasses import dataclass
from llm import ask_llm
from rag import search_products


@dataclass
class Agent:
    name: str
    role: str            # the agent's instructions (its system prompt)
    n_results: int = 4   # how many products its search tool fetches

    def run(self, question: str) -> dict:
        # Tool: semantic product search
        matches = search_products(question, n_results=self.n_results)
        context = "\n".join(
            f"- {m['text']} | Rs {m['price']} | rating {m['rating']}" for m in matches
        )
        prompt = f"Retrieved products:\n{context}\n\nCustomer message: {question}"
        answer = ask_llm(prompt, self.role)
        return {
            "agent": self.name,
            "answer": answer,
            "sources": [m["name"] for m in matches],
        }


AGENTS = {
    "recommend": Agent(
        name="Recommendation Agent",
        role=(
            "You are a personal shopping advisor. Use ONLY the retrieved products. "
            "Recommend those that genuinely fit the customer's need and budget, ignore the rest, "
            "and give the price in rupees. Name one top pick. If nothing fits, say so honestly."
        ),
        n_results=4,
    ),
    "compare": Agent(
        name="Comparison Agent",
        role=(
            "You are a product comparison expert. Use ONLY the retrieved products. "
            "Compare the relevant ones side by side on price, rating and key features, "
            "then say which is best value and for whom. Be concise."
        ),
        n_results=4,
    ),
    "qa": Agent(
        name="Product Q&A Agent",
        role=(
            "You answer specific questions about product features. Use ONLY the retrieved product "
            "details. If the answer is not in them, say you don't have that information. "
            "Never guess specifications."
        ),
        n_results=2,
    ),
}

ROUTER_PROMPT = (
    "You are the router of a shopping assistant. Read the customer's message and choose ONE agent:\n"
    "- recommend: wants suggestions, gift ideas, or products for a need or budget\n"
    "- compare: wants to compare products, or asks which is better\n"
    "- qa: asks a specific question about a product's features\n"
    "Reply with ONLY one word: recommend, compare, or qa."
)


def route(question: str) -> str:
    choice = ask_llm(question, ROUTER_PROMPT).strip().lower()
    for key in AGENTS:
        if key in choice:
            return key
    return "recommend"   # safe default


def handle(question: str) -> dict:
    agent_key = route(question)
    return AGENTS[agent_key].run(question)