import chromadb
from chromadb.utils import embedding_functions
import os 


CHROMA_PATH = os.path.join(os.getcwd(), "backend/data/chroma_db")

class RAGEngine:
    def __init__(self):
        
        self.huggingface_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        self.client = chromadb.PersistentClient(path=CHROMA_PATH)
        
        self.collection = self.client.get_or_create_collection(
            name="csa_docs", 
            embedding_function=self.huggingface_ef
        )
        
    def query_documents(self, user_query: str, n_results: int = 3):
        """
        Searches Chromadb for the most relevant documents to the user query.
        """
        try:
            results = self.collection.query(
                query_texts=[user_query],
                n_results=n_results
            )
            context_list = results.get('documents', [[]])[0]
            context_text = "\n\n".join(context_list)
            
            return context_text if context_text else "No relevant documents found."
            
        except Exception as e:
            return f"Error querying local database: {str(e)}"

rag_engine = RAGEngine()