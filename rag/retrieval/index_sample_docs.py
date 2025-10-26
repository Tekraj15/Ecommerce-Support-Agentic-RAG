"""
Script to index sample docs into vector store (in-memory or Pinecone).
"""
from rag.ingestion.loader import DocumentLoader
from rag.ingestion.chunker import DocumentChunker
from rag.retrieval.vector_store import InMemoryVectorStore, PineconeVectorStore
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    source_dir = "data/documents/raw"  #e-commerce data path for RAG ingesiton
    loader = DocumentLoader(source_dir=source_dir)
    docs = loader.load_json() + loader.load_pdf() + loader.load_csv()
    chunker = DocumentChunker(chunk_size=512, chunk_overlap=50)
    chunks = chunker.chunk_docs(docs)
    
    # Assign IDs and metadata
    for chunk in chunks:
        chunk["id"] = f"doc{chunk['doc_id']}_chunk{chunk['chunk_id']}"
        chunk["metadata"] = {"source": chunk.get("source", "ecommerce_doc")}

    # Index to Pinecone (or InMemory as fallback)
    store = PineconeVectorStore(index_name="ecommerce-rag")  # Replaced the InMemoryVectorStore() as it's inefficient for large data.
    store.add_documents(chunks)
    print(f"Indexed {len(chunks)} chunks.")

    # Example query
    from langchain_openai import OpenAIEmbeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    query_embedding = embeddings.embed_query("backpack specs")
    results = store.query(query_embedding, top_k=3)
    print("Top results:", results)