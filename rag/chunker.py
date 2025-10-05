"""
Chunker for semantic/sliding window chunking of documents.
"""
from typing import List, Dict, Any
import math

class DocumentChunker:
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str) -> List[str]:
        """Chunk text using sliding window."""
        chunks = []
        start = 0
        text_length = len(text)
        while start < text_length:
            end = min(start + self.chunk_size, text_length)
            chunk = text[start:end]
            chunks.append(chunk)
            if end == text_length:
                break
            start += self.chunk_size - self.overlap
        return chunks

    def chunk_docs(self, docs: List[str]) -> List[Dict[str, Any]]:
        """Chunk multiple docs and add metadata."""
        chunked = []
        for idx, doc in enumerate(docs):
            chunks = self.chunk_text(doc)
            for i, chunk in enumerate(chunks):
                chunked.append({
                    "doc_id": idx,
                    "chunk_id": i,
                    "text": chunk,
                    "total_chunks": len(chunks)
                })
        return chunked
