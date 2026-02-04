from .utils.llm_hf import get_hf_response
from .utils.rag_engine import rag_engine

def answer_query(user_query: str) -> str:

    context = rag_engine.query_documents(user_query)

    prompt = f"""Sei un Assistente di Ricerca CSA. Usa i documenti forniti per rispondere alla domanda in modo accurato.
    Se la risposta non è presente nei documenti, dì che non lo sai. Rispondi sempre in italiano.

    DOCUMENTI:
    {context}
    
    DOMANDA: {user_query}
    
    RISPOSTA:"""
    
    return get_hf_response(prompt)