"""Add email verification columns to production database"""
import psycopg2
import os

# Production database URL
DATABASE_URL = "postgresql://ssc_grievance_system_user:YMoc4SP86RipFTHVRiNXbj77bToYpzSL@dpg-d4htrvbuibrs73drcln0-a.singapore-postgres.render.com/ssc_grievance_system"

def add_verification_columns():
    """Add email verification columns to users table"""
    try:
        # Connect to database
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print("Adding email verification columns...")
        
        # Add columns
        cur.execute("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE,
            ADD COLUMN IF NOT EXISTS verification_code VARCHAR(10),
            ADD COLUMN IF NOT EXISTS verification_code_expires TIMESTAMP,
            ADD COLUMN IF NOT EXISTS verification_token VARCHAR(100);
        """)
        
        # Create indices
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_verification_code 
            ON users(verification_code);
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_verification_token 
            ON users(verification_token);
        """)
        
        # Update existing users to verified (including admin)
        cur.execute("""
            UPDATE users 
            SET email_verified = TRUE 
            WHERE email_verified IS NULL OR email_verified = FALSE;
        """)
        
        conn.commit()
        print("✅ Email verification columns added successfully!")
        print("✅ Existing users marked as verified")
        
        # Show table structure
        cur.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'users'
            AND column_name LIKE '%verif%'
            ORDER BY ordinal_position;
        """)
        
        print("\nVerification columns:")
        for row in cur.fetchall():
            print(f"  {row[0]}: {row[1]} (nullable: {row[2]}, default: {row[3]})")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    add_verification_columns()
