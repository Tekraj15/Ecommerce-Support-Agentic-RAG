"""
Basic tests for RAG ingestion pipeline.
"""
import unittest
from rag.ingestion.loader import DocumentLoader
from rag.ingestion.chunker import DocumentChunker
from rag.retrieval.vector_store import InMemoryVectorStore
from rag.retrieval.retriever import Retriever

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

class TestRetriever(unittest.TestCase):
    def setUp(self):
        # Create dummy chunks with embeddings
        self.chunks = [
            {"id": "doc0_chunk0", "text": "Fjallraven Backpack specs", "embedding": [1.0]*10},
            {"id": "doc1_chunk0", "text": "Laptop under $1000", "embedding": [0.5]*10},
            {"id": "doc2_chunk0", "text": "Returns and refund policy", "embedding": [0.2]*10}
        ]
        self.store = InMemoryVectorStore()
        self.store.add_documents(self.chunks)
        # Dummy embed_fn: returns the same embedding for test query
        self.embed_fn = lambda x: [1.0]*10 if "Backpack" in x else [0.5]*10
        self.retriever = Retriever(vector_store=self.store, embed_fn=self.embed_fn)

    def test_retrieve_top_k(self):
        results = self.retriever.retrieve("Fjallraven Backpack specs", top_k=2)
        self.assertEqual(len(results), 2)
        self.assertTrue(any("Backpack" in r["text"] for r in results))

    def test_retrieve_with_hyde(self):
        # Dummy hyde_fn: returns a hypothetical answer
        hyde_fn = lambda q: "Hypothetical Backpack specs"
        retriever = Retriever(vector_store=self.store, embed_fn=self.embed_fn, hyde_fn=hyde_fn)
        results = retriever.retrieve("Backpack", top_k=1, use_hyde=True)
        self.assertEqual(len(results), 1)

if __name__ == "__main__":
    unittest.main()
