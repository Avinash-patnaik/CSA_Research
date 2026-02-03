import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  
from pydantic import BaseModel
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = """
Sei l'assistente virtuale ufficiale del team CSA. 
...
"""

class ChatRequest(BaseModel):
    query: str

client = InferenceClient(
    model=os.getenv("HF_MODEL_ID"),
    token=os.getenv("HF_TOKEN")  
)

@app.get("/")
def read_root():
    return {"status": "CSA Chatbot API is online"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Standard chat completion call
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.query}
            ],
            max_tokens=800,
            temperature=0.4 
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Errore del server AI")