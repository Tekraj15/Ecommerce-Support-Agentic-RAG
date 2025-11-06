# api/app/services/return_service.py
from api.utils.mock_data import POLICIES

def get_return_policy(product_id: str = None) -> dict:
    """Return return policy. If product_id given, try product-specific."""
    base = POLICIES["return"]
    if product_id and product_id in POLICIES["products"]:
        specific = POLICIES["products"][product_id].get("return", {})
        return {**base, **specific}
    return base

def get_refund_policy(product_id: str = None) -> dict:
    """Refund policy with dummy form link."""
    base = POLICIES["refund"]
    if product_id and product_id in POLICIES["products"]:
        specific = POLICIES["products"][product_id].get("refund", {})
        return {**base, **specific}
    return base
