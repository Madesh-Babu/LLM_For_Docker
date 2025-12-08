from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.config import Config
from src.prompts.lcel_prompt import lcel_rag_prompt


def get_retriever():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectorstore = PGVector(
        connection_string=Config.PG_URI,
        collection_name="product_embeddings",
        embedding_function=embeddings
    )

    return vectorstore.as_retriever(search_kwargs={"k": 3})


retriever = get_retriever()
llm = ChatOpenAI(model="gpt-4.1-mini", api_key=Config.OPENAI_API_KEY)


# LCEL PIPELINE
rag_chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough()
    }
    | lcel_rag_prompt
    | llm
    | StrOutputParser()
)


def ask_question(q: str):
    return rag_chain.invoke(q)


if __name__ == "__main__":
    print("Ask a question:")
    question = input("> ")

    answer = ask_question(question)
    print("\nANSWER:\n", answer)
