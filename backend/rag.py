import chromadb

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("products")


def search_products(question: str, n_results: int = 4) -> list[dict]:
    """Find the products whose meaning is closest to the question."""
    results = collection.query(query_texts=[question], n_results=n_results)
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    return [{**meta, "text": doc} for meta, doc in zip(metadatas, documents)]