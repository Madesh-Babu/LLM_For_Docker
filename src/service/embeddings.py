from langchain_openai import OpenAIEmbeddings
from src.config import Config

emb = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=Config.OPENAI_API_KEY
)

def get_embedding(text: str):
    return emb.embed_query(text)
