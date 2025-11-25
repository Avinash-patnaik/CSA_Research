from llama_cpp import Llama
import os 
from ..config import settings 

class LLMLocalEngine:
    
    def __init__(self):
        
        # 1. 🔑 FIX: Access the model path from the 'settings' instance
        self.model_path = settings.MODEL_PATH

        if not self.model_path or not os.path.exists(self.model_path):
            raise ValueError(f"Model path not found: {self.model_path}")

        print(f"Loading model from {self.model_path}; Please wait! this may take a few minutes...")

        # 2. 🔑 FIX: Store the initialized object as an instance attribute (self.llm)
        self.llm = Llama( 
            model_path=self.model_path,
            n_ctx=2048,
            n_gpu_layers=0,
            n_threads=4,
            n_batch=256,
            verbose=False
        )
        print("✅ Model loaded successfully!")

    # 3. 🔑 FIX: Move the response logic into a method (self)
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
            # 🔑 FIX: Access the model using self.llm
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


# --- Singleton Access ---
# Create one instance of the engine when the module is imported
local_llm_instance = LLMLocalEngine()

# This is the function chatbot.py will call (for convenience)
def get_local_llm_response(prompt: str) -> str:
    """Convenience function for chatbot.py to call the instance method."""
    return local_llm_instance.generate_response(prompt)