"""
Script to add google_id column to users table
Run this to fix Google OAuth authentication
"""
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

def add_google_id_column():
    """Add google_id column to users table if it doesn't exist"""
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'ssc_grievance_system'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', '')
        )
        
        cur = conn.cursor()
        
        # Check if column exists
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' 
            AND column_name = 'google_id'
        """)
        
        if cur.fetchone():
            print("✓ google_id column already exists")
        else:
            print("Adding google_id column to users table...")
            
            # Add the column
            cur.execute("""
                ALTER TABLE users 
                ADD COLUMN google_id VARCHAR(255) UNIQUE
            """)
            
            # Create index
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_users_google_id 
                ON users(google_id)
            """)
            
            conn.commit()
            print("✓ google_id column added successfully!")
            print("✓ Index created on google_id column")
        
        # Verify
        cur.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'users' 
            AND column_name = 'google_id'
        """)
        
        result = cur.fetchone()
        if result:
            print(f"\nColumn details:")
            print(f"  Name: {result[0]}")
            print(f"  Type: {result[1]}")
            print(f"  Nullable: {result[2]}")
        
        cur.close()
        conn.close()
        
        print("\n✓ Database update complete!")
        print("You can now use Google OAuth authentication.")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    add_google_id_column()
