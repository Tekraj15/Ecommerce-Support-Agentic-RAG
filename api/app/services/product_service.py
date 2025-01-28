from app.utils.mock_data import PRODUCTS

def get_product_stock(product_name):
    """Fetch the stock count of a product"""
    return PRODUCTS.get(product_name, 0)
