# 📚 SSC STUDENT GRIEVANCE SYSTEM - DATABASE DOCUMENTATION (PART 2)

## 4. DATA DICTIONARY

### 4.1 Table: users

**Purpose:** Stores all user accounts (students and administrators)

| Column Name | Data Type | Length | Null | Default | Constraints | Description |
|-------------|-----------|--------|------|---------|-------------|-------------|
| user_id | INTEGER | - | NO | AUTO | PRIMARY KEY | Unique identifier for each user |
| sr_code | VARCHAR | 20 | NO | - | UNIQUE | Student/Staff Registration code (e.g., "21-12345") |
| email | VARCHAR | 255 | NO | - | UNIQUE | User's institutional email address |
| password_hash | VARCHAR | 255 | NO | - | - | Encrypted password using bcrypt |
| first_name | VARCHAR | 100 | NO | - | - | User's first name |
| last_name | VARCHAR | 100 | NO | - | - | User's last name |
| middle_name | VARCHAR | 100 | YES | NULL | - | User's middle name (optional) |
| program | VARCHAR | 100 | YES | NULL | - | Academic program (e.g., "BSCS", "BSIT") |
| year_level | INTEGER | - | YES | NULL | CHECK (1-4) | Year level (1st, 2nd, 3rd, or 4th year) |
| role | VARCHAR | 20 | NO | 'student' | CHECK | User role: 'student' or 'admin' |
| google_id | VARCHAR | 255 | YES | NULL | UNIQUE | Google OAuth identifier for SSO |
| email_verified | BOOLEAN | - | NO | FALSE | - | Whether email has been verified |
| verification_code | VARCHAR | 6 | YES | NULL | - | 6-digit code for email verification |
| verification_code_expires | TIMESTAMP | - | YES | NULL | - | Expiration time for verification code |
| verification_token | VARCHAR | 255 | YES | NULL | - | Token for email verification links |
| is_active | BOOLEAN | - | NO | TRUE | - | Whether account is active |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | - | Account creation timestamp |
| updated_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | AUTO-UPDATE | Last update timestamp |

**Indexes:**
- `idx_users_sr_code` on `sr_code`
- `idx_users_email` on `email`
- `idx_users_role` on `role`
- `idx_users_google_id` on `google_id`
- `idx_users_verification_code` on `verification_code`
- `idx_users_verification_token` on `verification_token`

**Sample Data:**
```sql
-- Admin User
INSERT INTO users VALUES (
    1, '00-00000', 'admin@ssc.batstateu.edu.ph',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg9KW',
    'Admin', 'User', NULL, NULL, NULL, 'admin',
    NULL, TRUE, NULL, NULL, NULL, TRUE,
    '2025-01-01 08:00:00', '2025-01-01 08:00:00'
);

-- Student User
INSERT INTO users VALUES (
    2, '21-12345', 'juan.delacruz@g.batstate-u.edu.ph',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg9KW',
    'Juan', 'Dela Cruz', 'Pablo', 'BSCS', 3, 'student',
    NULL, TRUE, NULL, NULL, NULL, TRUE,
    '2025-01-15 10:30:00', '2025-01-15 10:30:00'
);
```

---

### 4.2 Table: concern_categories

**Purpose:** Defines categories for organizing different types of concerns

| Column Name | Data Type | Length | Null | Default | Constraints | Description |
|-------------|-----------|--------|------|---------|-------------|-------------|
| category_id | INTEGER | - | NO | AUTO | PRIMARY KEY | Unique identifier for each category |
| category_name | VARCHAR | 100 | NO | - | UNIQUE | Name of the category |
| description | TEXT | - | YES | NULL | - | Detailed description of what concerns fit this category |
| is_active | BOOLEAN | - | NO | TRUE | - | Whether category is currently active/available |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | - | Category creation timestamp |

