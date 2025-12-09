from service.lcel_chain import build_rag_chain

def ask_question(query: str):
    chain = build_rag_chain()
    response = chain.invoke(query)
    print("\nQUESTION:", query)
    print("\nANSWER:\n", response)

if __name__ == "__main__":
    ask_question("Explain about Langchain?")
