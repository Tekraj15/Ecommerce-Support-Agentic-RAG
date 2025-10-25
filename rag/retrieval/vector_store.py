"""
Vector store adapter interface and Pinecone/in-memory implementations with OpenAI embeddings.
"""
from typing import List, Dict, Any
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

class VectorStore:
    def add_documents(self, docs: List[Dict[str, Any]]):
        raise NotImplementedError
    def query(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        raise NotImplementedError

class InMemoryVectorStore(VectorStore):
    def __init__(self):
        self.vectors = []  # List of dicts: {"id": str, "embedding": list, "metadata": dict, "text": str}

    def add_documents(self, docs: List[Dict[str, Any]]):
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_API_KEY)
        for doc in docs:
            embedding = embeddings.embed_query(doc["text"])
            self.vectors.append({
                "id": doc["id"],
                "embedding": embedding,
                "metadata": doc["metadata"],
                "text": doc["text"]
            })

    def query(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        def cosine(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)
        scored = [(cosine(query_embedding, v["embedding"]), v) for v in self.vectors]
        scored.sort(reverse=True, key=lambda x: x[0])
        return [v for _, v in scored[:top_k]]

class PineconeVectorStore(VectorStore):
    def __init__(self, index_name: str):
        pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index = pc.Index(index_name)

    def add_documents(self, docs: List[Dict[str, Any]]):
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_API_KEY)
        vectors = [
            {
                "id": doc["id"],
                "values": embeddings.embed_query(doc["text"]),
                "metadata": {"text": doc["text"], **doc["metadata"]}
            }
            for doc in docs
        ]
        self.index.upsert(vectors=vectors)

    def query(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        results = self.index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
        return [
            {"id": match["id"], "score": match["score"], "metadata": match["metadata"]}
            for match in results["matches"]
        ]