**Sample Data:**
```sql
INSERT INTO concern_categories (category_name, description) VALUES
('Academic', 'Concerns related to classes, grades, curriculum, and academic matters'),
('Administrative Decisions', 'Issues with administrative policies, decisions, and procedures'),
('Services & Facilities', 'Problems with campus facilities, services, and infrastructure'),
('Harassment', 'Harassment, discrimination, or bullying reports'),
('Others', 'Other concerns not covered by the above categories');
```

---

### 4.3 Table: offices

**Purpose:** Stores university offices/departments that handle concerns

| Column Name | Data Type | Length | Null | Default | Constraints | Description |
|-------------|-----------|--------|------|---------|-------------|-------------|
| office_id | INTEGER | - | NO | AUTO | PRIMARY KEY | Unique identifier for each office |
| office_name | VARCHAR | 100 | NO | - | UNIQUE | Official name of the office |
| description | TEXT | - | YES | NULL | - | Description of office responsibilities |
| contact_email | VARCHAR | 255 | YES | NULL | - | Office contact email address |
| contact_number | VARCHAR | 20 | YES | NULL | - | Office contact phone number |
| is_active | BOOLEAN | - | NO | TRUE | - | Whether office is currently active |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | - | Office registration timestamp |

**Sample Data:**
```sql
INSERT INTO offices (office_name, description, contact_email, contact_number) VALUES
('SSC', 'Supreme Student Council', 'ssc@batstateu.edu.ph', '043-XXX-XXXX'),
('Registrar', 'Office of the Registrar', 'registrar@batstateu.edu.ph', '043-XXX-XXXX'),
('OSAS', 'Office of Student Affairs and Services', 'osas@batstateu.edu.ph', '043-XXX-XXXX'),
('Facility Management', 'Campus Facility Management', 'facilities@batstateu.edu.ph', '043-XXX-XXXX'),
('Academic Affairs', 'Office of Academic Affairs', 'academics@batstateu.edu.ph', '043-XXX-XXXX');
```

---

### 4.4 Table: concerns

**Purpose:** Main table storing all grievance reports submitted by students

| Column Name | Data Type | Length | Null | Default | Constraints | Description |
|-------------|-----------|--------|------|---------|-------------|-------------|
| concern_id | INTEGER | - | NO | AUTO | PRIMARY KEY | Unique identifier for each concern |
| ticket_number | VARCHAR | 50 | NO | AUTO | UNIQUE | Auto-generated ticket (e.g., "GRV-2025-00001") |
| student_id | INTEGER | - | NO | - | FK → users | Student who filed the concern |
| category_id | INTEGER | - | NO | - | FK → concern_categories | Category of the concern |
| assigned_office_id | INTEGER | - | YES | NULL | FK → offices | Office assigned to handle concern |
| assigned_admin_id | INTEGER | - | YES | NULL | FK → users | Admin assigned to concern |
| title | VARCHAR | 255 | NO | - | - | Brief title/subject of concern |
| description | TEXT | - | NO | - | - | Detailed description of the concern |
| location | VARCHAR | 255 | YES | NULL | - | Location where incident occurred |
| incident_date | DATE | - | YES | NULL | - | Date when incident happened |
| status | VARCHAR | 50 | NO | 'pending' | CHECK | Current status (pending, in-review, in-progress, resolved, closed, rejected) |
| priority | VARCHAR | 20 | NO | 'normal' | CHECK | Priority level (low, normal, high, urgent) |
| is_anonymous | BOOLEAN | - | NO | FALSE | - | Whether student wants to remain anonymous |
| other_category | VARCHAR | 100 | YES | NULL | - | Custom category if "Others" was selected |
| resolution_notes | TEXT | - | YES | NULL | - | Final resolution details and notes |
| resolved_at | TIMESTAMP | - | YES | NULL | - | Timestamp when concern was resolved |
| resolved_by | INTEGER | - | YES | NULL | FK → users | Admin who resolved the concern |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | - | When concern was submitted |
| updated_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | AUTO-UPDATE | Last update timestamp |

