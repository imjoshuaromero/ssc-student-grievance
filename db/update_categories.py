"""
Update concern categories in the database
"""
import sys
import os

# Add parent directory to path to import Database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config.database import Database

def update_categories():
    """Update concern categories with new list"""
    
    # New categories - reordered with Others at the end
    categories = [
        {
            'name': 'Academic / Akademiko',
            'description': 'Concerns related to classes, grades, curriculum, and academic matters'
        },
        {
            'name': 'Administrative Decisions / Desisyong Administratibo',
            'description': 'Issues with administrative policies, decisions, and procedures'
        },
        {
            'name': 'Harrassment / Panghaharas',
            'description': 'Harassment, discrimination, or bullying reports'
        },
        {
            'name': 'Service and Facilities / Serbisyo at Pasilidad',
            'description': 'Problems with campus facilities, services, and infrastructure'
        },
        {
            'name': 'Other:',
            'description': 'Other concerns not covered by the above categories'
        }
    ]
    
    try:
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        # Get current categories count
        cursor.execute("SELECT COUNT(*) as count FROM concern_categories")
        result = cursor.fetchone()
        current_count = result['count'] if isinstance(result, dict) else result[0]
        
        print(f"📊 Current categories: {current_count}")
        print("🔄 Updating categories...")
        
        # First, temporarily rename all categories to avoid conflicts
        cursor.execute("UPDATE concern_categories SET category_name = 'TEMP_' || category_id")
        
        # Update existing categories and insert new ones
        for idx, category in enumerate(categories, start=1):
            # Check if category exists
            cursor.execute("SELECT category_id FROM concern_categories WHERE category_id = %s", (idx,))
            exists = cursor.fetchone()
            
            if exists:
                # Update existing category
                cursor.execute(
                    """
                    UPDATE concern_categories 
                    SET category_name = %s, description = %s
                    WHERE category_id = %s
                    """,
                    (category['name'], category['description'], idx)
                )
                print(f"   ✓ Updated: {category['name']}")
            else:
                # Insert new category
                cursor.execute(
                    """
                    INSERT INTO concern_categories (category_id, category_name, description)
                    VALUES (%s, %s, %s)
                    """,
                    (idx, category['name'], category['description'])
                )
                print(f"   ✓ Added: {category['name']}")
        
        # Delete any extra categories beyond our list
        if current_count > len(categories):
            cursor.execute("DELETE FROM concern_categories WHERE category_id > %s", (len(categories),))
            print(f"   🗑️  Removed {current_count - len(categories)} old categories")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✅ Categories updated successfully!")
        print(f"   Total categories: {len(categories)}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        try:
            if conn:
                conn.rollback()
        except:
            pass

if __name__ == "__main__":
    update_categories()
