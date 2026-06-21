import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings


@st.cache_resource(show_spinner=False)
def get_embeddings():
    """
    Load and cache the embedding model.

    Cached via @st.cache_resource so the model (and its underlying
    PyTorch weights) is loaded into memory only once per Streamlit
    server process, instead of being reloaded on every "Process Video"
    click. This significantly speeds up repeated processing.
    """

    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={
            "device": "cpu"
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )

    return embeddings