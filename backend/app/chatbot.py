from .utils.llm_hf import get_hf_response
from .utils.rag_engine import rag_engine

def answer_query(user_query: str) -> str:

    retrieved_data = rag_engine.query_documents(user_query)

    context_text = "\n\n".join([f"Source: {d['source']}\nContent: {d['text']}" for d in retrieved_data])
    
    prompt = f"""You are the official virtual assistant for the Centro Statistica Azienda (CSA). 
    
    INSTRUCTIONS:
    - If the user greets you or engages in general small talk (e.g., "Hi", "How are you?"), respond cordially in Italian as a friendly AI assistant.
    - If the user asks a specific question, use the provided DOCUMENTS to answer accurately in professional Italian.
    - If the question is technical/specific but NOT found in the DOCUMENTS, tell the user politely that you don't have that specific information in your records.
    - Always maintain the identity of Centro Statistica Azienda (CSA).

    DOCUMENTS:
    {context_text}
    
    USER QUESTION: {user_query}
    
    RESPONSE:"""
    

    llm_answer = get_hf_response(prompt)
    
    print(f"✅ RAG Response generated for Italian query")
    
    return llm_answer