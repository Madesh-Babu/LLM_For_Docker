from src.db import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns
    WHERE table_name = 'selfcare_products';
""")

print("\nColumns in selfcare_products:")
for r in cur.fetchall():
    print(r)

conn.close()
