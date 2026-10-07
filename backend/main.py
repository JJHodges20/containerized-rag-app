import os

import chromadb
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="RAG API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Configuration from environment variables
OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434",
)

MODEL = os.getenv(
    "MODEL_NAME",
    "llama3.2:1b",
)


# Persistent ChromaDB storage
client = chromadb.PersistentClient(
    path="/app/chroma_data"
)

collection = client.get_or_create_collection(
    name="documents"
)


@app.get("/")
def root():
    return {
        "message": "RAG API running in Docker",
        "model": MODEL,
    }


@app.get("/health")
def health():
    ollama_ok = False

    try:
        response = requests.get(
            f"{OLLAMA_URL}/api/tags",
            timeout=3,
        )

        ollama_ok = (
            response.status_code == 200
        )

    except requests.RequestException:
        pass


    return {
        "status": "healthy",
        "ollama": (
            "connected"
            if ollama_ok
            else "unavailable"
        ),
        "ollama_url": OLLAMA_URL,
        "documents": collection.count(),
    }