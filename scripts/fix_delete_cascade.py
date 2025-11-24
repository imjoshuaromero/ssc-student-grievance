"""Fix foreign key constraints to allow cascade deletion"""

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
print("FIXING FOREIGN KEY CONSTRAINTS FOR CASCADE DELETE")
print("=" * 60)

# List of foreign key constraints to fix
constraints_to_fix = [
    {
        'table': 'concerns',
        'constraint': 'concerns_student_id_fkey',
        'column': 'student_id',
        'ref_table': 'users',
        'ref_column': 'user_id'
    },
    {
        'table': 'concerns',
        'constraint': 'concerns_assigned_admin_id_fkey',
        'column': 'assigned_admin_id',
        'ref_table': 'users',
        'ref_column': 'user_id'
    },
    {
        'table': 'concerns',
        'constraint': 'concerns_resolved_by_fkey',
        'column': 'resolved_by',
        'ref_table': 'users',
        'ref_column': 'user_id'
    },
    {
        'table': 'concern_status_history',
        'constraint': 'concern_status_history_changed_by_fkey',
        'column': 'changed_by',
        'ref_table': 'users',
        'ref_column': 'user_id'
    },
    {
        'table': 'comments',
        'constraint': 'comments_user_id_fkey',
        'column': 'user_id',
        'ref_table': 'users',
        'ref_column': 'user_id'
    },
    {
        'table': 'notifications',
        'constraint': 'notifications_user_id_fkey',
        'column': 'user_id',
        'ref_table': 'users',
        'ref_column': 'user_id'
    },
    {
        'table': 'attachments',
        'constraint': 'attachments_uploaded_by_fkey',
        'column': 'uploaded_by',
        'ref_table': 'users',
        'ref_column': 'user_id'
    }
]

for constraint in constraints_to_fix:
    try:
        print(f"\nProcessing {constraint['table']}.{constraint['column']}...")
        
        # Drop existing constraint
        drop_sql = f"ALTER TABLE {constraint['table']} DROP CONSTRAINT IF EXISTS {constraint['constraint']}"
        cursor.execute(drop_sql)
        print(f"  ✓ Dropped old constraint: {constraint['constraint']}")
        
        # Add new constraint with CASCADE
        add_sql = f"""
            ALTER TABLE {constraint['table']}
            ADD CONSTRAINT {constraint['constraint']}
            FOREIGN KEY ({constraint['column']})
            REFERENCES {constraint['ref_table']}({constraint['ref_column']})
            ON DELETE CASCADE
        """
        cursor.execute(add_sql)
        print(f"  ✓ Added CASCADE constraint: {constraint['constraint']}")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")

print("\n" + "=" * 60)
print("VERIFICATION - Current Foreign Key Constraints:")
print("=" * 60)

cursor.execute("""
    SELECT 
        tc.table_name, 
        kcu.column_name,
        tc.constraint_name,
        ccu.table_name AS foreign_table_name,
        rc.delete_rule
    FROM information_schema.table_constraints AS tc 
    JOIN information_schema.key_column_usage AS kcu
        ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage AS ccu
        ON ccu.constraint_name = tc.constraint_name
    JOIN information_schema.referential_constraints AS rc
        ON tc.constraint_name = rc.constraint_name
    WHERE tc.constraint_type = 'FOREIGN KEY' 
        AND ccu.table_name = 'users'
    ORDER BY tc.table_name, kcu.column_name
""")

results = cursor.fetchall()
for row in results:
    table, column, constraint, ref_table, delete_rule = row
    status = "✓ CASCADE" if delete_rule == "CASCADE" else "✗ " + delete_rule
    print(f"{table:30} → {column:20} {status}")

print("\n" + "=" * 60)
print("✓ Foreign key constraints updated!")
print("=" * 60)

cursor.close()
conn.close()
