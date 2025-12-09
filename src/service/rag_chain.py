from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from openai import OpenAIError
from src.config import Config
from src.prompts.lcel_prompt import lcel_rag_prompt


def get_retriever():
    '''
    Create and return a retriever for the RAG pipeline.
    Returns:
        A retriever instance.
    '''
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectorstore = PGVector(
        connection_string=Config.PG_URI,
        collection_name="product_embeddings",
        embedding_function=embeddings,
    )

    return vectorstore.as_retriever(search_kwargs={"k": 3})


def get_llm():
    """Create LLM instance but handle missing API Key."""
    if not Config.OPENAI_API_KEY:
        raise ValueError(
            "OpenAI API Key is missing! Set OPENAI_API_KEY in environment or config file."
        )

    try:
        return ChatOpenAI(
            model="gpt-4.1-mini",
            api_key=Config.OPENAI_API_KEY,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to initialize ChatOpenAI: {e}")


# Initialize retriever
retriever = get_retriever()

# Initialize model safely
try:
    llm = get_llm()
except Exception as e:
    print(e)
    llm = None  # Prevents crash


# LCEL PIPELINE (only build if llm exists)
if llm:
    rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough(),
        }
        | lcel_rag_prompt
        | llm
        | StrOutputParser()
    )
else:
    rag_chain = None


def ask_question(q: str):
    """Execute the RAG pipeline safely."""
    if rag_chain is None:
        return " RAG pipeline not initialized because the API key is missing."

    try:
        return rag_chain.invoke(q)

    except OpenAIError as e:
        return f"OpenAI Error: {str(e)}"

    except Exception as e:
        return f"Unexpected error: {str(e)}"


if __name__ == "__main__":
    print("Ask a question:")
    question = input("> ")

    answer = ask_question(question)
    print("\nANSWER:\n", answer)
