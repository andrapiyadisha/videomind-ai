from langchain_community.document_loaders import YoutubeLoader


def get_transcript(youtube_url: str):
    loader = YoutubeLoader.from_youtube_url(
        youtube_url,
        add_video_info=True,
    )

    documents = loader.load()

    return documents