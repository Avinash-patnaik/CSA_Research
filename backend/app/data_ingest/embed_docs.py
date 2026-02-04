import os
import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader


DOCS_DIR = "backend/data/documents"
CHROMA_PATH = "backend/data/chroma_db"

def run_ingestion():

    huggingface_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(
        name="csa_docs", 
        embedding_function=huggingface_ef
    )

    print(f"--- Loading documents from {DOCS_DIR} ---")
    loader = DirectoryLoader(
        DOCS_DIR, 
        glob="**/*.pdf", 
        loader_cls=PyPDFLoader
    )
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(docs)

    documents = [c.page_content for c in chunks]
    metadatas = [c.metadata for c in chunks]
    ids = [f"id_{i}" for i in range(len(chunks))]

    print(f"--- Ingesting {len(chunks)} chunks into ChromaDB ---")
    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print("--- Ingestion Complete! ---")

if __name__ == "__main__":
    run_ingestion()