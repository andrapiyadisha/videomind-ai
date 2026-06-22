import re
from pathlib import Path


def parse_vtt(vtt_path: str) -> str:
    """
    Convert a WebVTT subtitle file into clean plain text.

    Removes:
    - WEBVTT header
    - timestamps
    - cue numbers
    - HTML tags
    - duplicate consecutive captions

    Returns:
        Clean transcript string.
    """

    path = Path(vtt_path)

    if not path.exists():
        raise FileNotFoundError(f"Subtitle file not found: {vtt_path}")

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned_lines = []
    previous = ""

    for line in lines:

        line = line.strip()

        # Empty line
        if not line:
            continue

        # WEBVTT header
        if line.startswith("WEBVTT"):
            continue

        # Timestamp
        if "-->" in line:
            continue

        # Cue number
        if line.isdigit():
            continue

        # Remove HTML tags (<c>, <i>, etc.)
        line = re.sub(r"<[^>]+>", "", line)

        # Remove music notes
        line = line.replace("♪", "")

        # Remove duplicate consecutive captions
        if line == previous:
            continue

        previous = line
        cleaned_lines.append(line)

    transcript = " ".join(cleaned_lines)

    # Remove repeated whitespace
    transcript = re.sub(r"\s+", " ", transcript).strip()

    return transcript