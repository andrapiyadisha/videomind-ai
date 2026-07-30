import html
import streamlit as st

from loaders.youtube_loader import extract_video_id


# ----------------------------------------------------------------- #
# Sidebar-only styling (scoped strictly to the sidebar container)
# ----------------------------------------------------------------- #

def _inject_sidebar_css():
    st.markdown(
        """
        <style>

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0a0e1f 0%, #050816 100%);
            border-right: 1px solid rgba(255, 255, 255, 0.06);
        }

        section[data-testid="stSidebar"] .block-container {
            padding-top: 1rem !important;
        }

        /* Logo / brand row */
        .yt-sb-logo {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            margin-bottom: 1.2rem !important;
            padding-bottom: 0.8rem !important;
            border-bottom: 1px solid rgba(255,255,255,0.07);
        }

        .yt-sb-logo-icon {
            width: 38px;
            height: 38px;
            border-radius: 11px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            background: linear-gradient(135deg, #6C63FF 0%, #3B82F6 100%);
            box-shadow: 0 4px 14px rgba(108, 99, 255, 0.35);
        }

        .yt-sb-logo-text {
            line-height: 1.15;
        }

        .yt-sb-logo-text .main {
            font-size: 1.02rem;
            font-weight: 700;
            color: #f1f1f6;
        }

        .yt-sb-logo-text .sub {
            font-size: 0.92rem;
            font-weight: 700;
            background: linear-gradient(135deg, #6C63FF, #3B82F6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] .yt-sb-heading {
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            color: #9a9cab;
            margin-bottom: 0.5rem;
        }

        section[data-testid="stSidebar"] .yt-sb-section {
            margin-bottom: 1rem !important;
        }

        section[data-testid="stSidebar"] .yt-sb-helper {
            font-size: 0.74rem;
            color: #7e8090;
            margin-top: -0.3rem;
            margin-bottom: 0.7rem;
        }

        /* Inputs */
        section[data-testid="stSidebar"] input[type="text"] {
            background: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid rgba(255, 255, 255, 0.09) !important;
            border-radius: 12px !important;
            color: #e7e8ee !important;
        }

        section[data-testid="stSidebar"] input[type="text"]:focus {
            border-color: rgba(108, 99, 255, 0.55) !important;
            box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.15) !important;
        }

        /* Rounded, consistent buttons of equal height */
        section[data-testid="stSidebar"] button {
            border-radius: 12px !important;
            height: 38px !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: all 0.18s ease;
        }

        /* Primary button (Process Video) */
        section[data-testid="stSidebar"] button[kind="primary"] {
            background: linear-gradient(135deg, #6C63FF 0%, #3B82F6 100%) !important;
            border: none !important;
            box-shadow: 0 4px 16px rgba(108, 99, 255, 0.3);
            font-weight: 600;
        }

        section[data-testid="stSidebar"] button[kind="primary"]:hover:not(:disabled) {
            filter: brightness(1.08);
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(108, 99, 255, 0.4);
        }

        /* Secondary outlined button (Load New Video) */
        section[data-testid="stSidebar"] button[kind="secondary"] {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.16) !important;
            color: #d6d7e0 !important;
        }

        section[data-testid="stSidebar"] button[kind="secondary"]:hover:not(:disabled) {
            border-color: rgba(108, 99, 255, 0.55) !important;
            color: #fff !important;
            transform: translateY(-1px);
        }

        /* Ghost button (Clear URL) */
        section[data-testid="stSidebar"] .yt-sb-ghost button {
            background: transparent !important;
            border: none !important;
            color: #7e8090 !important;
            font-size: 0.76rem !important;
            padding: 0.1rem 0.3rem !important;
            box-shadow: none !important;
            height: 24px !important;
        }

        section[data-testid="stSidebar"] .yt-sb-ghost button:hover:not(:disabled) {
            color: #e7e8ee !important;
            text-decoration: underline;
        }

        button:disabled {
            opacity: 0.4 !important;
            cursor: not-allowed !important;
        }

        /* Ready badge */
        .yt-sb-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.76rem;
            font-weight: 600;
            color: #6ee7a8;
            background: rgba(110, 231, 168, 0.1);
            border: 1px solid rgba(110, 231, 168, 0.3);
            padding: 0.32rem 0.75rem;
            border-radius: 999px;
            margin-bottom: 1rem;
        }

        .yt-sb-badge .dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #6ee7a8;
            box-shadow: 0 0 6px rgba(110, 231, 168, 0.8);
        }

        section[data-testid="stSidebar"] hr {
            margin: 1rem 0 !important;
            border-color: rgba(255, 255, 255, 0.07);
        }

        /* Video info glass card wrapper */
        .yt-sb-info-card {
            background: rgba(255, 255, 255, 0.035);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 18px;
            padding: 0.8rem;
            margin-bottom: 0.4rem;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
        }

        .yt-sb-info-card img {
            border-radius: 12px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }

        .yt-sb-info-card img:hover {
            transform: scale(1.02) !important;
            box-shadow: 0 6px 20px rgba(108, 99, 255, 0.25) !important;
        }

        .yt-sb-info-title {
            font-size: 0.88rem;
            font-weight: 600;
            color: #eceef4;
            line-height: 1.35;
            margin: 0.6rem 0 0.3rem 0;
        }

        .yt-sb-info-meta {
            font-size: 0.78rem;
            color: #9a9cab;
            display: flex;
            justify-content: space-between;
            margin-top: 0.3rem;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def _is_valid_youtube_url(url: str) -> bool:
    """Cheap validity check reusing the same ID-extraction logic the
    backend already relies on (loaders/youtube_loader.py), without
    modifying that file."""

    if not url:
        return False

    return extract_video_id(url) is not None


def _reset_everything():
    """
    Reset the application back to its initial state.

    IMPORTANT:
    Never modify the value of a text_input widget after it has been
    created during the current Streamlit run.

    Instead, remove the widget state completely.
    """

    # Remove the text input state safely
    if "yt_url_input" in st.session_state:
        del st.session_state["yt_url_input"]

    # Clear chat
    st.session_state.messages = []

    # Clear RAG objects
    st.session_state.retriever = None
    st.session_state.chain = None

    # Reset processing flags
    st.session_state.processed = False
    st.session_state.pending_process = False
    st.session_state.is_processing = False

    # Reset video info
    st.session_state.video_id = None
    st.session_state.video_metadata = None

    # Reset transcript
    st.session_state.transcript = None
    st.session_state.show_more_transcript = False

def render_sidebar():
    """
    Render the sidebar: logo, URL input, validation, process/reset
    controls.

    Returns:
        (youtube_url: str, process: bool)
    """

    _inject_sidebar_css()

    st.session_state.setdefault("yt_url_input", "")

    if "pending_process" not in st.session_state:
        st.session_state.pending_process = False

    if "is_processing" not in st.session_state:
        st.session_state.is_processing = False

    if "processed" not in st.session_state:
        st.session_state.processed = False

    is_processing = st.session_state.pending_process
    st.session_state.is_processing = is_processing

    process = False

    with st.sidebar:

        # ---- Logo / brand ---- #
        st.markdown(
            """
            <div class="yt-sb-logo">
                <div class="yt-sb-logo-icon">🎬</div>
                <div class="yt-sb-logo-text">
                    <div class="main">YouTube RAG</div>
                    <div class="sub">Chatbot</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="yt-sb-heading">📹 Video Source</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="yt-sb-section">', unsafe_allow_html=True)

        youtube_url = st.text_input(
            "Paste YouTube URL",
            key="yt_url_input",
            placeholder="https://www.youtube.com/watch?v=...",
            disabled=is_processing,
            label_visibility="collapsed",
        )

        st.markdown(
            '<div class="yt-sb-helper">Paste any YouTube video URL.</div>',
            unsafe_allow_html=True,
        )

        if youtube_url and not is_processing:
            st.markdown('<div class="yt-sb-ghost">', unsafe_allow_html=True)
            if st.button("✕ Clear URL", key="clear_url_btn"):

                if "yt_url_input" in st.session_state:
                    del st.session_state["yt_url_input"]

                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        url = youtube_url.strip()
        url_is_valid = _is_valid_youtube_url(url)

        # ---- Ready badge ---- #
        if st.session_state.processed and not is_processing:
            st.markdown(
                '<div class="yt-sb-badge"><span class="dot"></span> Video Ready</div>',
                unsafe_allow_html=True,
            )

        # ---- Primary action: Process Video / disabled spinner state ---- #
        if not st.session_state.processed or is_processing:

            process_clicked = st.button(
                "🔍  Process Video",
                type="primary",
                use_container_width=True,
                disabled=is_processing,
                key="process_video_btn",
            )
            
            if process_clicked:

                if not url:
                    st.warning("⚠️ Please paste a YouTube URL.")
                    st.stop()

                if not url_is_valid:
                    st.error("❌ Please enter a valid YouTube URL.")
                    st.stop()

                st.session_state.pending_process = True
                st.rerun()

            if is_processing:
                with st.spinner("Processing video..."):
                    st.empty()
                st.session_state.pending_process = False
                process = True

            elif process_clicked:
                if url_is_valid:
                    st.session_state.pending_process = True
                    st.rerun()

        # ---- Secondary action: Load New Video (only once processed) ---- #
        if st.session_state.processed and not is_processing:
            if st.button(
                "↻  Load New Video",
                type="secondary",
                use_container_width=True,
                key="load_new_video_btn",
            ):
                _reset_everything()
                st.rerun()

    return url, process


def render_video_info(metadata: dict):
    """
    Render the processed video's info card (thumbnail, title, channel,
    duration, views) and transcript preview in the sidebar.
    """

    with st.sidebar:
        st.markdown("<hr/>", unsafe_allow_html=True)

        st.markdown(
            '<div class="yt-sb-heading">📄 Video Info</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="yt-sb-info-card">', unsafe_allow_html=True)

        st.image(metadata["thumbnail"], use_container_width=True)

        st.markdown(
            f'<div class="yt-sb-info-title">{metadata["title"]}</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="yt-sb-info-meta">'
            f'<span>📺 {metadata["channel"]}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        views_html = (
            f'<span>👁️ {metadata["view_count"]:,} views</span>'
            if metadata.get("view_count")
            else "<span></span>"
        )

        st.markdown(
            f'<div class="yt-sb-info-meta">'
            f'<span>⏱️ {metadata["duration"]}</span>'
            f'{views_html}'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # ---- Transcript Preview ---- #
        transcript = st.session_state.get("transcript")
        if transcript:
            st.markdown("<hr/>", unsafe_allow_html=True)
            st.markdown(
                '<div class="yt-sb-heading">📜 Transcript Preview</div>',
                unsafe_allow_html=True,
            )

            show_more = st.session_state.get("show_more_transcript", False)
            class_name = "show-more" if show_more else "show-less"

            st.markdown(
                f'<div class="yt-transcript-preview {class_name}">'
                f'{html.escape(transcript)}'
                f'</div>',
                unsafe_allow_html=True,
            )

            label = "Show Less" if show_more else "Show More"
            if st.button(label, key="toggle_transcript_view", use_container_width=True):
                st.session_state.show_more_transcript = not show_more
                st.rerun()