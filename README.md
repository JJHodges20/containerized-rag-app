# Docker Compose RAG Demo

A Docker Compose project that runs a FastAPI backend and an Ollama service together in separate containers.

The backend uses ChromaDB for persistent document storage and communicates with Ollama over Docker’s internal network.

## Features

- FastAPI backend
- Ollama running in its own container
- ChromaDB persistent storage
- Docker Compose service orchestration
- Environment variable configuration
- Persistent Docker volumes
- Health check endpoint
- Local API access through port 8000

## Project Structure

```text
compose-demo/
├── docker-compose.yml
├── .env
└── backend/
    ├── Dockerfile
    ├── main.py
    ├── requirements.txt
    └── docs/
        └── sample.txt
```

## Environment Variables

Example `.env` file:

```text
MODEL_NAME=llama3.2:1b
OLLAMA_URL=http://ollama:11434
```

The backend can reach Ollama using the Compose service name `ollama`.

## Start the Project

Build and start the containers in detached mode:

```powershell
docker compose up --build -d
```

Check running services:

```powershell
docker compose ps
```

## Pull the Ollama Model

The first time the project runs, pull the model into the Ollama container:

```powershell
docker compose exec ollama ollama pull llama3.2:1b
```

Verify the model:

```powershell
docker compose exec ollama ollama list
```

The Ollama model is stored in a persistent Docker volume, so it does not need to be downloaded every time the containers restart.

## Test the API

Open:

```text
http://localhost:8000
```

Health endpoint:

```text
http://localhost:8000/health
```

Swagger UI:

```text
http://localhost:8000/docs
```

You can also test the health endpoint from PowerShell:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

## Stop the Project

Stop and remove the containers with:

```powershell
docker compose down
```

The Docker volumes remain unless they are explicitly removed.

## Purpose

This project demonstrates how Docker Compose can coordinate multiple services in one application. FastAPI and Ollama run independently but communicate over Docker’s internal network, while ChromaDB and Ollama data are preserved using Docker volumes.