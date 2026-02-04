from .utils.llm_hf import get_hf_response
from .utils.rag_engine import rag_engine

def answer_query(user_query: str) -> str:
    
    retrieved_data = rag_engine.query_documents(user_query)
    
    context_text = "\n\n".join([f"Fonte: {d['source']}\nContenuto: {d['text']}" for d in retrieved_data])
    
    prompt = f"""Sei l'assistente ufficiale del Centro Statistica Azienda (CSA).
    Rispondi in italiano usando solo i documenti forniti.
    
    DOCUMENTI:
    {context_text}
    
    DOMANDA: {user_query}
    
    RISPOSTA:"""
    
    llm_answer = get_hf_response(prompt)
    
    unique_sources = list(set([d['source'] for d in retrieved_data]))
    sources_list = "\n\n**Fonti consultate:**\n" + "\n".join([f"- {s}" for s in unique_sources])
    
    return f"{llm_answer}{sources_list}"