# Containerized RAG Application

## Overview

This project is a fully containerized Retrieval-Augmented Generation (RAG) application built with FastAPI, Streamlit, ChromaDB, Ollama, and Docker Compose.

Users can index documents, ask questions about their content, and receive AI-generated answers with source citations. The project also includes automated testing and a GitHub Actions CI pipeline to verify that the backend works and both Docker images build successfully.

## Features

- **Streamlit:** Interactive interface for indexing documents and asking questions.
- **FastAPI:** Backend API for document ingestion, retrieval, and AI-generated answers.
- **Ollama:** Runs local language models for embeddings and text generation.
- **ChromaDB:** Stores document embeddings for semantic search.
- **Docker Compose:** Manages the backend, frontend, and Ollama containers.
- **Environment Variables:** Centralized configuration using `config.py` and `.env`.
- **Persistent Storage:** Docker volumes preserve document data and downloaded models.
- **Pytest:** Automated tests for the backend API.
- **GitHub Actions:** Automatically runs tests and verifies Docker builds on pushes and pull requests.

## Project Structure

```text
containerized-rag-app/
├── .github/
│   └── workflows/
│       └── ci.yml
├── backend/
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_api.py
│   ├── docs/
│   │   └── sample.txt
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Configuration

The application uses environment variables to manage its settings.

Create a `.env` file from `.env.example`:

```powershell
Copy-Item .env.example .env
```

Example configuration:

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

The `.env` file is excluded from Git to prevent local configuration and potential credentials from being committed.

## Running the Application

### Requirements

- Docker Desktop with Docker Compose
- Internet connection for downloading Docker images and Ollama models
- Python 3.11 for running backend tests locally

### 1. Start Docker Containers

From the project root:

```powershell
docker compose up --build -d
```

Verify that all three containers are running:

```powershell
docker compose ps
```

### 2. Download Ollama Models

Download the language model:

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

### 3. Open the Application

**Streamlit Frontend:** http://localhost:8501

**FastAPI Documentation:** http://localhost:8000/docs

**Health Endpoint:** http://localhost:8000/health

In Streamlit, click **Re-index Documents**, enter a question, and review the generated answer and source citations.

## API Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/` | GET | Returns application information |
| `/health` | GET | Checks Ollama connectivity and application status |
| `/stats` | GET | Returns the indexed document count and model information |
| `/ingest` | POST | Processes and indexes documents |
| `/ask` | POST | Retrieves relevant documents and generates an answer |

Test the health endpoint using PowerShell:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

## Running Tests Locally

The backend includes automated tests written with pytest.

### 1. Set Up Python 3.11

If Python 3.11 is not installed:

```powershell
py install 3.11
```

Navigate into the backend folder:

```powershell
cd backend
```

Create and activate a virtual environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
python -m pip install -r requirements.txt
python -m pip install pytest==8.3.5 httpx==0.27.2
```

### 3. Run Tests

```powershell
python -m pytest tests/test_api.py -v
```

The tests verify that:

1. The root endpoint returns HTTP 200.
2. The health endpoint returns HTTP 200 and the expected fields.
3. The stats endpoint returns HTTP 200 and includes `document_count`.

Tests use a temporary ChromaDB directory and mock Ollama responses, so a live model is not required.

## GitHub Actions CI

The project includes a GitHub Actions workflow located at:

```text
.github/workflows/ci.yml
```

The workflow runs automatically when code is pushed to `main` or a pull request is opened.

It contains two jobs:

**Backend Tests**

- Sets up Python 3.11.
- Installs backend dependencies.
- Runs pytest against the backend tests.

**Docker Build Verification**

- Builds the FastAPI backend Docker image.
- Builds the Streamlit frontend Docker image.
- Verifies that both images were created successfully.

CI results can be viewed under the **Actions** tab in the GitHub repository.

## How the RAG Pipeline Works

1. Documents are read from `backend/docs/`.
2. FastAPI splits the documents into smaller chunks.
3. Ollama generates embeddings using `nomic-embed-text`.
4. ChromaDB stores the document embeddings.
5. A user asks a question through Streamlit.
6. Ollama generates an embedding for the question.
7. ChromaDB retrieves relevant document chunks.
8. FastAPI builds a prompt using the retrieved context.
9. Ollama generates an answer using `llama3.2:1b`.
10. Streamlit displays the answer and source citations.

## Useful Docker Commands

Check running containers:

```powershell
docker compose ps
```

View logs:

```powershell
docker compose logs -f
```

Rebuild and restart:

```powershell
docker compose up --build -d
```

Stop containers:

```powershell
docker compose down
```

Named Docker volumes preserve ChromaDB data and Ollama models after containers are stopped.

## Future Improvements

- Support uploading PDF and Markdown documents.
- Add conversational chat history.
- Improve retrieval accuracy and source citations.
- Add more integration tests for document ingestion and retrieval.
- Expand CI to include additional code-quality checks.
- Improve the Streamlit interface.

## What I Learned

This project helped me understand how to build and test a multi-container AI application. I practiced connecting Streamlit, FastAPI, ChromaDB, and Ollama through Docker Compose while using environment variables and persistent volumes.

I also learned how to create automated API tests with pytest and configure GitHub Actions to run tests and verify Docker builds. This makes it easier to catch problems when changes are pushed to GitHub.