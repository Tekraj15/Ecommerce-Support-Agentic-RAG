"""
Retriever with semantic search, reranker, and HyDE pipeline toggle.
"""
from typing import List, Dict, Any, Optional
import numpy as np

class Retriever:
    def __init__(self, vector_store, embed_fn, rerank_fn=None, hyde_fn=None):
        self.vector_store = vector_store
        self.embed_fn = embed_fn
        self.rerank_fn = rerank_fn
        self.hyde_fn = hyde_fn

    def retrieve(self, query: str, top_k: int = 5, use_hyde: bool = False) -> List[Dict[str, Any]]:
        if use_hyde and self.hyde_fn:
            hypo = self.hyde_fn(query)
            query_emb = self.embed_fn(hypo)
        else:
            query_emb = self.embed_fn(query)
        results = self.vector_store.query(query_emb, top_k=top_k)
        if self.rerank_fn:
            results = self.rerank_fn(query, results)
        return results

# Example stub for reranker (to be implemented with sentence-transformers CrossEncoder)
def simple_rerank(query: str, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Placeholder: sort by length of text
    return sorted(docs, key=lambda d: len(d.get("text", "")), reverse=True)
