from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import products_collection
from agents import handle

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
    try:
        return handle(req.question)
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="The AI service is busy right now. Please try again in a moment.",
        )