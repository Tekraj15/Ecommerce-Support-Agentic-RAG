"""
Mock data for orders, products, and policies.
Linked via product_id.
"""

from datetime import datetime, timedelta
from typing import Dict, List

# === ORDERS ===
ORDERS: Dict[str, dict] = {
    "ORD-1001": {
        "status": "Shipped",
        "eta": "2025-11-08",
        "product_id": "PROD-001",
        "user_email": "alice@example.com"
    },
    "ORD-1002": {
        "status": "Processing",
        "eta": None,
        "product_id": "PROD-002",
        "user_email": "bob@example.com"
    },
    "ORD-1003": {
        "status": "Delivered",
        "eta": "2025-11-01",
        "product_id": "PROD-003",
        "user_email": "carl@example.com"
    }
}

# === PRODUCTS ===
PRODUCTS: Dict[str, dict] = {
    "Laptop Pro": {
        "stock": 8,
        "restock_date": "2025-11-15",
        "product_id": "PROD-001"
    },
    "Galaxy S21": {
        "stock": 0,
        "restock_date": "2025-11-20",
        "product_id": "PROD-002"
    },
    "Noise-Cancelling Headphones": {
        "stock": 45,
        "restock_date": None,
        "product_id": "PROD-003"
    }
}

# === POLICIES (Linked to product_id) ===
POLICIES = {
    "return": {
        "days": 30,
        "condition": "unopened",
        "form_url": "https://forms.gle/return-form-dummy-link"
    },
    "refund": {
        "processing_time": "5-10 business days",
        "form_url": "https://forms.gle/refund-form-dummy-link"
    },
    "shipping": {
        "international": True,
        "countries": 50,
        "free_threshold": 50.0,
        "cost_domestic": 5.99,
        "cost_international": 19.99,
        "carriers": ["DHL", "FedEx", "UPS"],
        "source": "payment_and_shipping_options.pdf"
    },
    "products": {
        "PROD-001": {
            "return": {"days": 30, "condition": "sealed box"},
            "refund": {"processing_time": "7 business days"},
            "warranty": "2 years manufacturer warranty + 1 year accidental damage",
            "source": "laptop_warranty.pdf"
        },
        "PROD-002": {
            "return": {"days": 14, "condition": "with receipt"},
            "refund": {"processing_time": "5 business days"},
            "warranty": "1 year",
            "source": "phone_warranty.pdf"
        },
        "PROD-003": {
            "return": {"days": 30},
            "refund": {"processing_time": "10 business days"},
            "warranty": "1 year limited warranty",
            "source": "headphones_warranty.pdf"
        }
    },
    "payment": {
    "methods": ["Credit Card", "PayPal", "Apple Pay", "Google Pay"],
    "security": "256-bit SSL, PCI-DSS Level 1",
    "failed_payment": "We retry failed payments 3 times over 48 hours.",
    "refund_on_failure": True,
    "form_url": "https://forms.gle/payment-support-dummy",
    "source": "payment_and_shipping_options.pdf"
    }
}