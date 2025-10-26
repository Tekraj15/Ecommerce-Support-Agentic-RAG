"""
Retriever with semantic search, reranker, MMR, and HyDE support.
"""
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from rag.retrieval.vector_store import VectorStore
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

class Retriever:
    def __init__(self, vector_store: VectorStore, embed_fn, rerank_fn=None, hyde_llm=None):
        self.vector_store = vector_store
        self.embed_fn = embed_fn
        self.rerank_fn = rerank_fn
        self.hyde_llm = hyde_llm if hyde_llm else ChatOpenAI(model="gpt-4o-mini")  # For HyDE

    def hyde_query(self, query: str) -> str:
        """Generate hypothetical document for HyDE Retrieval."""
        hypo_prompt = f"Write a detailed hypothetical answer to: {query}"
        return self.hyde_llm.invoke(hypo_prompt).content

    def retrieve(self, query: str, top_k: int = 5, use_hyde: bool = False, use_mmr: bool = False, use_rerank: bool = False) -> List[Dict[str, Any]]:
        query_text = self.hyde_query(query) if use_hyde else query
        query_emb = self.embed_fn.embed_query(query_text)

        # Base retrieval
        results = self.vector_store.query(query_emb, top_k=20 if (use_mmr or use_rerank) else top_k)

        # Maximal Margin Relevance(MMR) for diversity(aiding the LLM in generalization)
        if use_mmr:
            docs = [r["metadata"]["text"] for r in results]  # Extract texts for MMR
            mmr_retriever = BM25Retriever.from_texts(docs)
            mmr_retriever.search_type = "mmr"
            results = mmr_retriever.get_relevant_documents(query)[:top_k]

        # Rerank for precision
        if use_rerank:
            compressor = CohereRerank(top_n=top_k)
            reranker = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=results)
            results = reranker.get_relevant_documents(query)

        return results