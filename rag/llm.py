import os

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


@st.cache_resource(show_spinner=False)
def get_llm():
    """
    Create and cache the Groq LLM client.

    Cached via @st.cache_resource so the same ChatGroq client (and its
    underlying HTTP connection pool) is reused across reruns instead of
    being re-instantiated on every question or video processing call.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise Exception(
            "GROQ_API_KEY is missing. Please set it in your .env file."
        )

    llm = ChatGroq(
        api_key=api_key,
        model="llama-3.1-8b-instant",
        temperature=0,
    )

    return llm