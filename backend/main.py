from fastapi import FastAPI

app = FastAPI(title="AI Shopping Assistant")


@app.get("/")
def home():
    return {"message": "Shopping assistant backend is running"}


@app.get("/products")
def get_products():
    return [
        {"id": 1, "name": "Wireless Earbuds", "price": 1999, "category": "Electronics"},
        {"id": 2, "name": "Running Shoes", "price": 2999, "category": "Footwear"},
        {"id": 3, "name": "Backpack", "price": 1499, "category": "Accessories"},
    ]