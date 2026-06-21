def get_retriever(vectorstore):
    """
    Create retriever from FAISS vector database.
    """

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k":8,
            "fetch_k":20,
            "lambda_mult":0.7
        }
    )

    return retriever