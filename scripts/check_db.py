from backend.config.database import Database

# Check tables
tables = Database.execute_query("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;", fetch_all=True)
print("📊 Tables in database:")
if tables:
    for t in tables:
        print(f"  - {t['table_name']}")
else:
    print("  No tables found")

# Check student count
students = Database.execute_query("SELECT COUNT(*) as count FROM users WHERE role = 'student';", fetch_one=True)
print(f"\n👥 Student count: {students['count']}")

# Check if tables exist
print("\n✅ Database structure:")
print(f"  Tables: {'Yes' if tables else 'No'}")
print(f"  Students loaded: {'Yes' if students['count'] > 0 else 'No'}")
