import psycopg2

# Connect to database
conn = psycopg2.connect(
    dbname="ssc_grievance_system",
    user="postgres",
    password="J0shu@r0mer0",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

try:
    # Check for admin accounts
    cursor.execute("""
        SELECT user_id, email, first_name, last_name, role, password_hash
        FROM users 
        WHERE role = 'admin' OR email LIKE '%admin%' OR email LIKE '%ssc%'
        ORDER BY user_id
    """)
    
    results = cursor.fetchall()
    
    if results:
        print("Admin accounts found:")
        print("-" * 80)
        for row in results:
            print(f"ID: {row[0]}")
            print(f"Email: {row[1]}")
            print(f"Name: {row[2]} {row[3]}")
            print(f"Role: {row[4]}")
            print(f"Password Hash: {row[5][:50]}..." if len(row[5]) > 50 else f"Password Hash: {row[5]}")
            print("-" * 80)
    else:
        print("No admin accounts found!")
        
except Exception as e:
    print(f"Error: {e}")
finally:
    cursor.close()
    conn.close()
