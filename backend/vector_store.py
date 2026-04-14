import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

model = SentenceTransformer("all-MiniLM-L6-v2")

index = None
property_ids = []


def build_index(properties: list):
    """
    Call this on startup and whenever a new property is added.
    properties: list of ORM Property objects
    """
    global index, property_ids

    if not properties:
        return

    property_ids = [p.id for p in properties]
    texts = [
        f"{p.title} {p.type} {p.city} size {p.size} price {int(p.price)}"
        for p in properties
    ]
    embeddings = model.encode(texts, convert_to_numpy=True)
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # inner product = cosine on normalised vecs
    index.add(embeddings)


def get_similar(property_id: int, top_k: int = 5) -> list[int]:
    """Returns list of similar property IDs (excluding itself)."""
    global index, property_ids

    if index is None or property_id not in property_ids:
        return []

    pos = property_ids.index(property_id)
    texts = []  # re-encode just the query property
    return _search(pos, top_k + 1)  # +1 because result includes itself


def _search(pos: int, top_k: int) -> list[int]:
    """Internal: search by position in index."""
    vec = np.array([index.reconstruct(pos)])
    _, indices = index.search(vec, top_k)
    results = []
    for i in indices[0]:
        if i != pos and i < len(property_ids):
            results.append(property_ids[i])
    return results
