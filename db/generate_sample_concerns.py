"""
Generate sample concerns for testing the grievance system
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config.database import Database
import random
from datetime import datetime, timedelta

# Sample concern data
concern_titles = [
    "Issues with Campus WiFi Connection",
    "Library Opening Hours Concern",
    "Broken Air Conditioning in Room 301",
    "Missing Equipment in Computer Lab",
    "Cafeteria Food Quality Complaint",
    "Parking Space Shortage",
    "Unclear Grading Criteria",
    "Bullying Incident Report",
    "Unfair Treatment by Staff",
    "Facility Maintenance Request",
    "Lost and Found Item",
    "Scholarship Application Issues",
    "Registration System Errors",
    "Cleanliness of Restrooms",
    "Security Concerns in Campus"
]

concern_descriptions = [
    "The WiFi connection in the campus is very slow and keeps disconnecting. This affects my ability to attend online classes and submit assignments on time.",
    "The library closes too early, especially during exam periods when students need more time to study. Can we extend the hours?",
    "The air conditioning unit in Room 301 has been broken for weeks now. It's very hot and uncomfortable during classes.",
    "Several computers in the lab are missing keyboards and mice. This makes it difficult for students to complete their programming assignments.",
    "The food quality in the cafeteria has declined recently. Some students have complained about food safety issues.",
    "There are not enough parking spaces for students. Many of us arrive early but still can't find parking.",
    "The grading criteria for our final project was not clearly explained. Many students are confused about the requirements.",
    "I witnessed a bullying incident between students last week. This needs to be addressed immediately.",
    "Some staff members treat students unfairly and show favoritism. This creates an uncomfortable learning environment.",
    "The facilities need regular maintenance. Many classrooms have broken chairs and damaged whiteboards.",
    "I lost my student ID card on campus last week. Has anyone turned it in to the lost and found?",
    "The scholarship application process is confusing and the requirements are not clearly stated on the website.",
    "The online registration system keeps showing errors when I try to enroll in classes. This is very frustrating.",
    "The restrooms on the third floor are not being cleaned regularly. This is a health and sanitation concern.",
    "There are dark areas on campus at night with insufficient lighting. This poses a security risk for students."
]

def generate_concerns():
    """Generate sample concerns"""
    
    # Get all students
    students_query = "SELECT user_id FROM users WHERE role = 'student' ORDER BY user_id LIMIT 20"
    students = Database.execute_query(students_query, fetch_all=True)
    
    if not students:
        print("❌ No students found in database")
        return
    
    # Get categories and offices
    categories_query = "SELECT category_id FROM concern_categories"
    categories = Database.execute_query(categories_query, fetch_all=True)
    
    offices_query = "SELECT office_id FROM offices"
    offices = Database.execute_query(offices_query, fetch_all=True)
    
    if not categories or not offices:
        print("❌ Categories or offices not found")
        return
    
    print(f"📝 Generating sample concerns...")
    
    statuses = ['pending', 'in-review', 'in-progress', 'resolved', 'closed']
    priorities = ['low', 'normal', 'high', 'urgent']
    
    # Check existing concern count
    count_query = "SELECT COUNT(*) as count FROM concerns"
    count_result = Database.execute_query(count_query, fetch_one=True)
    existing_count = count_result['count'] if count_result else 0
    
    concerns_created = 0
    
    for i in range(len(concern_titles)):
        # Random student
        student = random.choice(students)
        
        # Random category and office
        category = random.choice(categories)
        office = random.choice(offices)
        
        # Random status and priority
        status = random.choice(statuses)
        priority = random.choice(priorities)
        
        # Random date within last 30 days
        days_ago = random.randint(0, 30)
        created_at = datetime.now() - timedelta(days=days_ago)
        
        # Some concerns are anonymous (20% chance)
        is_anonymous = random.random() < 0.2
        
        # Insert concern
        insert_query = """
            INSERT INTO concerns 
            (student_id, category_id, assigned_office_id, title, description, 
             status, priority, is_anonymous, created_at, ticket_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING concern_id
        """
        
        # Generate unique ticket number
        ticket_number = f"SSC-{datetime.now().year}-{existing_count + concerns_created + 1:05d}"
        
        params = (
            student['user_id'],
            category['category_id'],
            office['office_id'],
            concern_titles[i],
            concern_descriptions[i],
            status,
            priority,
            is_anonymous,
            created_at,
            ticket_number
        )
        
        result = Database.execute_query(insert_query, params, fetch_one=True)
        
        if result:
            concerns_created += 1
            print(f"  ✓ Created concern #{result['concern_id']}: {concern_titles[i]} ({status})")
    
    print(f"\n✅ Successfully created {concerns_created} sample concerns!")

if __name__ == "__main__":
    generate_concerns()
