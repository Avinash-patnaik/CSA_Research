from llama_cpp import Llama
from app import config
import os 

MODEL_PATH = config.MODEL_PATH

if not MODEL_PATH or not os.path.exists(MODEL_PATH):
    raise ValueError(f"Model path not found: {MODEL_PATH}")

print(f"Loading model from {MODEL_PATH}; Please wait! this may take a few minutes...")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=4096,
    n_gpu_layers=0,
    n_threads=8,
    verbose=False
)

print("✅ Model loaded successfully!")

def get_local_llm_response(prompt: str) -> str:
    """
    Get a response from the local LLM model.
    """
    system_prompt = "Sei un assistente disponibile, rispettoso e onesto."
    # Construct the full prompt using the official Llama 3.1 template
    full_prompt = (
        f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
        f"{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
        f"{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    )

    print(f"Querying local model with: {prompt}")

    # --- Generate the Response ---
    try:
        output = llm(
            full_prompt,
            max_tokens=512,      # Max tokens to generate
            echo=False,          # Don't repeat the prompt in the output
            stop=["<|eot_id|", "<|end_of_text|>"] # Stop tokens
        )
        
        response_text = output["choices"][0]["text"].strip()
        print(f"Model response: {response_text}")
        
        return response_text

    except Exception as e:
        print(f"Error during model generation: {e}")
        return "Spiacenti, si è verificato un errore durante l'elaborazione della tua richiesta."
