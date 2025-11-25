"""
Check if all required database columns exist
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config.database import Database

def check_columns():
    """Check if all required columns exist"""
    try:
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        print("\n📋 Checking database columns...")
        
        # Check users table columns
        print("\n1️⃣ Checking users table:")
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'users'
            ORDER BY ordinal_position
        """)
        users_columns = cursor.fetchall()
        for col in users_columns:
            print(f"   ✓ {col['column_name']} ({col['data_type']})")
        
        # Check concerns table columns
        print("\n2️⃣ Checking concerns table:")
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'concerns'
            ORDER BY ordinal_position
        """)
        concerns_columns = cursor.fetchall()
        for col in concerns_columns:
            print(f"   ✓ {col['column_name']} ({col['data_type']})")
        
        # Check if email_verified exists
        email_verified_exists = any(col['column_name'] == 'email_verified' for col in users_columns)
        other_category_exists = any(col['column_name'] == 'other_category' for col in concerns_columns)
        
        print("\n📊 Summary:")
        print(f"   {'✅' if email_verified_exists else '❌'} email_verified in users table")
        print(f"   {'✅' if other_category_exists else '❌'} other_category in concerns table")
        
        cursor.close()
        conn.close()
        
        return email_verified_exists and other_category_exists
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = check_columns()
    sys.exit(0 if success else 1)
