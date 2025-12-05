from src.db import get_connection
from src.service.embeddings import get_embedding

sentences = [
    "This project uses pgvector to store embeddings.",
    "LangChain OpenAIEmbeddings makes vector embedding easy.",
    "PostgreSQL is now ready for semantic search."
]

def store():
    conn = get_connection()
    cur = conn.cursor()

    for sentence in sentences:
        vector = get_embedding(sentence)   # returns a list[float]

        cur.execute(
            """INSERT INTO sentence_embeddings (text, embedding)
               VALUES (%s, %s)""",
            (sentence, vector)
        )

    conn.commit()
    cur.close()
    conn.close()

    print("[SUCCESS] Stored embeddings using OpenAIEmbeddings.")

if __name__ == "__main__":
    store()
