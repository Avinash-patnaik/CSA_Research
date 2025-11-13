1.  Clone the repository: `git clone ...`
2.  **Download the LLM Model:**
    This project requires a GGUF model. Download the following file:
    * **Model:** `Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf`
    * **From:** `https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/blob/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf`
    * **Place it in:** `backend/models/`
3.  Run the application: `docker compose up --build`