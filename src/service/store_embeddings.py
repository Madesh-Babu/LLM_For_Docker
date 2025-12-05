from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.pgvector import PGVector

from src.service.embeddings import chunk_text
from src.config import Config
from src.db import get_connection
import psycopg2.extras


def fetch_products():
    """
    Fetch product rows from the selfcare_products table.
    Uses DictCursor to allow r["id"] indexing.
    """
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # ✔ Correct table name from your DB: selfcare_products
    cur.execute("SELECT id, name, description FROM products;")

    rows = cur.fetchall()
    conn.close()

    products = [
        {
            "id": r["id"],
            "name": r["name"],
            "description": r["description"],
        }
        for r in rows
    ]

    return products


def store_embeddings(products):
    texts = []
    metadata = []

    for p in products:
        chunks = chunk_text(p["description"])
        for ch in chunks:
            texts.append(ch)
            metadata.append({
                "product_id": p["id"],
                "name": p["name"]
            })

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    PGVector.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadata,
        connection_string=Config.PG_URI,
        collection_name="product_embeddings"
    )

    print(f"Stored {len(texts)} embeddings successfully!")


if __name__ == "__main__":
    print("Fetching products...")
    products = fetch_products()

    if not products:
        print("❌ No products found! Check if table contains data.")
    else:
        print(f"Found {len(products)} products. Generating embeddings...")
        store_embeddings(products)
        print("✔ Done!")
