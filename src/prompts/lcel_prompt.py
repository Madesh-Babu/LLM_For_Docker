from langchain_core.prompts import ChatPromptTemplate

lcel_rag_prompt = ChatPromptTemplate.from_messages([
    ("system", "Use ONLY the provided context to answer the question."),
    ("user", "Question: {question}\n\nContext:\n{context}\n\nAnswer:")
])
