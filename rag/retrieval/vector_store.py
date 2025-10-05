"""
Vector store adapter interface and Pinecone/in-memory implementations.
"""
from typing import List, Dict, Any

class VectorStore:
    def add_documents(self, docs: List[Dict[str, Any]]):
        raise NotImplementedError
    def query(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        raise NotImplementedError

class InMemoryVectorStore(VectorStore):
    def __init__(self):
        self.vectors = []  # List of dicts: {"embedding": [...], "metadata": {...}}
    def add_documents(self, docs: List[Dict[str, Any]]):
        for doc in docs:
            self.vectors.append(doc)
    def query(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        # Simple cosine similarity search
        from numpy import dot
        from numpy.linalg import norm
        def cosine(a, b):
            return dot(a, b) / (norm(a) * norm(b) + 1e-8)
        scored = [
            (cosine(query_embedding, v["embedding"]), v)
            for v in self.vectors if "embedding" in v
        ]
        scored.sort(reverse=True, key=lambda x: x[0])
        return [v for _, v in scored[:top_k]]

class PineconeVectorStore(VectorStore):
    def __init__(self, index):
        self.index = index
    def add_documents(self, docs: List[Dict[str, Any]]):
        # docs: [{"id": str, "embedding": [...], "metadata": {...}}]
        items = [
            (doc["id"], doc["embedding"], doc.get("metadata", {}))
            for doc in docs if "id" in doc and "embedding" in doc
        ]
        self.index.upsert(vectors=items)
    def query(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        results = self.index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
        return [
            {"id": match.id, "score": match.score, "metadata": match.metadata}
            for match in results.matches
        ]
