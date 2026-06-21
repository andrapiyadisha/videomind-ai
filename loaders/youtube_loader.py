import re

from langchain_core.documents import Document
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
)


def extract_video_id(url: str):
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
    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)

        text = " ".join(chunk.text for chunk in transcript)

        return [
            Document(
                page_content=text,
                metadata={
                    "video_id": video_id,
                },
            )
        ]

    except TranscriptsDisabled:
        raise Exception("This video has subtitles disabled.")

    except NoTranscriptFound:
        raise Exception("No transcript found for this video.")

    except Exception as e:
        raise Exception(f"Failed to load transcript: {str(e)}")