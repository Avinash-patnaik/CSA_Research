from .utils.llm_hf import get_hf_response
from .utils.rag_engine import rag_engine

def answer_query(user_query: str) -> str:
    
    context = rag_engine.query_documents(user_query)


    prompt = f"""Sei l'assistente virtuale ufficiale di CSA, che sta per 'Centro Statistica Azienda'.
    
    REGOLE IMPORTANTI:
    - Quando ti riferisci a CSA, usa sempre il nome completo: 'Centro Statistica Azienda'.
    - Rispondi in modo professionale e cordiale in lingua italiana e inglese.
    - Usa solo le informazioni fornite nei DOCUMENTI qui sotto per rispondere.
    - Se la risposta non è presente, dì gentilmente che non lo sai.

    DOCUMENTI:
    {context}
    
    DOMANDA: {user_query}
    
    RISPOSTA:"""
    
    return get_hf_response(prompt)