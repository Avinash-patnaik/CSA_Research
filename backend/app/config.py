# app/config.py
import os 
from dotenv import load_dotenv

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_PATH = os.path.join(BACKEND_DIR, ".env")
load_dotenv(ENV_PATH)

# LLM settings 
MODEL_PATH = os.getenv("MODEL_PATH")

# --- Debug: Print to confirm it's working ---
if MODEL_PATH and os.path.exists(MODEL_PATH):
    print(f"✅ Config loaded: Model path found at {MODEL_PATH}")
elif MODEL_PATH:
    print(f"⚠️ WARNING: Config loaded, but path {MODEL_PATH} does not exist.")
else:
    print(f"❌ ERROR: MODEL_PATH not found in {ENV_PATH}. Please check your .env file.")