**Indexes:**
- `idx_concerns_student_id` on `student_id`
- `idx_concerns_status` on `status`
- `idx_concerns_category_id` on `category_id`
- `idx_concerns_ticket_number` on `ticket_number`
- `idx_concerns_created_at` on `created_at`

**Sample Data:**
```sql
INSERT INTO concerns VALUES (
    1, 'GRV-2025-00001', 2, 3, 4, 1,
    'Broken Air Conditioning in Room 301',
    'The air conditioning unit in Room 301 has not been working for the past 2 weeks. This is affecting our ability to focus during classes, especially in the afternoon when temperatures are high.',
    'Room 301, Building A', '2025-11-15', 'resolved', 'high', FALSE, NULL,
    'AC unit has been repaired and tested. New filters installed.',
    '2025-11-20 16:00:00', 1,
    '2025-11-15 10:00:00', '2025-11-20 16:00:00'
);
```

---

### 4.5 Table: concern_status_history

**Purpose:** Audit trail of all status changes for complete transparency

| Column Name | Data Type | Length | Null | Default | Constraints | Description |
|-------------|-----------|--------|------|---------|-------------|-------------|
| history_id | INTEGER | - | NO | AUTO | PRIMARY KEY | Unique identifier for each history entry |
| concern_id | INTEGER | - | NO | - | FK → concerns | Concern this history belongs to |
| old_status | VARCHAR | 50 | YES | NULL | - | Previous status (NULL for initial creation) |
| new_status | VARCHAR | 50 | NO | - | - | New status after change |
| changed_by | INTEGER | - | NO | - | FK → users | User who made the status change |
| remarks | TEXT | - | YES | NULL | - | Notes or reason for status change |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | - | When status change occurred |

**Indexes:**
- `idx_history_concern_id` on `concern_id`
- `idx_history_created_at` on `created_at`

**Sample Data:**
```sql
INSERT INTO concern_status_history VALUES
(1, 1, NULL, 'pending', 2, 'Concern created', '2025-11-15 10:00:00'),
(2, 1, 'pending', 'in-review', 1, 'Reviewing the issue', '2025-11-16 14:30:00'),
(3, 1, 'in-review', 'in-progress', 1, 'Assigned to facilities team', '2025-11-17 09:00:00'),
(4, 1, 'in-progress', 'resolved', 1, 'AC unit repaired and tested', '2025-11-20 16:00:00');
```

---

### 4.6 Table: comments

**Purpose:** Communication thread between students and administrators

| Column Name | Data Type | Length | Null | Default | Constraints | Description |
|-------------|-----------|--------|------|---------|-------------|-------------|
| comment_id | INTEGER | - | NO | AUTO | PRIMARY KEY | Unique identifier for each comment |
| concern_id | INTEGER | - | NO | - | FK → concerns | Concern this comment belongs to |
| user_id | INTEGER | - | NO | - | FK → users | User who wrote the comment |
| comment_text | TEXT | - | NO | - | - | Content of the comment |
| is_internal | BOOLEAN | - | NO | FALSE | - | Internal admin note (not visible to student) |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | - | When comment was posted |
| updated_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | AUTO-UPDATE | Last edit timestamp |

**Indexes:**
- `idx_comments_concern_id` on `concern_id`
- `idx_comments_user_id` on `user_id`
- `idx_comments_created_at` on `created_at`

**Sample Data:**
```sql
INSERT INTO comments VALUES
(1, 1, 2, 'This is really urgent. Students are complaining about the heat.', FALSE, '2025-11-15 10:05:00', '2025-11-15 10:05:00'),
(2, 1, 1, 'We have assigned this to the facility management team.', FALSE, '2025-11-16 14:35:00', '2025-11-16 14:35:00'),
(3, 1, 1, 'Checking budget allocation for repair', TRUE, '2025-11-16 15:00:00', '2025-11-16 15:00:00'),
(4, 1, 1, 'The AC has been repaired. Please let us know if there are any more issues.', FALSE, '2025-11-20 16:05:00', '2025-11-20 16:05:00');
```

