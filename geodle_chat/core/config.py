import os

from dotenv import load_dotenv

# Load the environment variables from a .env file
load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

settings = Settings()

# Project directories
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
SESSION_LOGS_DIR = os.path.join(LOGS_DIR, "sessions")
os.makedirs(SESSION_LOGS_DIR, exist_ok=True)
