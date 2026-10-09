import chromadb
import requests

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings


app = FastAPI(
    title="RAG API",
    version="1.1.0",
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize ChromaDB using centralized settings.

client = chromadb.PersistentClient(
    path=settings.chroma_path
)

collection = client.get_or_create_collection(
    name="documents"
)


@app.get("/")
def root():
    return {
        "message": "RAG API running in Docker",
        "model": settings.model_name,
        "max_results": settings.max_results,
        "confidence_threshold": settings.confidence_threshold,
        "debug": settings.debug,
    }


@app.get("/health")
def health():
    ollama_ok = False

    try:
        response = requests.get(
            f"{settings.ollama_url}/api/tags",
            timeout=3,
        )

        ollama_ok = response.status_code == 200

    except requests.RequestException:
        pass

    return {
        "status": "healthy",
        "ollama": (
            "connected" if ollama_ok else "unavailable"
        ),
        "ollama_url": settings.ollama_url,
        "model": settings.model_name,
        "documents": collection.count(),
    }