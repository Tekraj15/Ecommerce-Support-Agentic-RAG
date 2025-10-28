"""
Agentic RAG Controller: Full pipeline with reasoning loop.
"""
from rag.retrieval.retriever import Retriever
from rag.augmentation.augmenter import RAGAugmenter
from rag.generation.generator import RAGGenerator
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class AgenticRAGController:
    def __init__(self, retriever: Retriever):
        self.retriever = retriever
        self.augmenter = RAGAugmenter()
        self.generator = RAGGenerator()
        self.max_retries = 2

    def query(self, user_query: str, use_hyde: bool = True) -> Dict[str, Any]:
        query = user_query
        for attempt in range(self.max_retries + 1):
            # Step 1: Retrieve
            docs = self.retriever.retrieve(
                query, top_k=5, use_hyde=use_hyde, use_mmr=True, use_rerank=False
            )

            # Step 2: Augment
            augmented = self.augmenter.augment(query, docs)

            # Step 3: Generate
            result = self.generator.generate(augmented)

            confidence = augmented["metadata"]["confidence"]

            # Step 4: Self-Correction (if low confidence)
            if confidence < 0.6 and attempt < self.max_retries:
                logger.info(f"Low confidence ({confidence}), retrying with refined query...")
                query = f"Clarify or rephrase: {user_query} based on: {docs[0].get('text', '')[:200]}"
                continue

            return {
                "answer": result["response"],
                "sources": augmented["metadata"]["sources"],
                "confidence": confidence,
                "retrieved_docs": len(docs)
            }

        return {"answer": "I couldn't find a reliable answer for your query.", "confidence": 0.0}