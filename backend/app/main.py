from fastapi import FastAPI
from pydantic import BaseModel
from app.chatbot import answer_query

app = FastAPI(title="CSA Research Chatbot", version="0.1.0")

@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
def chat(request: ChatRequest):
    response = answer_query(request.query)
    return {"response": response}
