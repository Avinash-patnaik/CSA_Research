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

    def search(self, query: str, top_k: int = 3):

        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )

        return "\n\n".join(results['documents'][0])

rag_engine = RAGEngine()