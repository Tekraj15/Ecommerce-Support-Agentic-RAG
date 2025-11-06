from api.utils.mock_data import PRODUCTS

def get_product_stock(product_id: str) -> dict:
    product = PRODUCTS.get(product_id, {})
    return {
        "stock": product.get("stock", "Not found"),
        "restock_date": product.get("restock_date", "N/A"),
    }