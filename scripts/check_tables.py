"""Check database tables"""

import psycopg2

conn = psycopg2.connect(
    dbname="ssc_grievance_system",
    user="postgres",
    password="J0shu@r0mer0",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

print("Database Tables:")
print("=" * 60)
cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    ORDER BY table_name
""")
for table in cursor.fetchall():
    print(f"  {table[0]}")

cursor.close()
conn.close()
