from api.utils.mock_data import ORDERS

def get_order_status(order_id):
    """Fetch the order status from mock data"""
    return ORDERS.get(order_id, "Not Found")
