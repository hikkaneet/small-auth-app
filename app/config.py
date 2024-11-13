import secrets

# Generate a secret key for JWT encoding
SECRET_KEY = secrets.token_hex(32)  # 32 bytes of random data, equivalent to 256 bits

# Set the algorithm for JWT encoding
ALGORITHM = "HS256"  # HMAC using SHA-256

# Set the expiration time for access tokens in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes

# Tortoise ORM configuration
TORTOISE_ORM = {
    "connections": {
        "default": "postgres://admin:admin123@localhost:5432/taskboard"  # Connection string for PostgreSQL database
    },
    "apps": {
        "models": {
            "models": ["app.models"],  # Path to the models module
            "default_connection": "default",  # Default connection for the models
        }
    }
}
