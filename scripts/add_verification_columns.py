"""Add email verification columns to users table"""

import psycopg2

conn = psycopg2.connect(
    dbname="ssc_grievance_system",
    user="postgres",
    password="J0shu@r0mer0",
    host="localhost",
    port="5432"
)
conn.autocommit = True
cursor = conn.cursor()

print("=" * 60)
print("ADDING EMAIL VERIFICATION COLUMNS")
print("=" * 60)

try:
    # Add columns
    cursor.execute("""
        ALTER TABLE users 
        ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE,
        ADD COLUMN IF NOT EXISTS verification_code VARCHAR(6),
        ADD COLUMN IF NOT EXISTS verification_code_expires TIMESTAMP,
        ADD COLUMN IF NOT EXISTS verification_token VARCHAR(255)
    """)
    print("✓ Added verification columns")
    
    # Create indexes
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_users_verification_code 
        ON users(verification_code)
    """)
    print("✓ Created verification_code index")
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_users_verification_token 
        ON users(verification_token)
    """)
    print("✓ Created verification_token index")
    
    # Update existing users to verified
    cursor.execute("""
        UPDATE users SET email_verified = TRUE WHERE email_verified IS NULL
    """)
    print("✓ Updated existing users to verified")
    
    print("\n" + "=" * 60)
    print("✓ Email verification columns added successfully!")
    print("=" * 60)
    
except Exception as e:
    print(f"✗ Error: {e}")

cursor.close()
conn.close()
