import json
import logging
import os
from pathlib import Path

OPENMIND_DIR = Path(__file__).parent  # the path containing this file
print(OPENMIND_DIR)

BACKEND_DIR = OPENMIND_DIR.parent  # the path containing the backend/
BASE_DIR = BACKEND_DIR.parent  # the path containing the base/

print(BACKEND_DIR)
print(BASE_DIR)

DATA_DIR = Path(os.getenv("DATA_DIR", BACKEND_DIR / "data")).resolve()
print(DATA_DIR)

try:
    from dotenv import find_dotenv, load_dotenv

    load_dotenv(find_dotenv(str(BASE_DIR / ".env")))
except ImportError:
    print("dotenv not installed, skipping...")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_API_BASE = os.getenv("OLLAMA_API_BASE")

DATABASE_URL = os.environ.get("DATABASE_URL")
if "postgres://" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

DATABASE_SCHEMA = os.environ.get("DATABASE_SCHEMA", None)
DATABASE_POOL_SIZE = os.environ.get("DATABASE_POOL_SIZE", 0)

if DATABASE_POOL_SIZE == "":
    DATABASE_POOL_SIZE = 0
else:
    try:
        DATABASE_POOL_SIZE = int(DATABASE_POOL_SIZE)
    except Exception:
        DATABASE_POOL_SIZE = 0

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

VECTOR_DB = os.environ.get("VECTOR_DB", "chroma")
