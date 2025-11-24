import psycopg2
import bcrypt

# Connect to database
conn = psycopg2.connect(
    dbname="ssc_grievance_system",
    user="postgres",
    password="J0shu@r0mer0",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

# New password: admin123
new_password = "admin123"
password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

try:
    # Update admin password
    cursor.execute("""
        UPDATE users 
        SET password_hash = %s
        WHERE email = 'admin@ssc.batstateu.edu.ph'
    """, (password_hash,))
    
    conn.commit()
    print("✓ Admin password reset successfully!")
    print(f"  Email: admin@ssc.batstateu.edu.ph")
    print(f"  New Password: {new_password}")
    
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()
