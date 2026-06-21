from langchain_core.prompts import ChatPromptTemplate

RAG_PROMPT = ChatPromptTemplate.from_template("""
You are an expert assistant.

You MUST answer ONLY using the provided transcript context.

Rules:

- Never invent information.
- If the answer exists, answer naturally.
- If only part of the answer exists, answer with available information.
- Keep answers concise unless the user asks for details.
- Use bullet points whenever appropriate.
- If the answer is missing, reply exactly:

"I couldn't find that information in this YouTube video."

------------------------
Transcript Context:

{context}

------------------------

Question:

{question}

Answer:
""")