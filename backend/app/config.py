# app/config.py
import os 
from dotenv import load_dotenv

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_PATH = os.path.join(BACKEND_DIR, ".env")
load_dotenv(ENV_PATH)


class settings:
    APP_NAME: str = "CSA-Chatbot"
    MODEL_PATH: str = os.getenv("MODEL_PATH")
    
settings = settings()
    
# --- Debug/Verification ---
if settings.MODEL_PATH and os.path.exists(settings.MODEL_PATH):
    print(f"✅ Config loaded: Model path found at {settings.MODEL_PATH}")
elif settings.MODEL_PATH:
    print(f"⚠️ WARNING: Config loaded, but path {settings.MODEL_PATH} does not exist.")
else:
    print(f"❌ ERROR: MODEL_PATH not found. Please check your .env file.")
