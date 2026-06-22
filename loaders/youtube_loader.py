import os
import re
import shutil
import tempfile

import yt_dlp
from langchain_core.documents import Document

from loaders.subtitle_parser import parse_vtt


def extract_video_id(url: str):
    """
    Extract YouTube video ID from different URL formats.
    """

    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"shorts/([a-zA-Z0-9_-]{11})",
        r"embed/([a-zA-Z0-9_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def load_youtube(video_id: str):
    """
    Download subtitles using yt-dlp and return a LangChain Document.
    """

    url = f"https://www.youtube.com/watch?v={video_id}"

    temp_dir = tempfile.mkdtemp()

    try:

        ydl_opts = {
            "quiet": True,
            "skip_download": True,

            # Download subtitles only
            "writesubtitles": True,
            "writeautomaticsub": True,

            # Prefer English
            "subtitleslangs": ["en", "en-US", "en-GB"],

            # Save as .vtt
            "subtitlesformat": "vtt",

            "outtmpl": os.path.join(temp_dir, "%(id)s"),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Find downloaded subtitle
        subtitle_file = None

        for file in os.listdir(temp_dir):
            if file.endswith(".vtt"):
                subtitle_file = os.path.join(temp_dir, file)
                break

        if subtitle_file is None:
            raise Exception(
                "No English subtitles found for this video."
            )

        transcript = parse_vtt(subtitle_file)

        if not transcript.strip():
            raise Exception("Transcript is empty.")

        return [
            Document(
                page_content=transcript,
                metadata={
                    "video_id": video_id,
                    "source": "yt-dlp",
                },
            )
        ]

    except Exception as e:
        raise Exception(f"Failed to load transcript: {str(e)}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)