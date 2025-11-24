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
    # Get all users with their emails
    cursor.execute("""
        SELECT user_id, email, first_name, last_name, role, sr_code
        FROM users 
        ORDER BY role, user_id
        LIMIT 20
    """)
    
    results = cursor.fetchall()
    
    if results:
        print("USER EMAILS IN DATABASE:")
        print("=" * 100)
        for row in results:
            print(f"ID: {row[0]:3} | Email: {row[1]:40} | Name: {row[2]} {row[3]:15} | Role: {row[4]:8} | SR: {row[5]}")
        print("=" * 100)
        print(f"\nTotal users shown: {len(results)}")
        print("\n📧 IMPORTANT: Users will only receive emails if their email address is correct!")
        print("   Current sending email: 24-31688@g.batstate-u.edu.ph")
        print("   Make sure users have valid @g.batstate-u.edu.ph addresses")
    else:
        print("No users found!")
        
except Exception as e:
    print(f"Error: {e}")
finally:
    cursor.close()
    conn.close()
