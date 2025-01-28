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
