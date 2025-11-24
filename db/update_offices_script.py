"""
Update Offices in Database
Run this script to replace offices with the new list
"""

import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.config.database import Database

def update_offices():
    """Update offices in the database"""
    conn = Database.get_connection()
    cursor = conn.cursor()
    
    try:
        print("🔄 Updating offices in database...")
        
        # Step 1: Remove office assignments from concerns
        print("   Removing office assignments from concerns...")
        cursor.execute("UPDATE concerns SET assigned_office_id = NULL WHERE assigned_office_id IS NOT NULL")
        
        # Step 2: Delete all existing offices
        print("   Deleting old offices...")
        cursor.execute("DELETE FROM offices")
        
        # Step 3: Reset the sequence
        print("   Resetting office ID sequence...")
        cursor.execute("ALTER SEQUENCE offices_office_id_seq RESTART WITH 1")
        
        # Step 4: Insert new offices
        print("   Inserting new offices...")
        new_offices = [
            ('SSC', 'Supreme Student Council', 'ssc@batstateu.edu.ph'),
            ('Registrar', 'Office of the Registrar', 'registrar@batstateu.edu.ph'),
            ('Office of the Student Discipline', 'Office of the Student Discipline', 'discipline@batstateu.edu.ph'),
            ('Scholarship and Financial Assistance Office', 'Scholarship and Financial Assistance Office', 'scholarship@batstateu.edu.ph'),
            ('Office of the Guidance and Counseling', 'Office of the Guidance and Counseling', 'guidance@batstateu.edu.ph'),
            ('Academic Affairs', 'Office of Academic Affairs', 'academics@batstateu.edu.ph'),
            ('General Services Office (GSO)', 'General Services Office', 'gso@batstateu.edu.ph'),
            ('ICT Office', 'Information and Communications Technology Office', 'ict@batstateu.edu.ph')
        ]
        
        for office_name, description, email in new_offices:
            cursor.execute("""
                INSERT INTO offices (office_name, description, contact_email, is_active)
                VALUES (%s, %s, %s, TRUE)
            """, (office_name, description, email))
            print(f"   ✓ Added: {office_name}")
        
        # Commit the changes
        conn.commit()
        
        # Step 5: Verify the changes
        print("\n✅ Offices updated successfully!")
        print("\n📋 Current offices:")
        cursor.execute("SELECT office_id, office_name FROM offices ORDER BY office_id")
        offices = cursor.fetchall()
        
        for office_id, office_name in offices:
            print(f"   {office_id}. {office_name}")
        
        print(f"\n✨ Total offices: {len(offices)}")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error updating offices: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
    
    return True

if __name__ == '__main__':
    print("="*60)
    print("Office Update Script")
    print("="*60)
    print("\nThis will replace all offices with the new list:")
    print("1. SSC")
    print("2. Registrar")
    print("3. Office of the Student Discipline")
    print("4. Scholarship and Financial Assistance Office")
    print("5. Office of the Guidance and Counseling")
    print("6. Academic Affairs")
    print("7. General Services Office (GSO)")
    print("8. ICT Office")
    print("\n" + "="*60)
    
    confirm = input("\nProceed with update? (yes/no): ").strip().lower()
    
    if confirm in ['yes', 'y']:
        success = update_offices()
        if success:
            print("\n✅ Done! The new offices are now available in the system.")
        else:
            print("\n❌ Update failed. Please check the error message above.")
    else:
        print("\n❌ Update cancelled.")
