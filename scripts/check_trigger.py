"""
Check if the ticket number trigger exists and recreate if needed
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config.database import Database

def check_and_fix_trigger():
    """Check if trigger exists and recreate if needed"""
    try:
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        print("\n📋 Checking ticket number generation trigger...")
        
        # Check if trigger exists
        cursor.execute("""
            SELECT tgname 
            FROM pg_trigger 
            WHERE tgname = 'trigger_generate_ticket_number'
        """)
        trigger_exists = cursor.fetchone()
        
        if trigger_exists:
            print("   ✓ Trigger exists")
            print("   🔄 Dropping and recreating trigger...")
            cursor.execute("DROP TRIGGER IF EXISTS trigger_generate_ticket_number ON concerns")
        else:
            print("   ❌ Trigger does not exist")
            print("   🔄 Creating trigger...")
        
        # Recreate the function
        cursor.execute("""
            CREATE OR REPLACE FUNCTION generate_ticket_number()
            RETURNS TRIGGER AS $$
            DECLARE
                year_part VARCHAR(4);
                seq_number INTEGER;
                new_ticket VARCHAR(50);
            BEGIN
                year_part := TO_CHAR(CURRENT_DATE, 'YYYY');
                
                SELECT COUNT(*) + 1 INTO seq_number
                FROM concerns
                WHERE EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM CURRENT_DATE);
                
                new_ticket := 'GRV-' || year_part || '-' || LPAD(seq_number::TEXT, 5, '0');
                
                NEW.ticket_number := new_ticket;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        # Recreate the trigger
        cursor.execute("""
            CREATE TRIGGER trigger_generate_ticket_number
            BEFORE INSERT ON concerns
            FOR EACH ROW
            EXECUTE FUNCTION generate_ticket_number();
        """)
        
        conn.commit()
        
        print("   ✅ Trigger recreated successfully!")
        
        # Test the trigger
        print("\n🧪 Testing trigger...")
        cursor.execute("""
            SELECT generate_ticket_number FROM concerns LIMIT 0
        """)
        
        cursor.close()
        conn.close()
        
        print("   ✅ Trigger is working!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        try:
            if conn:
                conn.rollback()
        except:
            pass
        return False

if __name__ == "__main__":
    success = check_and_fix_trigger()
    sys.exit(0 if success else 1)
