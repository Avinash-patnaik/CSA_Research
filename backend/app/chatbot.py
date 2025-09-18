# backend/app/chatbot.py
def answer_query(query: str) -> str:
    if "blaise" in query.lower():
        return "This looks like a Blaise-related query. (Stub response)"
    return f"You asked: {query}"