---

### 4.7 Table: notifications

**Purpose:** In-app notification system for user alerts

| Column Name | Data Type | Length | Null | Default | Constraints | Description |
|-------------|-----------|--------|------|---------|-------------|-------------|
| notification_id | INTEGER | - | NO | AUTO | PRIMARY KEY | Unique identifier for each notification |
| user_id | INTEGER | - | NO | - | FK → users | User who receives this notification |
| concern_id | INTEGER | - | YES | NULL | FK → concerns | Related concern (if applicable) |
| notification_type | VARCHAR | 50 | NO | - | CHECK | Type: concern_created, status_changed, comment_added, concern_assigned, concern_resolved |
| title | VARCHAR | 255 | NO | - | - | Notification title/subject |
| message | TEXT | - | NO | - | - | Notification message content |
| is_read | BOOLEAN | - | NO | FALSE | - | Whether user has read the notification |
| read_at | TIMESTAMP | - | YES | NULL | - | When notification was marked as read |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | - | When notification was created |

**Indexes:**
- `idx_notifications_user_id` on `user_id`
- `idx_notifications_is_read` on `is_read`
- `idx_notifications_created_at` on `created_at`

**Sample Data:**
```sql
INSERT INTO notifications VALUES
(1, 2, 1, 'concern_created', 'Concern Received', 'Your concern GRV-2025-00001 has been received and is being reviewed.', TRUE, '2025-11-15 10:30:00', '2025-11-15 10:00:01'),
(2, 2, 1, 'status_changed', 'Status Updated', 'Your concern GRV-2025-00001 status has been updated to in-review.', TRUE, '2025-11-16 15:00:00', '2025-11-16 14:30:01'),
(3, 2, 1, 'concern_resolved', 'Concern Resolved', 'Your concern GRV-2025-00001 has been resolved.', FALSE, NULL, '2025-11-20 16:00:01');
```

---

### 4.8 Table: attachments

**Purpose:** Metadata for files uploaded with concerns

| Column Name | Data Type | Length | Null | Default | Constraints | Description |
|-------------|-----------|--------|------|---------|-------------|-------------|
| attachment_id | INTEGER | - | NO | AUTO | PRIMARY KEY | Unique identifier for each attachment |
| concern_id | INTEGER | - | NO | - | FK → concerns | Concern this file is attached to |
| uploaded_by | INTEGER | - | NO | - | FK → users | User who uploaded the file |
| file_name | VARCHAR | 255 | NO | - | - | Original filename |
| file_path | VARCHAR | 500 | NO | - | - | Server storage path |
| file_type | VARCHAR | 50 | YES | NULL | - | MIME type (e.g., "image/jpeg", "application/pdf") |
| file_size | INTEGER | - | YES | NULL | - | File size in bytes |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | - | Upload timestamp |

**Indexes:**
- `idx_attachments_concern_id` on `concern_id`

**Sample Data:**
```sql
INSERT INTO attachments VALUES
(1, 1, 2, 'room_301_broken_ac.jpg', 'uploads/1731650400_room_301_broken_ac.jpg', 'image/jpeg', 245678, '2025-11-15 10:02:00'),
(2, 1, 2, 'temperature_readings.pdf', 'uploads/1731650460_temperature_readings.pdf', 'application/pdf', 123456, '2025-11-15 10:03:00');
```

---

## 5. SAMPLE RECORDS & SQL SCRIPTS

### 5.1 Complete Sample Data Insertion Script

