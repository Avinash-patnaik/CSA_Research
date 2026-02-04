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
            chunks = results.get('documents', [[]])[0]
            metadatas = results.get('metadatas', [[]])[0]
            
            retrieved_data = []
            for text, meta in zip(chunks, metadatas):
                source_name = meta.get("source", "Documento Sconosciuto")
                retrieved_data.append({"text": text, "source": source_name})
                
            return retrieved_data
        except Exception as e:
            print(f"Errore RAG: {e}")
            return []

rag_engine = RAGEngine()