from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import products_collection
from llm import ask_llm
from rag import search_products

app = FastAPI(title="AI Shopping Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Shopping assistant backend is running"}


@app.get("/products")
def get_products(category: Optional[str] = None, max_price: Optional[int] = None):
    query = {}
    if category:
        query["category"] = category
    if max_price:
        query["price"] = {"$lte": max_price}

    products = list(products_collection.find(query, {"_id": 0}))
    return products


class AskRequest(BaseModel):
    question: str


@app.post("/ask")
def ask(req: AskRequest):
    # 1. RETRIEVE: find the most relevant products by meaning
    matches = search_products(req.question, n_results=4)

    # 2. AUGMENT: put only those products into the prompt
    context = "\n".join(
        f"- {m['text']} | Rs {m['price']} | rating {m['rating']}" for m in matches
    )
    system = (
        "You are a shopping assistant. Use ONLY the retrieved products below. "
        "Recommend the ones that genuinely fit the customer's need and budget, "
        "and ignore any that don't. If none fit, say so honestly. "
        "Always mention the price in rupees."
    )
    prompt = f"Retrieved products:\n{context}\n\nCustomer question: {req.question}"

    # 3. GENERATE: the LLM writes the answer
    try:
        answer = ask_llm(prompt, system)
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="The AI service is busy right now. Please try again in a moment.",
        )
    return {"answer": answer, "sources": [m["name"] for m in matches]}