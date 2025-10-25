"""
Chunker for semantic/sliding window chunking of documents using LangChain.
"""
from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentChunker:
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""],  # Semantic separators: paragraphs, lines, sentences, words
            keep_separator=True
        )

    def chunk_text(self, text: str) -> List[str]:
        """Chunk text semantically with overlap."""
        return self.splitter.split_text(text)

    def chunk_docs(self, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Chunk multiple docs and add metadata."""
        chunked = []
        for idx, doc in enumerate(docs):
            chunks = self.chunk_text(doc["text"])
            for i, chunk in enumerate(chunks):
                chunked.append({
                    "doc_id": doc.get("doc_id", idx),
                    "chunk_id": i,
                    "text": chunk,
                    "total_chunks": len(chunks),
                    "source": doc.get("source", "unknown"),
                    "metadata": doc.get("metadata", {})
                })
        return chunked