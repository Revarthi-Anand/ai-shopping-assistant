import chromadb

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("products")


def search_products(question, n_results=4, max_price=None, category=None):
    """Semantic search, with optional hard filters on price and category."""
    conditions = []
    if max_price is not None:
        conditions.append({"price": {"$lte": max_price}})
    if category:
        conditions.append({"category": category})

    where = None
    if len(conditions) == 1:
        where = conditions[0]
    elif len(conditions) > 1:
        where = {"$and": conditions}

    results = collection.query(query_texts=[question], n_results=n_results, where=where)
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    return [{**meta, "text": doc} for meta, doc in zip(metadatas, documents)]