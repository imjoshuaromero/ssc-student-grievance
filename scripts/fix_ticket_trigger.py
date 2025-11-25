"""
Fix the ticket number generation trigger to properly find the next available number
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config.database import Database

def fix_trigger():
    """Fix the trigger to properly generate unique ticket numbers"""
    try:
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        print("\n🔧 Fixing ticket number generation trigger...")
        
        # Drop existing trigger
        cursor.execute("DROP TRIGGER IF EXISTS trigger_generate_ticket_number ON concerns")
        
        # Create improved function that finds the max ticket number and increments
        cursor.execute("""
            CREATE OR REPLACE FUNCTION generate_ticket_number()
            RETURNS TRIGGER AS $$
            DECLARE
                year_part VARCHAR(4);
                max_seq INTEGER;
                new_ticket VARCHAR(50);
            BEGIN
                year_part := TO_CHAR(CURRENT_DATE, 'YYYY');
                
                -- Find the maximum sequence number for the current year
                SELECT COALESCE(MAX(
                    CAST(SUBSTRING(ticket_number FROM 'GRV-' || year_part || '-([0-9]+)') AS INTEGER)
                ), 0) INTO max_seq
                FROM concerns
                WHERE ticket_number LIKE 'GRV-' || year_part || '-%';
                
                -- Generate new ticket number with next sequence
                new_ticket := 'GRV-' || year_part || '-' || LPAD((max_seq + 1)::TEXT, 5, '0');
                
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
        
        print("   ✅ Trigger fixed successfully!")
        
        # Show what the next ticket number will be
        cursor.execute("""
            SELECT COALESCE(MAX(
                CAST(SUBSTRING(ticket_number FROM 'GRV-2025-([0-9]+)') AS INTEGER)
            ), 0) + 1 as next_num
            FROM concerns
            WHERE ticket_number LIKE 'GRV-2025-%'
        """)
        result = cursor.fetchone()
        next_num = result['next_num'] if result else 1
        
        print(f"   📋 Next ticket number will be: GRV-2025-{str(next_num).zfill(5)}")
        
        cursor.close()
        conn.close()
        
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
    success = fix_trigger()
    sys.exit(0 if success else 1)
