"""
Script to index sample docs into vector store (in-memory or Pinecone).
"""
from rag.ingestion.loader import DocumentLoader
from rag.ingestion.chunker import DocumentChunker
from rag.retrieval.vector_store import InMemoryVectorStore

# Example usage
if __name__ == "__main__":
    loader = DocumentLoader(source_dir="data/documents")
    docs = loader.load_json() + loader.load_pdf() + loader.load_csv()
    chunker = DocumentChunker(chunk_size=512, overlap=50)
    chunks = chunker.chunk_docs(docs if isinstance(docs, list) else [docs])
    # Dummy embedding: use length of text as embedding
    for chunk in chunks:
        chunk["embedding"] = [len(chunk["text"])] * 10  # Replace with real embedding
        chunk["id"] = f"doc{chunk['doc_id']}_chunk{chunk['chunk_id']}"
    store = InMemoryVectorStore()
    store.add_documents(chunks)
    print(f"Indexed {len(chunks)} chunks.")
    # Example query
    query = "backpack specs"
    query_embedding = [10] * 10  # Replace with real embedding
    results = store.query(query_embedding, top_k=3)
    print("Top results:", results)
