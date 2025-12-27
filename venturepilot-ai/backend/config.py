import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration (Mistral AI)
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "mistral-small-latest")

# Vector Store Configuration
CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")

# Data Paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
POLICIES_DIR = os.path.join(DATA_DIR, "policies")
INVESTORS_DIR = os.path.join(DATA_DIR, "investors")
NEWS_DIR = os.path.join(DATA_DIR, "news")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