```sql
-- ===========================================
-- Sample Data for SSC Grievance System
-- ===========================================

-- Insert Sample Users
INSERT INTO users (sr_code, email, password_hash, first_name, last_name, middle_name, program, year_level, role, email_verified) VALUES
-- Admin Users
('00-00000', 'admin@ssc.batstateu.edu.ph', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg9KW', 'Admin', 'User', NULL, NULL, NULL, 'admin', TRUE),
('00-00001', 'maria.santos@ssc.batstateu.edu.ph', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg9KW', 'Maria', 'Santos', 'Luna', NULL, NULL, 'admin', TRUE),

-- Student Users
('21-12345', 'juan.delacruz@g.batstate-u.edu.ph', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg9KW', 'Juan', 'Dela Cruz', 'Pablo', 'BSCS', 3, 'student', TRUE),
('22-67890', 'ana.reyes@g.batstate-u.edu.ph', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg9KW', 'Ana', 'Reyes', 'Cruz', 'BSIT', 2, 'student', TRUE),
('21-54321', 'pedro.garcia@g.batstate-u.edu.ph', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg9KW', 'Pedro', 'Garcia', 'Lopez', 'BSCS', 3, 'student', TRUE),
('23-11111', 'lisa.mendoza@g.batstate-u.edu.ph', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg9KW', 'Lisa', 'Mendoza', 'Santos', 'BSIT', 1, 'student', TRUE);

-- Password for all sample users: "password123"

-- Insert Sample Concerns
INSERT INTO concerns (ticket_number, student_id, category_id, title, description, location, incident_date, status, priority, assigned_office_id, assigned_admin_id, is_anonymous) VALUES
('GRV-2025-00001', 3, 3, 'Broken Air Conditioning in Room 301', 'The air conditioning unit in Room 301 has not been working for the past 2 weeks. This is affecting our ability to focus during classes.', 'Room 301, Building A', '2025-11-01', 'resolved', 'high', 4, 1, FALSE),
('GRV-2025-00002', 4, 1, 'Incorrect Grade Posted', 'My final grade for Database Management was posted as 2.5 but according to my computations it should be 1.75.', NULL, '2025-11-10', 'in-progress', 'normal', 5, 2, FALSE),
('GRV-2025-00003', 5, 2, 'Late Release of Study Permits', 'Study permits for graduating students were released 2 weeks late, causing delays in thesis defense scheduling.', 'Registrar Office', '2025-11-05', 'in-review', 'high', 2, 1, FALSE),
('GRV-2025-00004', 6, 4, 'Inappropriate Comments from Instructor', 'An instructor made inappropriate and discriminatory comments during class.', 'Room 205', '2025-11-15', 'pending', 'urgent', 3, NULL, TRUE),
('GRV-2025-00005', 3, 3, 'Broken Faucet in CR', 'The faucet in the 2nd floor CR has been leaking for weeks, wasting water.', '2nd Floor CR, Building B', '2025-10-20', 'pending', 'normal', 4, NULL, FALSE);

-- Insert Status History
INSERT INTO concern_status_history (concern_id, old_status, new_status, changed_by, remarks) VALUES
-- GRV-2025-00001 history
(1, NULL, 'pending', 3, 'Concern created'),
(1, 'pending', 'in-review', 1, 'Reviewing the issue'),
(1, 'in-review', 'in-progress', 1, 'Assigned to facilities team'),
(1, 'in-progress', 'resolved', 1, 'AC unit has been repaired and tested'),

-- GRV-2025-00002 history
(2, NULL, 'pending', 4, 'Concern created'),
(2, 'pending', 'in-review', 2, 'Contacting instructor for verification'),
(2, 'in-review', 'in-progress', 2, 'Rechecking grade computation'),

-- GRV-2025-00003 history
(3, NULL, 'pending', 5, 'Concern created'),
(3, 'pending', 'in-review', 1, 'Investigating the delay'),

-- GRV-2025-00004 history
(4, NULL, 'pending', 6, 'Concern created'),

-- GRV-2025-00005 history
(5, NULL, 'pending', 3, 'Concern created');

-- Insert Comments
INSERT INTO comments (concern_id, user_id, comment_text, is_internal) VALUES
-- Comments for GRV-2025-00001
(1, 3, 'This is really urgent. Students are complaining about the heat during afternoon classes.', FALSE),
(1, 1, 'We have assigned this to the facility management team. They will inspect the unit tomorrow.', FALSE),
(1, 1, 'Budget approval needed for repair - estimated 15,000 PHP', TRUE),
(1, 1, 'The AC has been repaired. Technician installed new compressor. Please let us know if there are any more issues.', FALSE),
(1, 3, 'Thank you! The AC is working perfectly now.', FALSE),

-- Comments for GRV-2025-00002
(2, 4, 'I have attached my grade computation sheet for reference.', FALSE),
(2, 2, 'We are currently verifying with your instructor. This may take 3-5 business days.', FALSE),

-- Comments for GRV-2025-00003
(3, 5, 'This affected our thesis defense schedule. We had to reschedule multiple times.', FALSE),
(3, 1, 'We are investigating what caused the delay. We apologize for the inconvenience.', FALSE);

-- Insert Notifications
INSERT INTO notifications (user_id, concern_id, notification_type, title, message, is_read) VALUES
-- Notifications for user 3 (Juan)
(3, 1, 'concern_created', 'Concern Received', 'Your concern GRV-2025-00001 has been received and is being reviewed.', TRUE),
(3, 1, 'status_changed', 'Status Updated', 'Your concern GRV-2025-00001 status has been updated to in-review.', TRUE),
(3, 1, 'comment_added', 'New Comment', 'Admin User commented on your concern GRV-2025-00001.', TRUE),
(3, 1, 'concern_resolved', 'Concern Resolved', 'Your concern GRV-2025-00001 has been resolved.', TRUE),

-- Notifications for user 4 (Ana)
(4, 2, 'concern_created', 'Concern Received', 'Your concern GRV-2025-00002 has been received and is being reviewed.', TRUE),
(4, 2, 'status_changed', 'Status Updated', 'Your concern GRV-2025-00002 status has been updated to in-progress.', FALSE),

-- Notifications for user 5 (Pedro)
(5, 3, 'concern_created', 'Concern Received', 'Your concern GRV-2025-00003 has been received and is being reviewed.', TRUE),

-- Notifications for user 6 (Lisa)
(6, 4, 'concern_created', 'Concern Received', 'Your concern GRV-2025-00004 has been received and is being reviewed.', FALSE);

-- Insert Attachments
INSERT INTO attachments (concern_id, uploaded_by, file_name, file_path, file_type, file_size) VALUES
(1, 3, 'room_301_broken_ac.jpg', 'uploads/1731650400_room_301_broken_ac.jpg', 'image/jpeg', 245678),
(1, 3, 'temperature_readings.pdf', 'uploads/1731650460_temperature_readings.pdf', 'application/pdf', 123456),
(2, 4, 'grade_computation.pdf', 'uploads/1731823200_grade_computation.pdf', 'application/pdf', 189234),
(3, 5, 'thesis_defense_schedule.pdf', 'uploads/1731736800_thesis_defense_schedule.pdf', 'application/pdf', 156789);
```

### 5.2 Sample Data Location

**📁 Repository Location:**
- Full SQL script: `db/seed_students.sql`
- Generated sample data: `db/generate_sample_concerns.py`
- Student records generator: `db/generate_seed_students.py`

**🔗 GitHub Repository:**
```
https://github.com/imjoshuaromero/ssc-student-grievance/tree/main/db
```

**📄 Files Available:**
- `schema.sql` - Complete database schema with triggers
- `seed_students.sql` - Sample student and admin accounts
- `generate_sample_concerns.py` - Python script to generate realistic concern data
- `generate_seed_students.py` - Python script to generate batch student accounts

---

*Continue to Part 3 for SQL Queries, Version Control, Screenshots, and Conclusion...*
