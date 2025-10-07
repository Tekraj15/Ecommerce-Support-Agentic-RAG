"""
Basic tests for RAG ingestion pipeline.
"""
import unittest
from rag.ingestion.loader import DocumentLoader
from rag.ingestion.chunker import DocumentChunker

class TestDocumentLoader(unittest.TestCase):
    def test_load_json(self):
        loader = DocumentLoader(source_dir="data/documents")
        self.assertIsInstance(loader.load_json(), list)

    def test_load_pdf(self):
        loader = DocumentLoader(source_dir="data/documents")
        self.assertIsInstance(loader.load_pdf(), list)

    def test_load_csv(self):
        loader = DocumentLoader(source_dir="data/documents")
        self.assertIsInstance(loader.load_csv(), list)

class TestDocumentChunker(unittest.TestCase):
    def test_chunk_text(self):
        chunker = DocumentChunker()
        chunks = chunker.chunk_text("This is a test document.")
        self.assertIsInstance(chunks, list)

    def test_chunk_docs(self):
        chunker = DocumentChunker()
        docs = ["Doc1 text", "Doc2 text"]
        chunked = chunker.chunk_docs(docs)
        self.assertIsInstance(chunked, list)

if __name__ == "__main__":
    unittest.main()
