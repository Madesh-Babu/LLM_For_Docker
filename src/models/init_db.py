from src.db import get_connection

def init_pgvector():
    conn = get_connection()
    cur = conn.cursor()

    # Install pgvector extension
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # -------------------------
    # 1️⃣ CREATE products table
    # -------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL
        );
    """)

    # Insert sample products (only if table is empty)
    cur.execute("SELECT COUNT(*) FROM products;")
    count = cur.fetchone()[0]

    if count == 0:
        print("Inserting sample products...")
        cur.execute("""
            INSERT INTO products (name, description)
            VALUES
            ('Vitamin C Serum', 'A lightweight serum with vitamin C to brighten dark spots.'),
            ('Aloe Gel', 'Pure aloe vera gel useful for skin hydration and soothing.'),
            ('Hair Growth Oil', 'A blend of natural oils that promote hair growth and reduce hair fall.');
        """)
    else:
        print("Products table already has data. Skipping insert.")

    # ------------------------------------------
    # 2️⃣ CREATE vector store table (embeddings)
    # ------------------------------------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS product_embeddings (
            id SERIAL PRIMARY KEY,
            text TEXT,
            metadata JSONB,
            embedding vector(1536)
        );
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    print("Initializing pgvector and tables...")
    init_pgvector()
    print("Done.")
