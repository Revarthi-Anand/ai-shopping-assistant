import chromadb
from database import products_collection

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="products")

products = list(products_collection.find({}, {"_id": 0}))

collection.upsert(
    ids=[str(p["id"]) for p in products],
    documents=[f"{p['name']}. {p['category']}. {p['description']}" for p in products],
    metadatas=[
        {"name": p["name"], "price": p["price"], "category": p["category"], "rating": p["rating"]}
        for p in products
    ],
)

print(f"Indexed {collection.count()} products")