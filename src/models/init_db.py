from src.db import get_connection

def run():
    conn = get_connection()
    cur = conn.cursor()

    print("[INFO] Enabling pgvector extension…")
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    print("[INFO] Creating table sentence_embeddings…")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sentence_embeddings (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL,
            embedding VECTOR(1536)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("[SUCCESS] Database initialized.")

if __name__ == "__main__":
    run()