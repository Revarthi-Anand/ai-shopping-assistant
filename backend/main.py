from typing import Optional
from fastapi import FastAPI
from database import products_collection

app = FastAPI(title="AI Shopping Assistant")


@app.get("/")
def home():
    return {"message": "Shopping assistant backend is running"}


@app.get("/products")
def get_products(category: Optional[str] = None, max_price: Optional[int] = None):
    query = {}
    if category:
        query["category"] = category
    if max_price:
        query["price"] = {"$lte": max_price}   # $lte means "less than or equal"

    products = list(products_collection.find(query, {"_id": 0}))
    return products