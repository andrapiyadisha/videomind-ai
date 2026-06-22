import os
import streamlit as st
from langchain_groq import ChatGroq

@st.cache_resource
def get_llm():
    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        st.error("GROQ_API_KEY is missing on Render.")
        st.stop()

    return ChatGroq(
        api_key=api_key,
        model="llama-3.1-8b-instant",
        temperature=0,
    )