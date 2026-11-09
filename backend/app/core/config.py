import os
from pathlib import Path

from dotenv import load_dotenv

DEPTH = 3
PROJECT_ROOT = Path(__file__).resolve().parents[DEPTH]
ENV_FILE = PROJECT_ROOT / "infrastructure" / "docker" / ".env"

load_dotenv(ENV_FILE)


CONTROL_DB_CONFIG = {
    "host": os.getenv("CONTROL_DB_HOST", "localhost"),
    "port": int(os.getenv("CONTROL_DB_PORT", "5433")),
    "database": os.getenv("CONTROL_DB_NAME"),
    "user": os.getenv("CONTROL_DB_USER"),
    "password": os.getenv("CONTROL_DB_PASSWORD"),
}

MANAGED_DB_CONFIG = {
    "host": os.getenv("MANAGED_DB_HOST", "localhost"),
    "port": int(os.getenv("MANAGED_DB_PORT", "5434")),
    "database": "postgres",
    "user": os.getenv("MANAGED_DB_USER"),
    "password": os.getenv("MANAGED_DB_PASSWORD"),
}


# JWT authentication
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30