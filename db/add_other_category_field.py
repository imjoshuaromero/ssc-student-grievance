"""
Add other_category field to concerns table
"""
import sys
import os

# Add parent directory to path to import Database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config.database import Database

def add_other_category_field():
    """Add other_category column to concerns table"""
    
    try:
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        print("📝 Adding other_category field to concerns table...")
        
        # Add the column
        cursor.execute("""
            ALTER TABLE concerns 
            ADD COLUMN IF NOT EXISTS other_category VARCHAR(100)
        """)
        
        # Add comment
        cursor.execute("""
            COMMENT ON COLUMN concerns.other_category 
            IS 'Custom category text when user selects Other category'
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Field added successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        try:
            if conn:
                conn.rollback()
        except:
            pass

if __name__ == "__main__":
    add_other_category_field()
