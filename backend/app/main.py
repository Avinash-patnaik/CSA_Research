import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from huggingface_hub import InferenceClient
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("csa_backend")

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    token = os.getenv("HF_TOKEN")
    model_id = os.getenv("HF_MODEL_ID")
    
    if not token or not model_id:
        logger.error("❌ Environment variables HF_TOKEN or HF_MODEL_ID are missing!")
    
    app.state.hf_client = InferenceClient(model=model_id, token=token)
    logger.info(f"🚀 CSA Chatbot Backend started with model: {model_id}")
    
    yield
    logger.info("🛑 Backend shutting down...")

app = FastAPI(
    title="CSA Assistant API",
    description="Official API for the CSA Team Virtual Assistant",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"], 
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, description="The user's message to the AI")

class ChatResponse(BaseModel):
    response: str

SYSTEM_PROMPT = """
Sei l'assistente virtuale ufficiale del team CSA. 
Responsabilità:
1. Rispondi in italiano professionale.
2. Sii conciso e accurato.
"""

def get_hf_client():
    return app.state.hf_client

@app.get("/health")
async def health_check():
    return {"status": "online", "model": os.getenv("HF_MODEL_ID")}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, client: InferenceClient = Depends(get_hf_client)):
    try:
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.query}
            ],
            max_tokens=800,
            temperature=0.4 
        )
        
        content = response.choices[0].message.content
        logger.info(f"✅ Successful inference for query: {request.query[:30]}...")
        return {"response": content}

    except Exception as e:
        logger.error(f"❌ AI Inference Error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Errore del server AI: {str(e)}"
        )