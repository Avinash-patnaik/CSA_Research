from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from .config import settings
from .chatbot import answer_query

# ----------APPLICATION COMPONENTS-----------
app = FastAPI(
    title=settings.APP_NAME if hasattr(settings, 'APP_NAME') else "CSA-Chatbot",
    description="A chatbot for the CSA project",
    version="0.0.1",
)

# ----------CORS CONFIGURATION-----------
origins = [
    # Frontend Development Ports (8080 is current working port)
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    
    # Other local/network IPs 
    "http://10.199.1.77:8080",
    "http://172.23.0.1:8080",
    
    # Original FastAPI/Vite defaults
    "http://localhost:5173",         
    "http://127.0.0.1:5173",         
    "http://localhost:8000",
    
    # Docker internal service name for container communication
    "http://backend:8000", 
    
    # Environment variable for production (if set)
    os.environ.get("FRONTEND_PROD_URL", "")
]
origins = [origin for origin in origins if origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ------------ENDPOINTS-------------
@app.get("/")
def root():
    return {"message": f"{app.title} is running"}

class ChatRequest(BaseModel):
    query: str 

@app.post("/chat")
def chat(request: ChatRequest):
    response = answer_query(request.query)
    return {"response": response}
