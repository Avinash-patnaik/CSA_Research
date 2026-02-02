from .utils.llm_hf import get_hf_response, get_local_llm_response

def answer_query(user_query: str) -> str:
    llm_response =get_hf_response(user_query)
    
    return llm_response