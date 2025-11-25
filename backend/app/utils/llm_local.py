from llama_cpp import Llama
import os 
from ..config import settings 

class LLMLocalEngine:
    
    def __init__(self):
        
        self.model_path = settings.MODEL_PATH

        if not self.model_path or not os.path.exists(self.model_path):
            raise ValueError(f"Model path not found: {self.model_path}")

        print(f"Loading model from {self.model_path}; Please wait! this may take a few minutes...")

        self.llm = Llama( 
            model_path=self.model_path,
            n_ctx=2048,
            n_gpu_layers=0,
            n_threads=8,
            n_batch=256,
            verbose=False
        )
        print("✅ Model loaded successfully!")

    def generate_response(self, prompt: str) -> str:
        """
        Get a response from the local LLM model using the class instance.
        """
        system_prompt = "Sei un assistente disponibile, rispettoso e onesto."
        full_prompt = (
            f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
            f"{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
            f"{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        )

        print(f"Querying local model with: {prompt}")

        try:
            output = self.llm(
                full_prompt,
                max_tokens=512,
                echo=False,
                stop=["<|eot_id|", "<|end_of_text|>"]
            )
            
            response_text = output["choices"][0]["text"].strip()
            print(f"Model response: {response_text}")
            
            return response_text

        except Exception as e:
            print(f"Error during model generation: {e}")
            return "Spiacenti, si è verificato un errore durante l'elaborazione della tua richiesta."


local_llm_instance = LLMLocalEngine()

def get_local_llm_response(prompt: str) -> str:
    """Convenience function for chatbot.py to call the instance method."""
    return local_llm_instance.generate_response(prompt)