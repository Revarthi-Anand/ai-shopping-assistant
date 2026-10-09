from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import products_collection

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