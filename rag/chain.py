from langchain_core.output_parsers import StrOutputParser

from prompts.prompt import RAG_PROMPT


def create_chain(llm):

    chain = (
        RAG_PROMPT
        | llm
        | StrOutputParser()
    )

    return chain