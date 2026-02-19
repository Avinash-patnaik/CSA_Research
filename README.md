## CSA Chatbot Agent: Enterprise RAG & SQL Intelligence
This repository contains the source code for the CSA Chatbot Agent, a sophisticated dual-engine AI assistant designed to bridge the gap between structured relational data and unstructured organizational knowledge. It leverages a combination of Natural Language to SQL and Retrieval-Augmented Generation (RAG) to provide comprehensive business intelligence.
+1

## Project Overview
The CSA Chatbot serves as a centralized intelligence hub. It utilizes a FastAPI backend to route user queries through two primary channels:


Relational Intelligence: Direct, read-only querying of MySQL databases via a dedicated SQL engine.


Knowledge Base Intelligence: Semantic search across PDF documents and transcribed video content using vector embeddings.

## Technical Stack
### Backend (Python 3.12+)

Core Framework: fastapi[all] (v0.115.2) for high-performance asynchronous API handling.


Data Validation: pydantic (v2.11.7) for strict schema enforcement and FastAPI compatibility.


Database Integration: mysql-connector-python (v8.2.0) for secure relational data access.


Vector Store: chromadb (v0.4.24) for high-speed similarity searches.


AI/ML Models: * openai (v1.30.1) for advanced reasoning and GPT-based queries.
+1


sentence-transformers (v2.2.2) for local embedding generation.


openai-whisper for automated video and audio transcription.


Server: uvicorn (v0.29.0) as the ASGI interface.

### Frontend (React & TypeScript)

Build Tool: Vite for optimized asset delivery.


Styling: Tailwind CSS and PostCSS for a responsive, modern UI.


State Management: Specialized React hooks, components, and TypeScript for type safety.


Package Management: Support for both npm and bun environments.

## Deployment & Installation
### 1. Environment Configuration
Create a .env file in the backend/ directory to manage sensitive configuration:
+1


OPENAI_API_KEY: Required for GPT-4 and Whisper integration.
+1


MYSQL_CONFIG: Connection parameters for the mysql-connector-python client.

### 2. Docker Orchestration
The system is fully containerized for consistent deployment across environments.

Bash
# Build and launch the entire stack
docker-compose up --build

Backend: Runs via the Dockerfile.backend configuration.


Frontend: Built and served via the Dockerfile.frontend configuration.

### 3. Data Ingestion Pipeline
To populate the knowledge base, utilize the scripts in backend/app/data_ingest/:

Place documents in data/documents/ and media in data/transcripts/.

Run video_transcriber.py to generate text from video assets.

Run embed_docs.py to index content into chromadb.

## Research & Development
Experimental SQL queries, embedding tests, and logic refinements can be found in the notebooks/dev_experiments.ipynb file.