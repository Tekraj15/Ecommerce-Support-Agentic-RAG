import os

# API Base URLs
FAKESTORE_API_URL = "https://fakestoreapi.com"

# Flask Configuration
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() in ("true", "1")

# Rasa Action Server
RASA_ACTION_SERVER_URL = os.getenv("RASA_ACTION_SERVER_URL", "http://localhost:5055/webhook")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
