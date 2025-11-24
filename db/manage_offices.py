"""
Manage Offices in the Database
Usage: python manage_offices.py
"""

import psycopg2
from backend.config.database import get_db_connection

def list_offices():
    """List all offices"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT office_id, office_name, description, contact_email, contact_number, is_active
        FROM offices
        ORDER BY office_id
    """)
    
    offices = cursor.fetchall()
    
    print("\n=== Current Offices ===")
    print(f"{'ID':<5} {'Name':<30} {'Email':<30} {'Active':<8}")
    print("-" * 80)
    
    for office in offices:
        office_id, name, desc, email, phone, is_active = office
        status = "✓" if is_active else "✗"
        print(f"{office_id:<5} {name:<30} {email or 'N/A':<30} {status:<8}")
    
    cursor.close()
    conn.close()
    
    print()

def add_office():
    """Add a new office"""
    print("\n=== Add New Office ===")
    office_name = input("Office Name: ").strip()
    description = input("Description: ").strip()
    contact_email = input("Contact Email: ").strip()
    contact_number = input("Contact Number (optional): ").strip()
    
    if not office_name:
        print("❌ Office name is required!")
        return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO offices (office_name, description, contact_email, contact_number)
            VALUES (%s, %s, %s, %s)
            RETURNING office_id
        """, (office_name, description or None, contact_email or None, contact_number or None))
        
        office_id = cursor.fetchone()[0]
        conn.commit()
        
        print(f"✅ Office added successfully! (ID: {office_id})")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error adding office: {e}")
    finally:
        cursor.close()
        conn.close()

def update_office():
    """Update an existing office"""
    list_offices()
    
    office_id = input("\nEnter Office ID to update: ").strip()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if office exists
    cursor.execute("SELECT * FROM offices WHERE office_id = %s", (office_id,))
    office = cursor.fetchone()
    
    if not office:
        print("❌ Office not found!")
        cursor.close()
        conn.close()
        return
    
    print(f"\nCurrent: {office[1]}")
    print("Leave blank to keep current value")
    
    office_name = input("New Office Name: ").strip() or office[1]
    description = input("New Description: ").strip() or office[2]
    contact_email = input("New Contact Email: ").strip() or office[3]
    contact_number = input("New Contact Number: ").strip() or office[4]
    
    try:
        cursor.execute("""
            UPDATE offices
            SET office_name = %s, description = %s, contact_email = %s, contact_number = %s
            WHERE office_id = %s
        """, (office_name, description, contact_email, contact_number, office_id))
        
        conn.commit()
        print("✅ Office updated successfully!")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error updating office: {e}")
    finally:
        cursor.close()
        conn.close()

def deactivate_office():
    """Deactivate an office"""
    list_offices()
    
    office_id = input("\nEnter Office ID to deactivate: ").strip()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE offices
            SET is_active = FALSE
            WHERE office_id = %s
        """, (office_id,))
        
        conn.commit()
        
        if cursor.rowcount > 0:
            print("✅ Office deactivated successfully!")
        else:
            print("❌ Office not found!")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error deactivating office: {e}")
    finally:
        cursor.close()
        conn.close()

def main():
    """Main menu"""
    while True:
        print("\n" + "="*50)
        print("Office Management System")
        print("="*50)
        print("1. List all offices")
        print("2. Add new office")
        print("3. Update office")
        print("4. Deactivate office")
        print("5. Exit")
        print("="*50)
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            list_offices()
        elif choice == '2':
            add_office()
        elif choice == '3':
            update_office()
        elif choice == '4':
            deactivate_office()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == '__main__':
    main()
