from .utils.llm_hf import get_hf_response
from .utils.rag_engine import rag_engine

def answer_query(user_query: str) -> str:

    retrieved_data = rag_engine.query_documents(user_query)
    
    context_text = "\n\n".join([f"Source: {d['source']}\nContent: {d['text']}" for d in retrieved_data])
    
    prompt = f"""Tu sei l'assistente del Centro Statistica Azienda (CSA). 
    
    REGOLE DI RISPOSTA:
    1. NON iniziare la risposta con saluti ripetitivi come "Ciao! Sono felice di assisterti" o "Il CSA è qui per aiutarti".
    2. Vai direttamente alla risposta o al commento richiesto dall'utente.
    3. Rispondi in italiano professionale usando i DOCUMENTI se necessario.
    4. Se l'utente ti saluta per la prima volta, puoi rispondere al saluto brevemente, ma evita presentazioni lunghe.

    DOCUMENTI:
    {context_text}
    
    DOMANDA UTENTE: {user_query}
    
    RISPOSTA:"""
    
    llm_answer = get_hf_response(prompt)
    
    return llm_answer