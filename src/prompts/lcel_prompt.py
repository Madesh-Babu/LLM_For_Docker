from langchain_core.prompts import ChatPromptTemplate

def get_ipl_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("user", "Who is the winner in IPL 2024?")
    ])
