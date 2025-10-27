from flask import Blueprint, jsonify, request
from app.services.order_service import get_order_status
from app.services.product_service import get_product_stock
from rag.retrieval.vector_store import PineconeVectorStore
from rag.retrieval.retriever import Retriever
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()


api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/orders/<order_id>', methods=['GET'])
def order_status(order_id):
    """Get order status by order ID"""
    status = get_order_status(order_id)
    return jsonify({"order_id": order_id, "status": status})

@api_blueprint.route('/products/<product_name>/stock', methods=['GET'])
def product_stock(product_name):
    """Get product stock availability"""
    stock = get_product_stock(product_name)
    return jsonify({"product_name": product_name, "stock": stock})

# --- FastAPI RAG endpoint ---
@api_blueprint.route('/rag/query', methods=['POST'])
def rag_query():
    """Get RAG results for a query"""
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Query is required"}), 400

    query = data["query"]
    top_k = data.get("top_k", 5)

    # Initialize RAG components
    vector_store = PineconeVectorStore(index_name="ecommerce-rag")
    embedder = OpenAIEmbeddings(model="text-embedding-3-large", api_key=os.getenv("OPENAI_API_KEY"))
    rerank_fn = None 
    retriever = Retriever(vector_store, embedder, rerank_fn=rerank_fn)

    try:
        results = retriever.retrieve(query, top_k)
        formatted_results = [{"text": r["text"], "metadata": r["metadata"]} for r in results]
        return jsonify({"results": formatted_results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500