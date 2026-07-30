import time
import uuid

import streamlit as st

from ui.components import (
    render_hero,
    render_compact_header,
    render_user_message,
    render_assistant_card_open,
    render_row_close,
    render_card_markdown,
    render_typing_indicator,
    render_meta_line,
    render_source_cards,
    render_quick_actions,
    render_followups,
)


def _ask(question: str, retriever, chain):
    """
    Run retrieval + generation for a single question, streaming the
    answer into the UI token-by-token.

    Returns (answer_text, docs, elapsed_seconds).
    """
    
    if retriever is None or chain is None:
        return "⚠️ Please process a YouTube video first.", [], 0.0

    docs = retriever.invoke(question)

    context = "\n\n".join(doc.page_content for doc in docs)

    placeholder = render_assistant_card_open()
    render_typing_indicator(placeholder)

    start = time.time()
    answer_parts = []

    try:
        for token in chain.stream({"context": context, "question": question}):
            answer_parts.append(token)
            render_card_markdown(placeholder, "".join(answer_parts))
    except Exception as e:
        render_card_markdown(
            placeholder,
            f"⚠️ Something went wrong while generating the answer: {str(e)}",
        )
        render_row_close()
        return "".join(answer_parts), docs, time.time() - start

    elapsed = time.time() - start
    render_row_close()

    return "".join(answer_parts).strip(), docs, elapsed


def render_chat_panel(video_metadata, retriever, chain):
    """
    Renders the full conversation panel for the main content area:
    header, message history, input box, streaming, sources, quick
    actions, and follow-up suggestions.

    Sidebar is NOT touched by this function or anything it calls.
    """

    # ---- Header ---- #
    if video_metadata:
        render_compact_header(
            video_metadata.get("title", "Untitled video"),
            model_name="Groq Llama 3 (8B Instant)",
        )
    else:
        render_hero()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "pending_question" not in st.session_state:
        st.session_state.pending_question = None

    # ---- Render existing history ---- #
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            render_user_message(msg["content"])
        else:
            placeholder = render_assistant_card_open()
            render_card_markdown(placeholder, msg["content"])
            render_row_close()

            if msg.get("model_name"):
                render_meta_line(
                    msg["model_name"],
                    msg.get("elapsed", 0.0),
                    msg.get("num_chunks", 0),
                )

            if msg.get("docs"):
                render_source_cards(msg["docs"])

            actions = render_quick_actions(msg["id"], msg["content"])

            if actions["regenerate"]:
                st.session_state.pending_question = msg.get("question")
                # Drop this Q/A pair so a fresh one is appended below.
                st.session_state.messages = [
                    m for m in st.session_state.messages if m["id"] != msg["id"]
                ]
                st.rerun()

            clicked_followup = render_followups(msg["id"])
            
            # Subtle conversation divider before next question
            st.markdown('<div class="yt-conv-divider"></div>', unsafe_allow_html=True)
            
            if clicked_followup:
                st.session_state.pending_question = clicked_followup
                st.rerun()

    # ---- Input box (Streamlit pins st.chat_input to the bottom natively) ---- #
    video_loaded = retriever is not None and chain is not None
    if not video_loaded:
        st.info("📹 Please paste a YouTube URL and click **Process Video** before asking questions.")
    typed_question = st.chat_input(
        "Ask anything about this video...",
        disabled=not video_loaded
    )

    st.markdown(
        '<div class="yt-disclaimer">⚠️ Answers are generated based on the video '
        'transcript and may not always be 100% accurate.</div>',
        unsafe_allow_html=True,
    )

    question = st.session_state.pending_question or typed_question
    st.session_state.pending_question = None

    if question:
        if not video_loaded:
            st.warning("⚠️ Please process a YouTube video first.")
            st.stop()

        st.session_state.messages.append(
            {"id": str(uuid.uuid4()), "role": "user", "content": question}
        )
        
        render_user_message(question)

        model_name = "Groq Llama 3 (8B Instant)"

        answer, docs, elapsed = _ask(question, retriever, chain)

        message_id = str(uuid.uuid4())

        st.session_state.messages.append(
            {
                "id": message_id,
                "role": "assistant",
                "content": answer,
                "question": question,
                "docs": docs,
                "model_name": model_name,
                "elapsed": elapsed,
                "num_chunks": len(docs),
            }
        )

        render_meta_line(model_name, elapsed, len(docs))
        render_source_cards(docs)
        render_quick_actions(message_id, answer)
        render_followups(message_id)
        
        # Subtle conversation divider at the end of the exchange
        st.markdown('<div class="yt-conv-divider"></div>', unsafe_allow_html=True)
        st.rerun()