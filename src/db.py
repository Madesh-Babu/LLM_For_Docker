import psycopg2
from src.config import Config

def get_connection():
    return psycopg2.connect(Config.PG_URI)


if __name__ == "__main__":
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT table_schema, table_name 
        FROM information_schema.tables
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema');
    """)
    print("Tables in DB:")
    for r in cur.fetchall():
        print(r)

    conn.close()