import streamlit as st


def _format_duration(seconds):
    """
    Convert a duration in seconds into a human-readable H:MM:SS or M:SS string.
    """

    if not seconds:
        return "Unknown"

    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}"

    return f"{minutes}:{seconds:02d}"


@st.cache_data(show_spinner=False, ttl=3600)
def get_video_metadata(video_id: str) -> dict:
    """
    Fetch lightweight metadata for a YouTube video (title, channel,
    duration, thumbnail) without downloading the video itself.

    Uses yt-dlp in "extract info only" mode. Cached per video_id for
    1 hour via @st.cache_data so revisiting the same video doesn't
    re-hit the network.

    Returns a dict with safe fallback values if any field is missing,
    so the UI never has to special-case None.
    """

    # Imported lazily so the rest of the app doesn't pay the import
    # cost of yt_dlp unless metadata is actually requested.
    import yt_dlp

    url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return {
            "title": info.get("title") or "Untitled video",
            "channel": info.get("channel") or info.get("uploader") or "Unknown channel",
            "duration": _format_duration(info.get("duration")),
            "thumbnail": info.get("thumbnail")
            or f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
            "view_count": info.get("view_count"),
        }

    except Exception:
        # Metadata is a "nice to have" — never let a metadata failure
        # block transcript processing. Fall back to safe defaults,
        # including YouTube's predictable thumbnail URL pattern which
        # works without any API call.
        return {
            "title": "Untitled video",
            "channel": "Unknown channel",
            "duration": "Unknown",
            "thumbnail": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
            "view_count": None,
        }