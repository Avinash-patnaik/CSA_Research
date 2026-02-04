import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
import os

CHROMA_PATH = "backend/data/chroma_db"

def get_vector_db():
    
    huggingface_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(
        name="Istat_docs",
        embedding_function=huggingface_ef
    )
    
def ingest_documents(docs):
    vector_db = get_vector_db()
    
    texts = [doc['text'] for doc in docs]
    metadatas = [{'source': doc['source']} for doc in docs]
    ids = [str(i) for i in range(len(docs))]
    
    vector_db.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )