"""
Script to create an admin user
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.config.database import Database
from backend.utils.auth import hash_password

def create_admin():
    """Create an admin user"""
    
    print("\n=== Create Admin User ===\n")
    
    # Get admin details
    email = input("Enter admin email: ").strip()
    if not email:
        print("Email is required!")
        return
    
    password = input("Enter admin password: ").strip()
    if not password:
        print("Password is required!")
        return
    
    first_name = input("Enter first name: ").strip()
    if not first_name:
        print("First name is required!")
        return
    
    last_name = input("Enter last name: ").strip()
    if not last_name:
        print("Last name is required!")
        return
    
    sr_code = input("Enter SR-Code (e.g., 24-00000): ").strip()
    if not sr_code:
        print("SR-Code is required!")
        return
    
    # Check if user already exists
    check_query = "SELECT user_id FROM users WHERE email = %s OR sr_code = %s"
    existing = Database.execute_query(check_query, (email, sr_code), fetch_one=True)
    
    if existing:
        print(f"\n❌ User with this email or SR-Code already exists!")
        return
    
    # Hash password
    password_hash = hash_password(password)
    
    # Create admin user
    insert_query = """
        INSERT INTO users (sr_code, email, password_hash, first_name, last_name, role, is_active)
        VALUES (%s, %s, %s, %s, %s, 'admin', true)
        RETURNING user_id, email, first_name, last_name, role
    """
    
    try:
        result = Database.execute_query(
            insert_query,
            (sr_code, email, password_hash, first_name, last_name),
            fetch_one=True
        )
        
        if result:
            print("\n✅ Admin user created successfully!")
            print(f"\nUser ID: {result['user_id']}")
            print(f"Email: {result['email']}")
            print(f"Name: {result['first_name']} {result['last_name']}")
            print(f"Role: {result['role']}")
            print(f"\nYou can now login with:")
            print(f"  Email: {email}")
            print(f"  Password: {password}")
        else:
            print("\n❌ Failed to create admin user!")
    
    except Exception as e:
        print(f"\n❌ Error creating admin user: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_admin()
