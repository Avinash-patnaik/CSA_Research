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
