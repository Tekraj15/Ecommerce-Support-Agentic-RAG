from api.utils.mock_data import POLICIES
def get_payment_methods() -> dict:
    """Return accepted payment methods and security info."""
    return {
        "methods": POLICIES.get("payment", {}).get("methods", []),
        "security": POLICIES.get("payment", {}).get("security", "PCI-DSS compliant"),
        "source": POLICIES.get("payment", {}).get("source", "payment_and_shipping_options.pdf")
    }


def get_payment_policy() -> dict:
    """General payment policy (refunds, failed payments, etc.)."""
    return {
        "failed_payment": POLICIES.get("payment", {}).get("failed_payment", "Retry within 24 hours"),
        "refund_on_failure": POLICIES.get("payment", {}).get("refund_on_failure", True),
        "form_url": POLICIES.get("payment", {}).get("form_url", "https://forms.gle/payment-issue-form"),
        "source": POLICIES.get("payment", {}).get("source", "payment_and_shipping_options.pdf")
    }

def get_shipping_info() -> dict:
    return POLICIES["shipping"]

def get_warranty_info(product_id: str) -> dict:
    """Product-specific warranty."""
    if product_id not in POLICIES.get("products", {}):
        return {"warranty": "Not available", "source": "unknown"}
    product = POLICIES["products"][product_id]
    return {
        "warranty": product.get("warranty", "Standard 1-year"),
        "source": product.get("source", "warranty_info.pdf")
    }