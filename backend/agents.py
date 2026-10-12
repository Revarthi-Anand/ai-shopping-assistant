import json
from dataclasses import dataclass
from llm import ask_llm
from rag import search_products

VALID_CATEGORIES = ["Electronics", "Footwear", "Accessories", "Clothing", "Home"]


@dataclass
class Agent:
    name: str
    role: str            # the agent's instructions (its system prompt)
    n_results: int = 4   # how many products its search tool fetches

    def run(self, question: str, filters: dict | None = None) -> dict:
        filters = filters or {}

        # Tool: semantic product search with hard filters
        matches = search_products(question, n_results=self.n_results, **filters)

        if not matches:
            return {
                "agent": self.name,
                "answer": "I couldn't find any products matching that request and budget. "
                          "Try raising the budget or describing what you need differently.",
                "sources": [],
                "filters": filters,
            }

        context = "\n".join(
            f"- {m['text']} | Rs {m['price']} | rating {m['rating']}" for m in matches
        )
        prompt = f"Retrieved products:\n{context}\n\nCustomer message: {question}"
        answer = ask_llm(prompt, self.role)
        return {
            "agent": self.name,
            "answer": answer,
            "sources": [m["name"] for m in matches],
            "filters": filters,
        }


AGENTS = {
    "recommend": Agent(
        name="Recommendation Agent",
        role=(
            "You are a personal shopping advisor. Use ONLY the retrieved products. "
            "Recommend those that genuinely fit the customer's need, ignore the rest, "
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

PLANNER_PROMPT = (
    "You are the planner of a shopping assistant. Read the customer's message and reply with "
    "ONLY a JSON object, no other text, with these keys:\n"
    '"agent": one of "recommend" (wants suggestions, gift ideas, or products for a need), '
    '"compare" (wants products compared, or asks which is better), '
    '"qa" (asks a specific question about one product\'s features).\n'
    '"max_price": a number in rupees if the customer states a budget, otherwise null.\n'
    '"category": one of Electronics, Footwear, Accessories, Clothing, Home ONLY if the customer '
    "clearly names that type of product, otherwise null."
)


def plan(question: str):
    """One LLM call that picks the agent AND extracts search filters."""
    raw = ask_llm(question, PLANNER_PROMPT)
    raw = raw.replace("```json", "").replace("```", "").strip()
    try:
        data = json.loads(raw)
    except Exception:
        data = {}

    agent_key = data.get("agent") if data.get("agent") in AGENTS else "recommend"

    filters = {}
    price = data.get("max_price")
    if isinstance(price, (int, float)) and not isinstance(price, bool):
        filters["max_price"] = price
    if data.get("category") in VALID_CATEGORIES:
        filters["category"] = data["category"]

    return agent_key, filters


def handle(question: str) -> dict:
    agent_key, filters = plan(question)
    return AGENTS[agent_key].run(question, filters)