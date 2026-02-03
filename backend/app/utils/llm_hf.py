import os 
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

class LLMHFEngine:
    def __init__(self):
        self.hf_token = os.getenv("HF_TOKEN")
        self.model_id = os.getenv("HF_MODEL_ID")
        
        if not self.hf_token:
            raise ValueError("HF_TOKEN is not set in environment variables.")
        
        self.client = InferenceClient(
            model=self.model_id,
            token=self.hf_token      
            )
        print(f"✅ Hugging Face Inference Client initialized for model: {self.model_id}")
        
    def generate_response(self, prompt: str) -> str:
        
        system_prompt = "Sei un assistente disponibile, rispettoso e onesto. Rispondi sempre in italiano."
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        print(f"🤖 Sending prompt to Hugging Face model: {self.model_id}")
        
        try:
            response = self.client.chat_completion(
                messages=messages,
                max_new_tokens=512,
                temperature=0.7
            )
            
            response_text = response.choices[0].message.content.strip()
            print(f"Model response: {response_text}")
            return response_text

        except Exception as e:
            print(f"❌ Error during Hugging Face inference: {e}")
            return "Si è verificato un errore durante la generazione della risposta."
        
llm_hf_engine = LLMHFEngine()

def get_hf_response(prompt: str) -> str:
    return llm_hf_engine.generate_response(prompt)