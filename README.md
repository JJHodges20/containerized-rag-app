# Docker Compose RAG Demo

## Overview

This project is a Docker-based Python application that demonstrates how FastAPI, Ollama, and ChromaDB can work together using Docker Compose.

The application uses a centralized `Settings` class to manage environment variables, making it easy to change models, database paths, and application settings without modifying the source code.

## Features

- FastAPI backend with API and health-check endpoints
- Ollama integration for running local language models
- Persistent ChromaDB document collection
- Docker Compose for managing multiple services
- Centralized environment configuration using `config.py`
- `.env` and `.env.example` for configuration management
- Persistent Docker volumes for database and model storage
- Environment variable validation and default values

## Project Structure

```text
compose-demo/
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
└── backend/
    ├── .dockerignore
    ├── Dockerfile
    ├── config.py
    ├── main.py
    ├── requirements.txt
    └── docs/
        └── sample.txt
```

## Configuration

Application settings are managed through the `Settings` class in `backend/config.py`.

The `.env` file contains the configuration used by Docker Compose.

Example:

```dotenv
OLLAMA_URL=http://ollama:11434
MODEL_NAME=llama3.2:1b
CHROMA_PATH=/app/chroma_data
MAX_RESULTS=5
CONFIDENCE_THRESHOLD=0.75
DEBUG=false
```

The application supports the following settings:

| Variable | Purpose |
| --- | --- |
| `OLLAMA_URL` | Address of the Ollama service |
| `MODEL_NAME` | Configured language model |
| `CHROMA_PATH` | Persistent ChromaDB storage location |
| `MAX_RESULTS` | Maximum number of future retrieval results |
| `CONFIDENCE_THRESHOLD` | Threshold reserved for future retrieval filtering |
| `DEBUG` | Enables or disables debug mode |

The `.env` file is excluded from Git and Docker build contexts, while `.env.example` provides a safe configuration template.

## Getting Started

**Requirements:**
- Docker Desktop
- Docker Compose
- An internet connection for the initial image and model downloads

### 1. Configure the Environment

Create a `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

### 2. Build and Start the Application

```powershell
docker compose up --build -d
```

Check the running containers:

```powershell
docker compose ps
```

### 3. Download the Ollama Model

If the model has not already been downloaded:

```powershell
docker compose exec ollama ollama pull llama3.2:1b
```

Verify the installed models:

```powershell
docker compose exec ollama ollama list
```

### 4. Test the API

Open the following URLs:

**Application:** http://localhost:8000

**Health check:** http://localhost:8000/health

**Swagger documentation:** http://localhost:8000/docs

You can also test the health endpoint from PowerShell:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

The health endpoint reports Ollama connectivity, the configured model, and the number of documents in ChromaDB.

## Testing Environment Variables

To verify that environment variable changes take effect:

1. Open `.env`.
2. Change `MODEL_NAME` to another value.
3. Save the file.
4. Recreate the backend container:

```powershell
docker compose up -d --no-deps --force-recreate backend
```

5. Run:

```powershell
Invoke-RestMethod http://localhost:8000/
```

The returned model name should match the new value in `.env`.

Changing a setting requires recreating the container because restarting an existing container does not reload its environment variables.

If you want to use a different model for actual AI requests, that model must also be downloaded into Ollama.

## Managing Containers

View logs:

```powershell
docker compose logs -f
```

Stop the application:

```powershell
docker compose down
```

The named Docker volumes preserve ChromaDB data and downloaded Ollama models after the containers are stopped or recreated.

## Current Limitations

The current version initializes ChromaDB and verifies connectivity to Ollama, but it does not yet implement a complete retrieval-augmented generation pipeline.

The `sample.txt` file provides example documentation but is not automatically ingested into ChromaDB.

Document ingestion, semantic search, and AI-generated responses using retrieved context are potential future improvements.

## What I Learned

This project helped me understand how to manage application configuration through environment variables instead of hardcoding values. I also practiced connecting multiple Docker containers, using persistent volumes, and verifying that configuration changes take effect when containers are recreated.

Centralizing the settings makes the application easier to maintain and prepares it for adding more functionality in the future.