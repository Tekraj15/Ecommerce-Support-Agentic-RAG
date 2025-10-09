from flask import Blueprint, jsonify, request
from app.services.order_service import get_order_status
from app.services.product_service import get_product_stock

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
try:
    from fastapi import APIRouter
    from pydantic import BaseModel
    from rag.retrieval.vector_store import InMemoryVectorStore
    from rag.retrieval.retriever import Retriever

    router = APIRouter()

    class QueryRequest(BaseModel):
        query: str
        top_k: int = 3
        use_hyde: bool = False

    # Dummy store and retriever for demo
    store = InMemoryVectorStore()
    embed_fn = lambda x: [1.0]*10
    retriever = Retriever(vector_store=store, embed_fn=embed_fn)

    @router.post("/rag/query")
    async def rag_query(request: QueryRequest):
        results = retriever.retrieve(request.query, top_k=request.top_k, use_hyde=request.use_hyde)
        return {"results": results}
except ImportError:
    pass
