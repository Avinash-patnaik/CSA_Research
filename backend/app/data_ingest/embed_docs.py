import os
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader

DOCS_DIR = "backend/data/documents"
TRANSCRIPTS_DIR = "backend/data/transcripts"
CHROMA_PATH = "backend/data/chroma_db"

def process_tabular_data(file_path):
    """Converts CSV/Excel rows into text strings for embedding."""
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    
    row_strings = []
    for _, row in df.iterrows():
        row_str = ", ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
        row_strings.append(row_str)
    return row_strings

def run_ingestion():
    huggingface_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(
        name="csa_docs", 
        embedding_function=huggingface_ef
    )

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    for target_dir in [DOCS_DIR, TRANSCRIPTS_DIR]:
        if not os.path.exists(target_dir): continue
        
        for filename in os.listdir(target_dir):
            file_path = os.path.join(target_dir, filename)
            
            if filename.endswith((".pdf", ".txt")):
                loader = PyPDFLoader(file_path) if filename.endswith(".pdf") else TextLoader(file_path)
                docs = loader.load()
                chunks = [c.page_content for c in text_splitter.split_documents(docs)]
            
            elif filename.endswith((".csv", ".xlsx", ".xls")):
                print(f"Processing tabular file: {filename}")
                chunks = process_tabular_data(file_path)
            
            else:
                continue

            collection.upsert(
                documents=chunks,
                metadatas=[{"source": filename} for _ in chunks],
                ids=[f"{filename}_{i}" for i in range(len(chunks))]
            )
            print(f"✅ Indexed: {filename}")

if __name__ == "__main__":
    run_ingestion()