# Full Containerized RAG Application

## Overview

This project is a fully containerized Retrieval-Augmented Generation (RAG) application built with Docker Compose, FastAPI, Streamlit, ChromaDB, and Ollama.

Users can index text documents, ask questions about their content, and receive AI-generated answers with source citations. Docker Compose manages the three services and allows them to communicate over an internal network.

## Features

- **Streamlit Frontend:** Interactive interface for indexing documents and asking questions.
- **FastAPI Backend:** Handles document processing, semantic search, and AI requests.
- **Ollama:** Runs local language models for embeddings and answer generation.
- **ChromaDB:** Stores document embeddings and retrieves relevant information.
- **Source Citations:** Displays the documents used to generate answers.
- **Centralized Configuration:** Uses environment variables managed through `config.py`.
- **Persistent Storage:** Docker volumes preserve indexed documents and downloaded models.

## Project Structure

```text
compose-demo/
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── requirements.txt
│   ├── config.py
│   ├── main.py
│   └── docs/
│       └── sample.txt
└── frontend/
    ├── Dockerfile
    ├── requirements.txt
    └── app.py
```

## Configuration

The application uses a `.env` file to manage settings.

```dotenv
OLLAMA_URL=http://ollama:11434
MODEL_NAME=llama3.2:1b
EMBED_MODEL=nomic-embed-text
CHROMA_PATH=/app/chroma_data
DOCS_PATH=/app/docs
MAX_RESULTS=5
CONFIDENCE_THRESHOLD=0.65
DEBUG=false
```

The `.env.example` file provides a configuration template without exposing sensitive information.

## Getting Started

### Requirements

- Docker Desktop
- Docker Compose
- Internet connection for the initial downloads

### 1. Configure Environment Variables

Create your `.env` file:

```powershell
Copy-Item .env.example .env
```

### 2. Build and Start the Containers

Run from the root project directory:

```powershell
docker compose up --build -d
```

Verify the services:

```powershell
docker compose ps
```

Three containers should be running: `backend`, `frontend`, and `ollama`.

### 3. Download Ollama Models

Download the chat model:

```powershell
docker compose exec ollama ollama pull llama3.2:1b
```

Download the embedding model:

```powershell
docker compose exec ollama ollama pull nomic-embed-text
```

Verify installation:

```powershell
docker compose exec ollama ollama list
```

The models are stored in a persistent Docker volume and do not need to be downloaded after every restart.

## Using the Application

### Streamlit Frontend

Open:

http://localhost:8501

1. Check that the backend and Ollama are connected.
2. Click **Re-index Documents**.
3. Wait for the documents to be processed.
4. Enter a question about the indexed documents.
5. Click **Ask Question**.
6. Review the generated answer and source citations.

### FastAPI Backend

API documentation:

http://localhost:8000/docs

Health endpoint:

http://localhost:8000/health

Available endpoints:

| Endpoint | Method | Description |
| --- | --- | --- |
| `/` | GET | Displays application and model information |
| `/health` | GET | Checks Ollama connectivity and document count |
| `/ingest` | POST | Indexes text documents into ChromaDB |
| `/ask` | POST | Retrieves relevant context and generates an AI response |

Test the health endpoint in PowerShell:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

## How the RAG Pipeline Works

1. The user clicks **Re-index Documents**.
2. FastAPI reads the `.txt` files inside `backend/docs/`.
3. Documents are divided into smaller chunks.
4. Ollama generates embeddings using `nomic-embed-text`.
5. ChromaDB stores the chunks and embeddings.
6. The user submits a question through Streamlit.
7. Ollama converts the question into an embedding.
8. ChromaDB retrieves relevant chunks using similarity search.
9. FastAPI sends the retrieved context and question to `llama3.2:1b`.
10. Ollama generates an answer, which Streamlit displays along with source references.

The assistant is instructed to answer using the retrieved document context rather than inventing unsupported information.

## Docker Compose Services

| Service | Technology | Port |
| --- | --- | --- |
| Frontend | Streamlit | 8501 |
| Backend | FastAPI + ChromaDB | 8000 |
| AI Model | Ollama | 11434 (internal only) |

The frontend communicates with FastAPI using `http://backend:8000`.

The backend communicates with Ollama using `http://ollama:11434`.

Docker Compose handles communication between the containers through its internal network.

## Managing the Containers

Check container status:

```powershell
docker compose ps
```

View application logs:

```powershell
docker compose logs -f
```

Stop the application:

```powershell
docker compose down
```

Docker volumes preserve the ChromaDB database and downloaded Ollama models even when the containers are removed.

## Troubleshooting

| Issue | Suggested Fix |
| --- | --- |
| Docker connection error | Ensure Docker Desktop is running |
| Streamlit won't load | Check `docker compose logs frontend` |
| Backend unavailable | Check `docker compose logs backend` |
| Ollama unavailable | Verify the Ollama container is running |
| Model not found | Pull the required model into the Ollama container |
| No documents indexed | Click Re-index Documents |
| No relevant results | Verify the documents contain relevant information and adjust the similarity threshold |

## Future Improvements

Potential improvements include:

- Uploading documents directly through Streamlit.
- Supporting PDF and Markdown documents.
- Adding conversational chat history.
- Displaying retrieved document excerpts.
- Improving the frontend design.
- Adding retrieval evaluation and more advanced guardrails.

## What I Learned

This project helped me understand how multiple Docker containers can work together to create a complete AI application. I practiced connecting Streamlit to FastAPI, using Ollama for local language models, and storing document embeddings with ChromaDB.

I also learned how environment variables, persistent volumes, and Docker Compose make it easier to configure and manage a multi-service application.