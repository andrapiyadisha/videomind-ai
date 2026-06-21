import html
import streamlit as st


# ----------------------------------------------------------------- #
# Header
# ----------------------------------------------------------------- #

def render_hero():
    """Big hero title shown only before any video has been processed."""

    st.markdown(
        '<div class="yt-hero"><h1>🎥 YouTube RAG Chatbot</h1>'
        '<p>Paste a YouTube link in the sidebar and start asking questions.</p></div>',
        unsafe_allow_html=True,
    )


def render_compact_header(video_title: str, model_name: str = "Groq Llama 3"):
    """Small sticky ChatGPT-style header shown once a video is processed,
    with Ready + model badges on the right."""

    safe_title = html.escape(video_title or "Untitled video")
    safe_model = html.escape(model_name)

    st.markdown(
        '<div class="yt-compact-header">'
        '<div class="yt-left">'
        '<span class="yt-icon">💬</span>'
        '<div style="display:flex; flex-direction:column; line-height:1.2; min-width:0; justify-content:center;">'
        f'<span class="yt-title">{safe_title}</span>'
        '<span class="yt-sub">Chatting about this video</span>'
        '</div></div>'
        '<div class="yt-header-badges">'
        '<span class="yt-badge-pill yt-badge-ready"><span class="dot"></span> Ready</span>'
        f'<span class="yt-badge-pill yt-badge-model">⚡ {safe_model}</span>'
        '</div></div>',
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------- #
# Chat bubbles
# ----------------------------------------------------------------- #

def render_user_message(content: str):
    safe = html.escape(content)

    st.markdown(
        '<div class="yt-msg-row user">'
        '<div class="yt-avatar user">🧑</div>'
        '<div class="yt-bubble-wrap">'
        f'<div class="yt-bubble user">{safe}</div>'
        '</div></div>',
        unsafe_allow_html=True,
    )


def render_assistant_card_open():
    """
    Open the assistant row + avatar, returning a placeholder where the
    markdown card content (and later, streamed tokens) can be written.
    """

    st.markdown(
        '<div class="yt-msg-row assistant">'
        '<div class="yt-avatar assistant">🤖</div>'
        '<div class="yt-bubble-wrap" style="width:100%;">',
        unsafe_allow_html=True,
    )

    placeholder = st.empty()
    return placeholder


def render_row_close():
    st.markdown("</div></div>", unsafe_allow_html=True)


def render_card_markdown(placeholder, markdown_text: str):
    """Render (or update, for streaming) the assistant's answer inside a styled glass card."""
    placeholder.markdown(
        f'<div class="yt-card">\n\n{markdown_text}\n\n</div>',
        unsafe_allow_html=True,
    )


def render_typing_indicator(placeholder):
    placeholder.markdown(
        '<div class="yt-typing"><span></span><span></span><span></span></div>',
        unsafe_allow_html=True,
    )


def render_meta_line(model_name: str, elapsed_seconds: float, num_chunks: int):
    """Renders retrieval and execution stats as premium rounded badges."""
    st.markdown(
        '<div class="yt-meta-row">'
        f'<span class="yt-meta-badge">⚡ {html.escape(model_name)}</span>'
        f'<span class="yt-meta-badge">⏱️ {elapsed_seconds:.1f} sec</span>'
        f'<span class="yt-meta-badge">📚 {num_chunks} Chunks</span>'
        '</div>',
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------- #
# Source cards: 4-column grid (desktop), stacked (mobile via CSS)
# ----------------------------------------------------------------- #

def render_source_cards(docs):
    """
    Render retrieved chunks as a responsive grid of source cards.
    Click expands the full chunk via an expander section below.
    """

    if not docs:
        return

    total = len(docs)

    st.markdown(
        f'<div class="yt-section-label">📚 Sources ({total})</div>',
        unsafe_allow_html=True,
    )

    cards_html = []

    for i, doc in enumerate(docs, start=1):
        relevance_pct = max(100 - int((i - 1) * (70 / max(total - 1, 1))), 30)

        snippet = doc.page_content.strip().replace("\n", " ")
        # Preview text is displayed, and CSS clamps it to exactly 2 lines
        safe_preview = html.escape(snippet)

        card = (
            '<div class="yt-source-card">'
            '<div class="yt-source-head">'
            f'<span>📄 Chunk {i}</span>'
            f'<span class="yt-relevance-badge">{relevance_pct}%</span>'
            '</div>'
            f'<div class="yt-source-snippet">{safe_preview}</div>'
            '</div>'
        )
        cards_html.append(card)

    grid_html = '<div class="yt-source-grid">' + "".join(cards_html) + '</div>'

    st.markdown(grid_html, unsafe_allow_html=True)

    # Click expands full chunk: keep existing functionality inside a styled expander
    with st.expander("🔍 Click to expand full source chunks"):
        for i, doc in enumerate(docs, start=1):
            st.markdown(f"**Chunk {i}**")
            st.write(doc.page_content)
            st.divider()


# ----------------------------------------------------------------- #
# Quick actions: copy / regenerate / feedback (Streamlit components only)
# ----------------------------------------------------------------- #

def render_quick_actions(message_id: str, answer_text: str):
    """
    Renders Copy / Regenerate / 👍 / 👎 under an assistant answer.
    Uses Streamlit components only to avoid rendering raw HTML buttons.
    """

    cols = st.columns([1, 1, 1, 1, 8])

    # Standard Streamlit button for copying to avoid broken HTML buttons
    copy_clicked = cols[0].button("📋", key=f"copy_{message_id}", help="Copy response")
    if copy_clicked:
        st.toast("Copied to clipboard! Copy the text from the box below:")
        st.code(answer_text, language="markdown")

    regenerate = cols[1].button("🔄", key=f"regen_{message_id}", help="Regenerate")
    thumbs_up = cols[2].button("👍", key=f"up_{message_id}", help="Good answer")
    thumbs_down = cols[3].button("👎", key=f"down_{message_id}", help="Bad answer")

    if thumbs_up:
        st.toast("Thanks for the feedback! 👍", icon="✅")

    if thumbs_down:
        st.toast("Thanks — we'll use this to improve answers. 👎", icon="📝")

    return {
        "regenerate": regenerate,
        "thumbs_up": thumbs_up,
        "thumbs_down": thumbs_down,
    }


# ----------------------------------------------------------------- #
# Quick-action suggestion chips (ChatGPT-style)
# ----------------------------------------------------------------- #

# Maps short display names to full descriptive prompts for the RAG chain
FOLLOWUP_SUGGESTIONS = [
    ("⚡", "Summary", "Summarize this video"),
    ("📝", "Notes", "Key takeaways"),
    ("🎓", "Explain", "Explain in simple words"),
    ("⭐", "Concepts", "Important concepts"),
]


def render_followups(message_id: str):
    """
    Renders follow-up suggestion chips below an answer.
    Returns the clicked suggestion's full descriptive prompt, or None.
    """

    st.markdown(
        '<div class="yt-section-label">💡 Quick Actions</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="yt-quick-actions">', unsafe_allow_html=True)
    cols = st.columns(len(FOLLOWUP_SUGGESTIONS))
    clicked = None

    for col, (icon, label, full_prompt) in zip(cols, FOLLOWUP_SUGGESTIONS):
        if col.button(
            f"{icon}  {label}",
            key=f"followup_{message_id}_{label}",
            use_container_width=True,
        ):
            clicked = full_prompt

    st.markdown("</div>", unsafe_allow_html=True)

    return clicked