import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Match the frontend body: JSON.stringify({ query: query })
class ChatRequest(BaseModel):
    query: str

client = InferenceClient(
    model=os.getenv("HF_MODEL_ID"),
    api_key=os.getenv("HF_TOKEN")
)

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Mistral v0.3 Italian logic
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.query}
            ],
            max_tokens=800,
            temperature=0.4 # Lower temperature for more professional, stable Italian
        )
        
        # Match the frontend interface: ChatResponse { response: string }
        return {"response": response.choices[0].message.content}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Errore del server AI")