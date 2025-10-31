from flask import Blueprint, jsonify, request
from app.services.order_service import get_order_status
from app.services.product_service import get_product_stock
from rag.retrieval.vector_store import PineconeVectorStore
from rag.retrieval.retriever import Retriever
from rag.agents.agentic_controller import AgenticRAGController
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

api_blueprint = Blueprint('api', __name__)

# === Core Business Endpoints ===
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


# === Agentic RAG Endpoint (UPGRADED) ===
# Initialize once at startup
vector_store = PineconeVectorStore(index_name="ecommerce-agentic-rag")
embedder = OpenAIEmbeddings(model="text-embedding-3-large", api_key=os.getenv("OPENAI_API_KEY"))
retriever = Retriever(vector_store, embedder)
rag_controller = AgenticRAGController(retriever)  # Full agentic logic


@api_blueprint.route('/rag/query', methods=['POST'])
def rag_query():
    """Full Agentic RAG: retrieval + tools + generation"""
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Query is required"}), 400

    query = data["query"]

    try:
        # Use Agentic Controller (includes self-correction RAG + tool calling)
        result = rag_controller.query(query)

        return jsonify({
            "answer": result["answer"],
            "sources": result["sources"],
            "confidence": result["confidence"],
            "tool_calls": result.get("tool_calls", []),
            "hops": result.get("hops", 1),
            "retrieval_retries": result.get("retrieval_retries", 0)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500