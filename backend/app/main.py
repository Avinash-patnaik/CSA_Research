import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from .chatbot import answer_query 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("csa_backend")

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info(f"🚀 CSA Italian Chatbot starting with RAG enabled")
    yield
    logger.info("🛑 Backend shutting down...")

app = FastAPI(
    title="CSA Assistant API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1)

class ChatResponse(BaseModel):
    response: str

@app.get("/health")
async def health_check():
    return {"status": "online", "rag_active": True}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:

        content = answer_query(request.query)
        
        logger.info(f"✅ RAG Response generated for Italian query")
        return {"response": content}

    except Exception as e:
        logger.error(f"❌ Error in RAG Pipeline: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Errore interno del server: {str(e)}"
        )