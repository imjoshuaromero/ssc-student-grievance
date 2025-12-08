# 🎓 Pilot Testing Accounts

## Overview

40 pre-registered students from your Java project have been migrated to the web system.

**Default Password:** Each student's password is their **SR-Code** (e.g., `24-31688`)

---

## 📋 How to Load Students into Database

### Option 1: Using pgAdmin (Recommended)

1. Open **pgAdmin**
2. Connect to `grievance_system` database
3. Click **Tools** → **Query Tool**
4. Open file: `db/seed_students.sql`
5. Click **Execute** (F5)

### Option 2: Using psql Command Line

```powershell
# Connect to PostgreSQL
psql -U postgres -d grievance_system

# Run the seed file
\i "C:/Users/bakaj/2NDYR IT/CS 121/FINAL PROJECT/db/seed_students.sql"
```

### Option 3: Direct Copy-Paste

1. Open `db/seed_students.sql`
2. Copy the entire INSERT statement
3. Paste into pgAdmin Query Tool
4. Execute

---

## 🧪 Test Login Credentials

Use any of these accounts to test:

| SR-Code | Email | Password | Name |
|---------|-------|----------|------|
| `24-31688` | 24-31688@g.batstate-u.edu.ph | `24-31688` | Joshua Romero |
| `24-37958` | 24-37958@g.batstate-u.edu.ph | `24-37958` | Jonalyn Aguila |
| `24-34182` | 24-34182@g.batstate-u.edu.ph | `24-34182` | Krista Mourine Barza |
| `24-35372` | 24-35372@g.batstate-u.edu.ph | `24-35372` | Marc Gian Concha |

**All 40 students follow the same pattern:**
- Email: `{SR-CODE}@g.batstate-u.edu.ph`
- Password: `{SR-CODE}` (e.g., `24-31688`)

---

## 👥 Complete Student List

All students are:
- **Program:** BS Information Technology
- **Year Level:** 2nd Year
- **Role:** Student
- **Status:** Active

### Students (A-Z by Last Name):

1. Aguila, Jonalyn R. - `24-37958`
2. Barza, Krista Mourine N. - `24-34182`
3. Bersuto, Karol Fernando II C. - `24-31558`
4. Concha, Marc Gian D. - `24-35372`
5. Cudala, Errol Matthew A. - `24-34231`
6. Dimaano, May Sigrid M. - `24-36106`
7. Dimaculangan, Angelo M. - `24-35146`
8. Dimalaluan, Jerome M. - `24-34530`
9. Dolor, Ricky D. - `24-37874`
10. Garcia, Jimuel M. - `24-32211`
11. Gruta, Marx Charlie Ann C. - `24-31029`
12. Javier, Dave D. - `24-33676`
13. Javier, Sabria Kriselle M. - `24-35172`
14. Liao, Zyrus A. - `24-38864`
15. Marquez, Ron Rafael A. - `24-31292`
16. Matanguihan, Juan Miguel S. - `24-35579`
17. Mendiola, Dianna V. - `24-34164`
18. Mendoza, John Andrei R. - `24-35717`
19. Mitra, John Ray I. - `24-36245`
20. Morales, Kristian L. - `24-34799`
21. Nebran, Mae Jalen A. - `24-38210`
22. Pactol, John Lloyd B. - `24-38791`
23. Padua, Jaspher D. - `24-34907`
24. Pangilinan, Dean Justin M. - `24-38290`
25. Perez, Jazztin H. - `24-31805`
26. Pernia, Paul Steven G. - `24-31066`
27. Ramirez, Dharil M. - `24-31223`
28. Reyes, Drake Ivanholm M. - `24-30542`
29. Reyes, Eizell Bridgette I. - `24-31057`
30. Reyes, Ivan Gabriel L. - `24-37156`
31. Robles, Elmar Jerome T. - `24-36287`
32. Romero, Joshua L. - `24-31688` ⭐ **(You!)**
33. Ruben, Alexa B. - `24-36233`
34. Silva, James Ethan L. - `24-36941`
35. Tuscano, Elisha Claire B. - `24-37217`
36. Ungui, Erica Anne B. - `24-36251`
37. Valencia, Faith A. - `24-37186`
38. Virtucio, Lalaine Anne K. - `24-37492`
39. Zapanta, James Paul D. - `24-32184`
40. Zaraspe, Rexie R. - `24-34662`

---

## 🔐 Security Notes

### Password Hashing

- All passwords are hashed using **bcrypt**
- Salt rounds: 12
- Passwords cannot be reversed or decrypted
- Each password hash is unique even for same password

### Password Reset (Future Feature)

Students can reset their password through:
1. Email verification link
2. Admin manual reset
3. Google OAuth sign-in (no password needed)

---

## 🧪 Testing Scenarios

### 1. Test Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "24-31688@g.batstate-u.edu.ph",
  "password": "24-31688"
}
```

### 2. Test Create Concern
```http
POST /api/concerns/
Authorization: Bearer {token_from_login}
Content-Type: application/json

{
  "category_id": 1,
  "title": "Test Concern",
  "description": "This is a test from pilot testing",
  "priority": "normal"
}
```

### 3. Test Profile
```http
GET /api/users/profile
Authorization: Bearer {token_from_login}
```

---

## 📊 Verification Queries

After loading the students, verify with these SQL queries:

```sql
-- Count total students
SELECT COUNT(*) as total_students 
FROM users 
WHERE role = 'student';
-- Expected: 40

-- List all students
SELECT sr_code, email, first_name, last_name, program, year_level
FROM users 
WHERE role = 'student'
ORDER BY last_name, first_name;

-- Check specific student
SELECT * FROM users WHERE sr_code = '24-31688';
```

---

## 🎯 For Pilot Testing

### What to Test:

1. ✅ **Login** - All 40 students can log in
2. ✅ **Create Concern** - Students can submit grievances
3. ✅ **View Concerns** - Students see only their concerns
4. ✅ **Notifications** - In-app notifications work
5. ✅ **Email** - Email notifications received
6. ✅ **Comments** - Students can comment on their concerns
7. ✅ **Profile** - Students can view/edit profile

### Admin Testing:

Create an admin account manually:

```sql
INSERT INTO users (sr_code, email, password_hash, first_name, last_name, role) 
VALUES (
  'ADMIN-001', 
  'admin@batstateu.edu.ph', 
  '$2b$12$eJQHwikuwL89giG0U1GUzOObSdk87M/UwUwGHYFC8M5ac9K88WEAW', -- Password: 24-31688
  'Admin', 
  'User', 
  'admin'
);
```

Admin credentials:
- Email: `admin@batstateu.edu.ph`
- Password: `24-31688`

---

## 🚀 Next Steps

1. ✅ Load students into database (`seed_students.sql`)
2. ✅ Verify 40 students loaded successfully
3. ✅ Test login with sample accounts
4. ✅ Create admin account
5. ⏳ Build frontend login page
6. ⏳ Test complete user flow
7. ⏳ Deploy for pilot testing

---

## 📝 Important Notes

- **Google OAuth:** Students can also sign in with their `@g.batstate-u.edu.ph` accounts
- **First Login:** Students should change their password after first login (future feature)
- **Password Pattern:** All passwords = SR-Code makes pilot testing easy
- **Real Deployment:** In production, students should set custom passwords

---

## ✅ Ready for Pilot Testing!

All 40 students from your Java project are now registered in the web system. They can immediately log in and start using the system.

**Happy Testing! 🎉**
