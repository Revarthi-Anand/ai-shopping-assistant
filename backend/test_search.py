import chromadb

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("products")

question = "something to carry my laptop while traveling"
results = collection.query(query_texts=[question], n_results=3)

for meta in results["metadatas"][0]:
    print(meta["name"], "- Rs", meta["price"])