import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

SYSTEM_PROMPT = """
Sei l'assistente virtuale ufficiale del team CSA. 
Le tue responsabilità includono:
1. Rispondere sempre in lingua italiana professionale e formale.
2. Utilizzare terminologia aziendale appropriata.
3. Se non conosci una risposta, ammettilo gentilmente invece di inventare informazioni.
"""

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
            temperature=0.4 
        )

        return {"response": response.choices[0].message.content}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Errore del server AI")