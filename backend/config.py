import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    ollama_url: str = "http://localhost:11434"
    model_name: str = "llama3.2:1b"
    chroma_path: str = "./chroma_data"
    max_results: int = 5
    confidence_threshold: float = 0.75
    debug: bool = False

    @classmethod
    def from_env(cls) -> "Settings":
        max_results = int(os.getenv("MAX_RESULTS", "5"))

        confidence_threshold = float(
            os.getenv("CONFIDENCE_THRESHOLD", "0.75")
        )

        debug = os.getenv("DEBUG", "false").lower() in (
            "true",
            "1",
            "yes",
        )

        if max_results < 1:
            raise ValueError("MAX_RESULTS must be at least 1.")

        if not 0 <= confidence_threshold <= 1:
            raise ValueError(
                "CONFIDENCE_THRESHOLD must be between 0 and 1."
            )

        return cls(
            ollama_url=os.getenv(
                "OLLAMA_URL", "http://localhost:11434"
            ).rstrip("/"),
            model_name=os.getenv(
                "MODEL_NAME", "llama3.2:1b"
            ),
            chroma_path=os.getenv(
                "CHROMA_PATH", "./chroma_data"
            ),
            max_results=max_results,
            confidence_threshold=confidence_threshold,
            debug=debug,
        )


settings = Settings.from_env()