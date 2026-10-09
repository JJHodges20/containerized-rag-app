
import os

import requests
import streamlit as st


BACKEND_URL = os.getenv(
    "BACKEND_URL", "http://backend:8000"
).rstrip("/")

st.set_page_config(
    page_title="RAG Knowledge Assistant",
    page_icon="📚",
    layout="wide",
)

st.title("📚 RAG Knowledge Assistant")
st.caption(
    "Ask questions about your documents using "
    "ChromaDB, FastAPI, and Ollama."
)


def api_request(method, endpoint, **kwargs):
    try:
        response = requests.request(
            method,
            f"{BACKEND_URL}{endpoint}",
            timeout=180,
            **kwargs,
        )

        response.raise_for_status()
        return response.json(), None

    except requests.RequestException as exc:
        detail = str(exc)

        if exc.response is not None:
            try:
                detail = exc.response.json().get(
                    "detail", detail
                )
            except ValueError:
                pass

        return None, detail


with st.sidebar:
    st.header("System Status")

    health, error = api_request("GET", "/health")

    if error:
        st.error("Backend unavailable")
        st.caption(error)
    else:
        st.success("Backend connected")
        st.write(
            "Ollama:",
            health["ollama"],
        )
        st.write(
            "Chat model:",
            health["model"],
        )
        st.write(
            "Indexed chunks:",
            health["documents"],
        )

    st.divider()

    st.subheader("Document Index")

    if st.button(
        "🔄 Re-index Documents",
        use_container_width=True,
    ):
        with st.spinner("Indexing documents..."):
            result, error = api_request(
                "POST", "/ingest"
            )

        if error:
            st.error(error)
        else:
            st.success(
                f"Indexed {result['files']} files "
                f"into {result['chunks']} chunks."
            )
            st.rerun()


st.subheader("Ask a Question")

question = st.text_input(
    "What would you like to know?",
    placeholder=(
        "How does Docker Compose connect "
        "the backend to Ollama?"
    ),
)

if st.button(
    "Ask Question",
    type="primary",
    disabled=not question.strip(),
):
    with st.spinner("Searching and generating an answer..."):
        result, error = api_request(
            "POST",
            "/ask",
            json={"question": question},
        )

    if error:
        st.error(error)
    else:
        st.session_state["last_result"] = result
        st.session_state["last_question"] = question


if "last_result" in st.session_state:
    result = st.session_state["last_result"]

    st.divider()
    st.subheader("Answer")

    st.markdown(result["answer"])

    st.subheader("Sources")

    if result["sources"]:
        for source in result["sources"]:
            st.write(
                f"**[{source['id']}] "
                f"{source['source']}**"
                f" — similarity: {source['similarity']:.3f}"
            )
    else:
        st.info("No relevant sources were found.")
