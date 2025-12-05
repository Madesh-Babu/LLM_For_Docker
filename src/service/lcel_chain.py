from prompts.lcel_prompt import lcel_rag_prompt
from lcel_model import get_lcel_model
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores.pgvector import PGVector
from config import Config
from langchain_openai import OpenAIEmbeddings

def build_rag_chain():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vector_store = PGVector(
        collection_name="product_embeddings",
        connection_string=Config.PG_URI,
        embedding_function=embeddings,
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    model = get_lcel_model()

    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | lcel_rag_prompt
        | model
        | StrOutputParser()
    )

    return chain
