import streamlit as st


def inject_custom_css():
    """
    Inject custom CSS for the main content area: dark-blue/purple
    premium SaaS theme, glass cards, source-card grid, quick-action
    chips, message actions, and a glowing gradient-border input.

    Every selector here is scoped to `.stApp`, `.main`, and custom
    `.yt-*` classes (or explicitly excludes `section[data-testid="stSidebar"]`).
    Sidebar styling lives entirely in ui/sidebar.py.
    """

    st.markdown(
        """
        <style>

        :root {
            --yt-bg: #050816;
            --yt-accent: #6C63FF;
            --yt-accent-2: #3B82F6;
            --yt-card: rgba(255, 255, 255, 0.06);
            --yt-border: rgba(255, 255, 255, 0.08);
            --yt-radius: 18px;
        }

        .stApp {
            background:
                radial-gradient(circle at 15% -10%, rgba(108, 99, 255, 0.12) 0%, transparent 45%),
                radial-gradient(circle at 90% 0%, rgba(59, 130, 246, 0.10) 0%, transparent 40%),
                var(--yt-bg);
        }

        html, body, [class*="css"] {
            font-family: "Inter", -apple-system, BlinkMacSystemFont,
                "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        section.main > div.block-container {
            max-width: 900px !important;
            padding-top: 1rem !important;
            padding-bottom: 6rem !important;
        }

        /* ---------- Global Whitespace Reductions ---------- */
        div[data-testid="stVerticalBlock"] > div {
            gap: 0.4rem !important;
        }
        
        div[data-testid="stChatMessage"] {
            padding: 0.5rem 0 !important;
            margin: 0 !important;
        }

        /* ---------- Compact sticky header ---------- */
        .yt-compact-header {
            position: sticky !important;
            top: 0 !important;
            z-index: 999 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            gap: 1rem !important;
            padding: 0.8rem 1.2rem !important;
            margin-bottom: 1.2rem !important;
            background: rgba(10, 12, 24, 0.85) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border: 1px solid var(--yt-border) !important;
            border-radius: var(--yt-radius) !important;
        }

        .yt-compact-header .yt-left {
            display: flex !important;
            align-items: center !important;
            gap: 0.7rem !important;
            min-width: 0 !important;
        }

        .yt-compact-header .yt-icon {
            font-size: 1.3rem !important;
            display: flex !important;
            align-items: center !important;
        }

        .yt-compact-header .yt-title {
            font-size: 1.15rem !important;
            font-weight: 700 !important;
            color: #f3f3f8 !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            max-width: 520px !important;
        }

        .yt-compact-header .yt-sub {
            font-size: 0.74rem !important;
            color: #8b8d98 !important;
        }

        .yt-header-badges {
            display: flex !important;
            align-items: center !important;
            gap: 0.6rem !important;
            flex-shrink: 0 !important;
        }

        .yt-badge-pill {
            display: inline-flex !important;
            align-items: center !important;
            gap: 0.35rem !important;
            font-size: 0.74rem !important;
            font-weight: 600 !important;
            padding: 0.32rem 0.7rem !important;
            border-radius: 999px !important;
            white-space: nowrap !important;
        }

        .yt-badge-ready {
            color: #6ee7a8 !important;
            background: rgba(110, 231, 168, 0.1) !important;
            border: 1px solid rgba(110, 231, 168, 0.3) !important;
        }

        .yt-badge-ready .dot {
            width: 6px !important;
            height: 6px !important;
            border-radius: 50% !important;
            background: #6ee7a8 !important;
            box-shadow: 0 0 6px rgba(110, 231, 168, 0.8) !important;
        }

        .yt-badge-model {
            color: #c7c9ff !important;
            background: rgba(108, 99, 255, 0.12) !important;
            border: 1px solid rgba(108, 99, 255, 0.3) !important;
        }

        /* ---------- Hero ---------- */
        .yt-hero {
            text-align: center;
            padding: 3.5rem 1rem 2.2rem 1rem;
        }

        .yt-hero h1 {
            font-size: 2.1rem;
            font-weight: 800;
            background: linear-gradient(135deg, #c8b6ff 0%, #6C63FF 45%, #3B82F6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        }

        .yt-hero p {
            color: #8b8d98;
            font-size: 0.98rem;
        }

        /* ---------- Chat message rows ---------- */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(6px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .yt-msg-row {
            display: flex;
            gap: 0.7rem;
            margin: 0.4rem 0 !important;
            animation: fadeInUp 0.25s ease-out;
        }

        .yt-msg-row.user {
            flex-direction: row-reverse;
        }

        .yt-avatar {
            flex-shrink: 0;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
        }

        .yt-avatar.user {
            background: linear-gradient(135deg, #6C63FF, #3B82F6);
            box-shadow: 0 3px 10px rgba(108, 99, 255, 0.25);
        }

        .yt-avatar.assistant {
            background: linear-gradient(135deg, #1c1e30, #11131f);
            border: 1px solid var(--yt-border);
        }

        .yt-bubble-wrap {
            max-width: 85%;
            display: flex;
            flex-direction: column;
        }

        .yt-msg-row.user .yt-bubble-wrap {
            align-items: flex-end;
        }

        /* User bubble: purple gradient */
        .yt-bubble.user {
            background: linear-gradient(135deg, #6C63FF 0%, #3B82F6 100%);
            color: #fff;
            padding: 0.65rem 1.05rem;
            border-radius: 18px 18px 4px 18px;
            font-size: 0.93rem;
            line-height: 1.5;
            box-shadow: 0 4px 12px rgba(108, 99, 255, 0.2);
        }

        /* Assistant card: large premium glass card */
        .yt-card {
            background: rgba(255, 255, 255, 0.06) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 18px 18px 18px 4px !important;
            padding: 1.3rem 1.6rem !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
        }

        .yt-card:hover {
            border-color: rgba(255, 255, 255, 0.16) !important;
            box-shadow: 0 12px 36px rgba(0, 0, 0, 0.3) !important;
        }

        .yt-card, .yt-card p, .yt-card li {
            color: #e9eaf2 !important;
            font-size: 0.95rem !important;
            line-height: 1.8 !important;
        }

        .yt-card strong {
            color: #c7c2ff !important;
        }

        .yt-card pre {
            background: #0a0b13 !important;
            border-radius: 12px;
            border: 1px solid var(--yt-border);
        }

        .yt-card table {
            border-collapse: collapse;
            width: 100%;
        }

        .yt-card table th, .yt-card table td {
            border: 1px solid rgba(255,255,255,0.1);
            padding: 0.45rem 0.65rem;
            font-size: 0.85rem;
        }

        /* ---------- Metadata Row Badges ---------- */
        .yt-meta-row {
            display: flex !important;
            gap: 0.5rem !important;
            flex-wrap: wrap !important;
            margin: 0.3rem 0.2rem 0.4rem 0.2rem !important;
        }

        .yt-meta-badge {
            display: inline-flex !important;
            align-items: center !important;
            gap: 0.3rem !important;
            font-size: 0.78rem !important;
            font-weight: 600 !important;
            color: #c7c9ff !important;
            background: rgba(108, 99, 255, 0.12) !important;
            border: 1px solid rgba(108, 99, 255, 0.25) !important;
            padding: 0.25rem 0.65rem !important;
            border-radius: 999px !important;
            white-space: nowrap !important;
        }

        /* Typing indicator */
        .yt-typing {
            display: inline-flex;
            gap: 5px;
            padding: 0.7rem 1rem;
            background: var(--yt-card);
            border: 1px solid var(--yt-border);
            border-radius: 16px;
        }

        .yt-typing span {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #6C63FF;
            animation: yt-bounce 1.1s infinite ease-in-out;
        }

        .yt-typing span:nth-child(2) { animation-delay: 0.15s; }
        .yt-typing span:nth-child(3) { animation-delay: 0.3s; }

        @keyframes yt-bounce {
            0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
            30% { transform: translateY(-5px); opacity: 1; }
        }

        /* ---------- Source section ---------- */
        .yt-section-label {
            display: flex !important;
            align-items: center !important;
            font-size: 0.8rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.03em !important;
            text-transform: uppercase !important;
            color: #9a9cab !important;
            margin: 0.8rem 0.2rem 0.4rem 0.2rem !important;
        }

        .yt-source-grid {
            display: grid !important;
            grid-template-columns: repeat(4, 1fr) !important;
            gap: 0.6rem !important;
            margin-bottom: 0.4rem !important;
        }

        @media (max-width: 900px) {
            .yt-source-grid { grid-template-columns: repeat(2, 1fr) !important; }
        }

        @media (max-width: 600px) {
            .yt-source-grid { grid-template-columns: 1fr !important; }
        }

        .yt-source-card {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 14px !important;
            padding: 0.8rem 0.9rem !important;
            height: 110px !important; /* Equal height */
            display: flex !important;
            flex-direction: column !important;
            justify-content: space-between !important;
            transition: border-color 0.18s ease, transform 0.18s ease, box-shadow 0.18s ease !important;
        }

        .yt-source-card:hover {
            border-color: rgba(108, 99, 255, 0.55) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 18px rgba(108, 99, 255, 0.15) !important;
        }

        .yt-source-head {
            display: flex !important;
            justify-content: space-between !important;
            align-items: center !important;
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            color: #d8d9e2 !important;
            margin-bottom: 0.3rem !important;
        }

        .yt-relevance-badge {
            font-size: 0.7rem !important;
            font-weight: 700 !important;
            padding: 0.12rem 0.5rem !important;
            border-radius: 999px !important;
            color: #6ee7a8 !important;
            background: rgba(110, 231, 168, 0.12) !important;
            border: 1px solid rgba(110, 231, 168, 0.3) !important;
        }

        .yt-source-snippet {
            font-size: 0.81rem !important;
            color: #b8b9c6 !important;
            line-height: 1.5 !important;
            display: -webkit-box !important;
            -webkit-line-clamp: 2 !important;
            -webkit-box-orient: vertical !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }

        /* ---------- Quick action chips ---------- */
        section.main .yt-quick-actions {
            margin-top: 0.3rem !important;
        }
        
        section.main .yt-quick-actions button {
            background: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            color: #d8d9e2 !important;
            border-radius: 10px !important;
            font-size: 0.8rem !important;
            padding: 0.4rem 0.5rem !important;
            height: 34px !important;
            transition: all 0.18s ease !important;
        }

        section.main .yt-quick-actions button:hover {
            background: rgba(108, 99, 255, 0.08) !important;
            border-color: rgba(108, 99, 255, 0.55) !important;
            color: #fff !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(108, 99, 255, 0.15) !important;
        }

        /* ---------- Message action icons ---------- */
        section.main .yt-msg-actions button {
            background: transparent !important;
            border: none !important;
            color: #80828f !important;
            font-size: 0.85rem !important;
            padding: 0.2rem 0.45rem !important;
            box-shadow: none !important;
        }

        section.main .yt-msg-actions button:hover {
            color: #fff !important;
        }

        /* ---------- Conversation Divider ---------- */
        .yt-conv-divider {
            height: 1px !important;
            background: rgba(255, 255, 255, 0.06) !important;
            margin: 1.4rem 0 !important;
            width: 100% !important;
        }

        /* ---------- Transcript Preview (Sidebar) ---------- */
        .yt-transcript-preview {
            background: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-radius: 8px !important;
            padding: 8px !important;
            margin-bottom: 6px !important;
            font-family: inherit !important;
        }
        
        .yt-transcript-preview.show-less {
            display: -webkit-box !important;
            -webkit-line-clamp: 5 !important;
            -webkit-box-orient: vertical !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            line-height: 1.55 !important;
            font-size: 0.82rem !important;
            color: #a0a2b0 !important;
        }
        
        .yt-transcript-preview.show-more {
            display: block !important;
            line-height: 1.55 !important;
            font-size: 0.82rem !important;
            color: #a0a2b0 !important;
            max-height: 250px !important;
            overflow-y: auto !important;
        }

        /* ---------- Chat input: premium border ---------- */
        div[data-testid="stChatInput"] {
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 24px !important;
            padding: 0 !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
            transition: all 0.2s ease !important;
        }
        
        div[data-testid="stChatInput"]:focus-within {
            border-color: #6C63FF !important;
            box-shadow: 0 0 15px rgba(108, 99, 255, 0.25) !important;
        }
        
        div[data-testid="stChatInput"] > div {
            background: #0b0d18 !important;
            border-radius: 24px !important;
            border: none !important;
        }
        
        div[data-testid="stChatInput"] textarea {
            background: transparent !important;
            color: #e9eaf2 !important;
            font-size: 0.92rem !important;
            padding: 10px 14px !important;
            line-height: 1.4 !important;
        }
        
        div[data-testid="stChatInput"] button {
            background: transparent !important;
            color: #6C63FF !important;
            border: none !important;
        }
        
        div[data-testid="stChatInput"] button:hover {
            color: #3B82F6 !important;
        }

        /* Disclaimer under the input */
        .yt-disclaimer {
            text-align: center;
            font-size: 0.74rem;
            color: #62636f;
            margin-top: 0.6rem;
        }

        html {
            scroll-behavior: smooth;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )