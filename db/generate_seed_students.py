#!/usr/bin/env python3
"""
Generate SQL INSERT statements for pilot testing students.
Each student's password is their SR-Code (e.g., "24-37958").
"""

import bcrypt
import json

# Load students from JSON
students_data = [
    {"sr":"24-37958","name":"Aguila, Jonalyn R.","email":"24-37958@g.batstate-u.edu.ph"},
    {"sr":"24-34182","name":"Barza, Krista Mourine N.","email":"24-34182@g.batstate-u.edu.ph"},
    {"sr":"24-31558","name":"Bersuto, Karol Fernando II C.","email":"24-31558@g.batstate-u.edu.ph"},
    {"sr":"24-35372","name":"Concha, Marc Gian D.","email":"24-35372@g.batstate-u.edu.ph"},
    {"sr":"24-34231","name":"Cudala, Errol Matthew A.","email":"24-34231@g.batstate-u.edu.ph"},
    {"sr":"24-36106","name":"Dimaano, May Sigrid M.","email":"24-36106@g.batstate-u.edu.ph"},
    {"sr":"24-35146","name":"Dimaculangan, Angelo M.","email":"24-35146@g.batstate-u.edu.ph"},
    {"sr":"24-34530","name":"Dimalaluan, Jerome M.","email":"24-34530@g.batstate-u.edu.ph"},
    {"sr":"24-37874","name":"Dolor, Ricky D.","email":"24-37874@g.batstate-u.edu.ph"},
    {"sr":"24-32211","name":"Garcia, Jimuel M.","email":"24-32211@g.batstate-u.edu.ph"},
    {"sr":"24-31029","name":"Gruta, Marx Charlie Ann C.","email":"24-31029@g.batstate-u.edu.ph"},
    {"sr":"24-33676","name":"Javier, Dave D.","email":"24-33676@g.batstate-u.edu.ph"},
    {"sr":"24-35172","name":"Javier, Sabria Kriselle M.","email":"24-35172@g.batstate-u.edu.ph"},
    {"sr":"24-38864","name":"Liao, Zyrus A.","email":"24-38864@g.batstate-u.edu.ph"},
    {"sr":"24-31292","name":"Marquez, Ron Rafael A.","email":"24-31292@g.batstate-u.edu.ph"},
    {"sr":"24-35579","name":"Matanguihan , Juan Miguel S.","email":"24-35579@g.batstate-u.edu.ph"},
    {"sr":"24-34164","name":"Mendiola , Dianna  V.","email":"24-34164@g.batstate-u.edu.ph"},
    {"sr":"24-35717","name":"Mendoza, John Andrei R.","email":"24-35717@g.batstate-u.edu.ph"},
    {"sr":"24-36245","name":"Mitra, John Ray I.","email":"24-36245@g.batstate-u.edu.ph"},
    {"sr":"24-34799","name":"Morales, Kristian L.","email":"24-34799@g.batstate-u.edu.ph"},
    {"sr":"24-38210","name":"Nebran, Mae Jalen A.","email":"24-38210@g.batstate-u.edu.ph"},
    {"sr":"24-38791","name":"Pactol, John Lloyd B.","email":"24-38791@g.batstate-u.edu.ph"},
    {"sr":"24-34907","name":"Padua, Jaspher D.","email":"24-34907@g.batstate-u.edu.ph"},
    {"sr":"24-38290","name":"Pangilinan, Dean Justin M.","email":"24-38290@g.batstate-u.edu.ph"},
    {"sr":"24-31805","name":"Perez, Jazztin H.","email":"24-31805@g.batstate-u.edu.ph"},
    {"sr":"24-31066","name":"Pernia, Paul Steven G.","email":"24-31066@g.batstate-u.edu.ph"},
    {"sr":"24-31223","name":"Ramirez, Dharil M.","email":"24-31223@g.batstate-u.edu.ph"},
    {"sr":"24-30542","name":"Reyes, Drake Ivanholm M.","email":"24-30542@g.batstate-u.edu.ph"},
    {"sr":"24-31057","name":"Reyes, Eizell Bridgette  I.","email":"24-31057@g.batstate-u.edu.ph"},
    {"sr":"24-37156","name":"Reyes, Ivan Gabriel L.","email":"24-37156@g.batstate-u.edu.ph"},
    {"sr":"24-36287","name":"Robles, Elmar Jerome T.","email":"24-36287@g.batstate-u.edu.ph"},
    {"sr":"24-31688","name":"Romero, Joshua L.","email":"24-31688@g.batstate-u.edu.ph"},
    {"sr":"24-36233","name":"Ruben, Alexa B.","email":"24-36233@g.batstate-u.edu.ph"},
    {"sr":"24-36941","name":"Silva, James Ethan L.","email":"24-36941@g.batstate-u.edu.ph"},
    {"sr":"24-37217","name":"Tuscano, Elisha Claire B.","email":"24-37217@g.batstate-u.edu.ph"},
    {"sr":"24-36251","name":"Ungui, Erica Anne B.","email":"24-36251@g.batstate-u.edu.ph"},
    {"sr":"24-37186","name":"Valencia, Faith A.","email":"24-37186@g.batstate-u.edu.ph"},
    {"sr":"24-37492","name":"Virtucio, Lalaine Anne K.","email":"24-37492@g.batstate-u.edu.ph"},
    {"sr":"24-32184","name":"Zapanta, James Paul D.","email":"24-32184@g.batstate-u.edu.ph"},
    {"sr":"24-34662","name":"Zaraspe, Rexie R.","email":"24-34662@g.batstate-u.edu.ph"}
]

