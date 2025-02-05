import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-jwt-key")
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    
    # PostgreSQL Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        f"postgresql://{os.getenv('DB_USER', 'postgres')}:"
        f"{os.getenv('DB_PASSWORD', ' ')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '5432')}/"
        f"{os.getenv('DB_NAME', ' ')}"
    )
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 20,
        "max_overflow": 30,
        "pool_pre_ping": True
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis Configuration
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # External APIs
    FAKESTORE_API_BASE = os.getenv(
        "FAKESTORE_API_BASE",
        "https://fakestoreapi.com"
    )
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_API_BASE = os.getenv(
        "DEEPSEEK_API_BASE", 
        "https://api.deepseek.com/v1"
    )
    
    # Rasa Configuration
    RASA_ACTIONS_URL = os.getenv(
        "RASA_ACTIONS_URL", 
        "http://localhost:5055/webhook"
    )
    
    # Email Configuration
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    
    # JWT Security
    JWT_ACCESS_TOKEN_EXPIRES = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 86400)  # 24h
    )
    PROPAGATE_EXCEPTIONS = True

class DevelopmentConfig(Config):
    DEBUG = True
    # Local PostgreSQL instance
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/ecommerce_dev"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/ecommerce_test"

class ProductionConfig(Config):
    DEBUG = False
    # Cloud PostgreSQL example
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        "postgresql://user:pass@cloud-postgres.example.com:5432/prod_db"
    )

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
