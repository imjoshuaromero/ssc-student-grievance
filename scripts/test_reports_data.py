"""Test script to verify reports data matches database"""

import psycopg2
from datetime import datetime, timedelta

# Database connection
conn = psycopg2.connect(
    dbname="ssc_grievance_system",
    user="postgres",
    password="J0shu@r0mer0",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

print("=" * 60)
print("REPORTS & ANALYTICS DATA VERIFICATION")
print("=" * 60)

# Get date range (last 30 days)
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

print(f"\nDate Range: {start_date.date()} to {end_date.date()}")
print("-" * 60)

# 1. Total Concerns in date range
cursor.execute("""
    SELECT COUNT(*) 
    FROM concerns 
    WHERE created_at >= %s AND created_at <= %s
""", (start_date, end_date))
total_concerns = cursor.fetchone()[0]
print(f"1. Total Concerns (last 30 days): {total_concerns}")

# 2. All time total
cursor.execute("SELECT COUNT(*) FROM concerns")
all_time_total = cursor.fetchone()[0]
print(f"   All Time Total: {all_time_total}")

# 3. Resolved Rate
cursor.execute("""
    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN status = 'resolved' THEN 1 ELSE 0 END) as resolved
    FROM concerns 
    WHERE created_at >= %s AND created_at <= %s
""", (start_date, end_date))
result = cursor.fetchone()
if result[0] > 0:
    resolved_rate = (result[1] / result[0]) * 100
else:
    resolved_rate = 0
print(f"2. Resolved Rate: {resolved_rate:.1f}% ({result[1]} of {result[0]})")

# 4. Average Resolution Time
cursor.execute("""
    SELECT 
        AVG(EXTRACT(EPOCH FROM (updated_at - created_at)) / 86400) as avg_days
    FROM concerns 
    WHERE status = 'resolved' 
    AND updated_at IS NOT NULL
    AND created_at >= %s AND created_at <= %s
""", (start_date, end_date))
avg_time = cursor.fetchone()[0]
if avg_time:
    print(f"3. Avg Resolution Time: {round(avg_time)}d")
else:
    print(f"3. Avg Resolution Time: 0d (no resolved concerns)")

# 5. Active Users (unique students with concerns)
cursor.execute("""
    SELECT COUNT(DISTINCT student_id) 
    FROM concerns 
    WHERE created_at >= %s AND created_at <= %s
""", (start_date, end_date))
active_users = cursor.fetchone()[0]
print(f"4. Active Users: {active_users}")

# Breakdown by status
print("\nStatus Breakdown:")
print("-" * 60)
cursor.execute("""
    SELECT status, COUNT(*) 
    FROM concerns 
    WHERE created_at >= %s AND created_at <= %s
    GROUP BY status 
    ORDER BY COUNT(*) DESC
""", (start_date, end_date))
for status, count in cursor.fetchall():
    percentage = (count / total_concerns * 100) if total_concerns > 0 else 0
    print(f"  {status:15} {count:3} ({percentage:.1f}%)")

# Top Categories
print("\nTop 5 Categories:")
print("-" * 60)
cursor.execute("""
    SELECT c.category_name, COUNT(con.concern_id) as count
    FROM concerns con
    JOIN concern_categories c ON con.category_id = c.category_id
    WHERE con.created_at >= %s AND con.created_at <= %s
    GROUP BY c.category_name
    ORDER BY count DESC
    LIMIT 5
""", (start_date, end_date))
for category, count in cursor.fetchall():
    percentage = (count / total_concerns * 100) if total_concerns > 0 else 0
    print(f"  {category:30} {count:3} ({percentage:.1f}%)")

# Recent concerns sample
print("\nRecent Concerns (Last 5):")
print("-" * 60)
cursor.execute("""
    SELECT ticket_number, title, status, created_at 
    FROM concerns 
    ORDER BY created_at DESC 
    LIMIT 5
""")
for ticket, title, status, created in cursor.fetchall():
    print(f"  {ticket} | {title[:40]:40} | {status:12} | {created.strftime('%Y-%m-%d')}")

print("\n" + "=" * 60)

cursor.close()
conn.close()