def parse_name(full_name):
    """Parse 'Last, First Middle' format"""
    parts = full_name.split(',')
    last_name = parts[0].strip()
    
    if len(parts) > 1:
        rest = parts[1].strip()
        name_parts = rest.split()
        
        # Get first name (everything except last part which is middle initial)
        if len(name_parts) > 1:
            first_name = ' '.join(name_parts[:-1])
            middle_name = name_parts[-1]
        else:
            first_name = name_parts[0]
            middle_name = None
    else:
        first_name = last_name
        last_name = ''
        middle_name = None
    
    return first_name, last_name, middle_name

def generate_password_hash(password):
    """Generate bcrypt hash for password"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

print("-- ============================================")
print("-- Seed Students for Pilot Testing")
print("-- Default password for all students is their SR-Code")
print("-- Total: 40 students")
print("-- ============================================\n")

print("INSERT INTO users (sr_code, email, password_hash, first_name, last_name, middle_name, program, year_level, role) VALUES")

inserts = []
for student in students_data:
    sr_code = student['sr']
    email = student['email']
    first_name, last_name, middle_name = parse_name(student['name'])
    
    # Generate bcrypt hash where password = SR-Code
    password_hash = generate_password_hash(sr_code)
    
    # Format SQL INSERT
    middle_sql = f"'{middle_name}'" if middle_name else 'NULL'
    
    insert = f"('{sr_code}', '{email}', '{password_hash}', '{first_name}', '{last_name}', {middle_sql}, 'BS Information Technology', 2, 'student')"
    inserts.append(insert)

# Print all inserts
print(',\n'.join(inserts) + ';')

print("\n-- Verification")
print("SELECT COUNT(*) as total_students FROM users WHERE role = 'student';")
print("SELECT sr_code, email, first_name, last_name FROM users WHERE role = 'student' ORDER BY last_name, first_name;")

print("\n-- ============================================")
print("-- Test Login Examples:")
print("-- ============================================")
print("-- Email: 24-31688@g.batstate-u.edu.ph")
print("-- Password: 24-31688")
print("--")
print("-- Email: 24-37958@g.batstate-u.edu.ph") 
print("-- Password: 24-37958")
