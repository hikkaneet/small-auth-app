import secrets

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

TORTOISE_ORM = {
    "connections": {
        "default": "postgres://admin:admin123@localhost:5432/taskboard"
    },
    "apps": {
        "models": {
            "models": ["app.models"],
            "default_connection": "default",
        }
    }
}
