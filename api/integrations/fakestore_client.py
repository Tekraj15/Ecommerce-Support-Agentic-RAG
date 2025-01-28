import requests

FAKESTORE_API_URL = "https://fakestoreapi.com"

def get_product_info(product_id):
    """Fetch product details from FakeStore API"""
    response = requests.get(f"{FAKESTORE_API_URL}/products/{product_id}")
    return response.json()
