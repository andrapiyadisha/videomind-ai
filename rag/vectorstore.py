from langchain_community.vectorstores import FAISS


def create_vectorstore(chunks, embeddings):
    """
    Create FAISS vector database.
    """

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vectorstore