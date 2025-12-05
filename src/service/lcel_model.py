from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

def get_llm():
    return ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0.9,
        api_key=os.getenv("OPENAI_API_KEY")
    )
