import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

@st.cache_resource(show_spinner=False)
def get_llm():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        st.error("GROQ_API_KEY is missing.")
        st.stop()

    return ChatGroq(
        api_key=api_key,
        model="llama-3.1-8b-instant",
        temperature=0,
    )