import os
import dotenv

dotenv.load_dotenv()

GIGACHAT_API_KEY = os.getenv("GIGACHAT_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///db.db")
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8888"))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
