"""
Quick check to see current offices in database
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.config.database import Database

conn = Database.get_connection()
cursor = conn.cursor()

cursor.execute("SELECT office_id, office_name, is_active FROM offices ORDER BY office_id")
offices = cursor.fetchall()

print("\n📋 Current Offices in Database:")
print("="*60)
for office in offices:
    status = "✓" if office['is_active'] else "✗"
    print(f"{office['office_id']}. {office['office_name']} [{status}]")
print("="*60)
print(f"Total: {len(offices)} offices\n")

cursor.close()
conn.close()
