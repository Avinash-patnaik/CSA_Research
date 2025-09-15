from fastapi import FastAPI

# create a FastAPI instance
app = FastAPI(title="CSA Research Chatbot", version="0.1.0")

# Root endpoint - just for testing
@app.get("/")
def root():
    return {"message": "Backend is running"}