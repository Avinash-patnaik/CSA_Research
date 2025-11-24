from .utils.llm_local import get_local_llm_response

def answer_query(user_query: str) -> str:
    llm_response =get_local_llm_response(user_query)
    
    return llm_response