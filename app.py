import streamlit as st

from ui.sidebar import render_sidebar, render_video_info
from ui.styles import inject_custom_css
from ui.chat import render_chat_panel
from loaders.youtube_loader import extract_video_id, load_youtube
from loaders.metadata import get_video_metadata

from rag.chunker import split_documents
from rag.embeddings import get_embeddings
from rag.vectorstore import create_vectorstore
from rag.retriever import get_retriever
from rag.llm import get_llm
from rag.chain import create_chain

st.set_page_config(
    page_title="YouTube RAG",
    page_icon="🎥",
    layout="wide",
)

inject_custom_css()

# ---------------- Session State ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "processed" not in st.session_state:
    st.session_state.processed = False

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "chain" not in st.session_state:
    st.session_state.chain = None

if "video_id" not in st.session_state:
    st.session_state.video_id = None

if "video_metadata" not in st.session_state:
    st.session_state.video_metadata = None

# ---------------- Sidebar (UNTOUCHED) ---------------- #

youtube_url, process = render_sidebar()

if st.session_state.processed and st.session_state.video_metadata:
    render_video_info(st.session_state.video_metadata)

# ---------------- Process Video ---------------- #

if process:

    video_id = extract_video_id(youtube_url)

    if not video_id:
        st.error("Invalid YouTube URL")
        st.stop()

    # Don't rebuild if same video
    if st.session_state.video_id != video_id:

        try:

            with st.spinner("Fetching video info..."):
                metadata = get_video_metadata(video_id)

            with st.spinner("Processing video..."):

                docs = load_youtube(video_id)

                chunks = split_documents(docs)

                embeddings = get_embeddings()

                vectorstore = create_vectorstore(
                    chunks,
                    embeddings
                )

                retriever = get_retriever(vectorstore)

                llm = get_llm()

                chain = create_chain(llm)

            # Save
            st.session_state.retriever = retriever
            st.session_state.chain = chain
            st.session_state.processed = True
            st.session_state.video_id = video_id
            st.session_state.video_metadata = metadata
            st.session_state.transcript = docs[0].page_content if docs else ""

            # New video -> always start a fresh conversation (requirement 14)
            st.session_state.messages = []

            st.toast("✅ Video processed successfully!", icon="🎬")

            st.rerun()

        except Exception as e:
            st.error(f"Couldn't process this video: {str(e)}")

    else:
        st.toast("This video is already processed.", icon="ℹ️")

# ---------------- Main content area: chat panel ---------------- #

render_chat_panel(
    video_metadata=st.session_state.video_metadata,
    retriever=st.session_state.retriever,
    chain=st.session_state.chain,
)