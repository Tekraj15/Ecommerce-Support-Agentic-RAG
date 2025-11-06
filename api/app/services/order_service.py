from api.utils.mock_data import ORDERS

def get_order_status(order_id: str) -> dict:
    order = ORDERS.get(order_id, {})
    return {
        "status": order.get("status", "Not found"),
        "eta": order.get("eta"),
        "product_id": order.get("product_id")
    }