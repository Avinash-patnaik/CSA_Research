import chromadb
from chromadb.utils import embedding_functions
import os

CHROMA_PATH = "backend/data/chroma_db"

class RAGEngine:
    def __init__(self):
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="nickprock/sentence-bert-base-italian-uncased"
        )
        self.client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.collection = self.client.get_or_create_collection(
            name="csa_docs", 
            embedding_function=self.ef
        )

    def query_documents(self, user_query: str, n_results: int = 3):
        try:
            results = self.collection.query(
                query_texts=[user_query],
                n_results=n_results
            )
            return "\n\n".join(results.get('documents', [[]])[0])
        except Exception as e:
            return f"Error: {str(e)}"

rag_engine = RAGEngine()