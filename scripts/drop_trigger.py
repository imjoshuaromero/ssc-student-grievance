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
    # Drop the trigger
    cursor.execute("DROP TRIGGER IF EXISTS trigger_log_status_change ON concerns;")
    conn.commit()
    print("✓ Trigger dropped successfully!")
    
    # Optionally drop the function
    cursor.execute("DROP FUNCTION IF EXISTS log_status_change();")
    conn.commit()
    print("✓ Function dropped successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()
