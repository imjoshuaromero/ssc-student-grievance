# 📚 SSC STUDENT GRIEVANCE SYSTEM - DATABASE DOCUMENTATION (PART 3)

## 6. SQL QUERIES AND RESULTS

### 6.1 Basic Queries

#### 6.1.1 Create Users Table
```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    sr_code VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    program VARCHAR(100),
    year_level INTEGER CHECK (year_level BETWEEN 1 AND 4),
    role VARCHAR(20) NOT NULL DEFAULT 'student' CHECK (role IN ('student', 'admin')),
    google_id VARCHAR(255) UNIQUE,
    email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    verification_code VARCHAR(6),
    verification_code_expires TIMESTAMP,
    verification_token VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

**Expected Result:**
```
CREATE TABLE
```

---

#### 6.1.2 Insert New Student
```sql
INSERT INTO users (sr_code, email, password_hash, first_name, last_name, middle_name, program, year_level, role, email_verified)
VALUES ('21-12345', 'juan.delacruz@g.batstate-u.edu.ph', '$2b$12$hashed_password_here', 
        'Juan', 'Dela Cruz', 'Pablo', 'BSCS', 3, 'student', TRUE)
RETURNING user_id, sr_code, first_name, last_name, email;
```

**Expected Result:**
```
 user_id | sr_code  | first_name | last_name  |              email
---------|----------|------------|------------|------------------------------------
       3 | 21-12345 | Juan       | Dela Cruz  | juan.delacruz@g.batstate-u.edu.ph
(1 row)
```

---

#### 6.1.3 View All Active Concerns
```sql
SELECT concern_id, ticket_number, title, status, priority, created_at
FROM concerns
WHERE status NOT IN ('closed', 'resolved')
ORDER BY priority DESC, created_at DESC;
```

**Expected Result:**
```
 concern_id | ticket_number |              title               |  status   | priority |      created_at
------------|---------------|----------------------------------|-----------|----------|---------------------
          4 | GRV-2025-00004| Inappropriate Comments...        | pending   | urgent   | 2025-11-15 14:30:00
          3 | GRV-2025-00003| Late Release of Study Permits    | in-review | high     | 2025-11-05 09:15:00
          2 | GRV-2025-00002| Incorrect Grade Posted           | in-progress| normal  | 2025-11-10 11:20:00
          5 | GRV-2025-00005| Broken Faucet in CR              | pending   | normal   | 2025-10-20 08:45:00
(4 rows)
```

---

### 6.2 Intermediate Queries with JOINs

#### 6.2.1 Get Concerns with Student and Category Details
```sql
SELECT 
    c.ticket_number,
    c.title,
    u.first_name || ' ' || u.last_name AS student_name,
    u.sr_code,
    u.program,
    cat.category_name,
    c.status,
    c.priority,
    c.created_at
FROM concerns c
INNER JOIN users u ON c.student_id = u.user_id
INNER JOIN concern_categories cat ON c.category_id = cat.category_id
WHERE c.status = 'pending'
ORDER BY c.priority DESC, c.created_at DESC;
```

**Expected Result:**
```
 ticket_number |              title               |  student_name   | sr_code  | program |    category_name      |  status  | priority |      created_at
---------------|----------------------------------|-----------------|----------|---------|----------------------|----------|----------|---------------------
 GRV-2025-00004| Inappropriate Comments...        | Lisa Mendoza    | 23-11111 | BSIT    | Harassment           | pending  | urgent   | 2025-11-15 14:30:00
 GRV-2025-00005| Broken Faucet in CR              | Juan Dela Cruz  | 21-12345 | BSCS    | Services & Facilities| pending  | normal   | 2025-10-20 08:45:00
(2 rows)
```

---

#### 6.2.2 Get Concern with All Comments
```sql
SELECT 
    c.ticket_number,
    c.title,
    c.status,
    com.comment_text,
    u.first_name || ' ' || u.last_name AS commenter,
    u.role,
    com.is_internal,
    com.created_at AS comment_date
FROM concerns c
INNER JOIN comments com ON c.concern_id = com.concern_id
INNER JOIN users u ON com.user_id = u.user_id
WHERE c.ticket_number = 'GRV-2025-00001'
ORDER BY com.created_at ASC;
```

**Expected Result:**
```
 ticket_number |            title              |  status  |                 comment_text                  |  commenter  |  role   | is_internal |     comment_date
---------------|-------------------------------|----------|-----------------------------------------------|-------------|---------|-------------|---------------------
 GRV-2025-00001| Broken Air Conditioning...    | resolved | This is really urgent. Students are...        | Juan Dela... | student | false       | 2025-11-15 10:05:00
 GRV-2025-00001| Broken Air Conditioning...    | resolved | We have assigned this to the facility...      | Admin User  | admin   | false       | 2025-11-16 14:35:00
 GRV-2025-00001| Broken Air Conditioning...    | resolved | Budget approval needed for repair...          | Admin User  | admin   | true        | 2025-11-16 15:00:00
 GRV-2025-00001| Broken Air Conditioning...    | resolved | The AC has been repaired. Technician...       | Admin User  | admin   | false       | 2025-11-20 16:05:00
 GRV-2025-00001| Broken Air Conditioning...    | resolved | Thank you! The AC is working perfectly...     | Juan Dela... | student | false       | 2025-11-20 16:30:00
(5 rows)
```

---

#### 6.2.3 Get Unread Notifications for a User
```sql
SELECT 
    n.notification_id,
    n.notification_type,
    n.title,
    n.message,
    c.ticket_number,
    n.created_at
FROM notifications n
LEFT JOIN concerns c ON n.concern_id = c.concern_id
WHERE n.user_id = 4 AND n.is_read = FALSE
ORDER BY n.created_at DESC;
```

**Expected Result:**
```
 notification_id | notification_type |       title       |                  message                  | ticket_number |      created_at
-----------------|-------------------|-------------------|-------------------------------------------|---------------|---------------------
              6  | status_changed    | Status Updated    | Your concern GRV-2025-00002 status...     | GRV-2025-00002| 2025-11-18 10:30:00
(1 row)
```

---

### 6.3 Advanced Queries

#### 6.3.1 Dashboard Statistics with Multiple Aggregations
```sql
SELECT 
    -- Total counts
    COUNT(*) AS total_concerns,
    COUNT(*) FILTER (WHERE status = 'pending') AS pending_count,
    COUNT(*) FILTER (WHERE status = 'in-review') AS in_review_count,
    COUNT(*) FILTER (WHERE status = 'in-progress') AS in_progress_count,
    COUNT(*) FILTER (WHERE status = 'resolved') AS resolved_count,
    COUNT(*) FILTER (WHERE status = 'closed') AS closed_count,
    
    -- Priority breakdown
    COUNT(*) FILTER (WHERE priority = 'urgent') AS urgent_count,
    COUNT(*) FILTER (WHERE priority = 'high') AS high_count,
    COUNT(*) FILTER (WHERE priority = 'normal') AS normal_count,
    COUNT(*) FILTER (WHERE priority = 'low') AS low_count,
    
    -- Average resolution time
    AVG(EXTRACT(EPOCH FROM (resolved_at - created_at))/86400)::NUMERIC(10,2) AS avg_resolution_days
FROM concerns
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days';
```

**Expected Result:**
```
 total_concerns | pending_count | in_review_count | in_progress_count | resolved_count | closed_count | urgent_count | high_count | normal_count | low_count | avg_resolution_days
----------------|---------------|-----------------|-------------------|----------------|--------------|--------------|------------|--------------|-----------|--------------------
             5  |       2       |        1        |         1         |       1        |      0       |      1       |     2      |      2       |     0     |        5.25
(1 row)
```

---

#### 6.3.2 Top 5 Most Active Students (Most Concerns Filed)
```sql
SELECT 
    u.user_id,
    u.sr_code,
    u.first_name || ' ' || u.last_name AS student_name,
    u.program,
    u.year_level,
    COUNT(c.concern_id) AS total_concerns_filed,
    COUNT(*) FILTER (WHERE c.status = 'resolved') AS resolved_concerns,
    COUNT(*) FILTER (WHERE c.status IN ('pending', 'in-review', 'in-progress')) AS active_concerns,
    MAX(c.created_at) AS last_concern_date
FROM users u
INNER JOIN concerns c ON u.user_id = c.student_id
WHERE u.role = 'student'
GROUP BY u.user_id, u.sr_code, u.first_name, u.last_name, u.program, u.year_level
ORDER BY total_concerns_filed DESC, resolved_concerns DESC
LIMIT 5;
```

**Expected Result:**
```
 user_id | sr_code  |   student_name  | program | year_level | total_concerns_filed | resolved_concerns | active_concerns | last_concern_date
---------|----------|-----------------|---------|------------|----------------------|-------------------|-----------------|---------------------
       3 | 21-12345 | Juan Dela Cruz  | BSCS    |     3      |          2           |         1         |        1        | 2025-10-20 08:45:00
       4 | 22-67890 | Ana Reyes       | BSIT    |     2      |          1           |         0         |        1        | 2025-11-10 11:20:00
       5 | 21-54321 | Pedro Garcia    | BSCS    |     3      |          1           |         0         |        1        | 2025-11-05 09:15:00
       6 | 23-11111 | Lisa Mendoza    | BSIT    |     1      |          1           |         0         |        1        | 2025-11-15 14:30:00
(4 rows)
```

---

#### 6.3.3 Monthly Concern Trends (Last 6 Months)
```sql
WITH monthly_stats AS (
    SELECT 
        DATE_TRUNC('month', created_at) AS month,
        COUNT(*) AS concerns_filed,
        COUNT(*) FILTER (WHERE status = 'resolved') AS concerns_resolved,
        COUNT(*) FILTER (WHERE priority IN ('urgent', 'high')) AS high_priority_count,
        AVG(EXTRACT(EPOCH FROM (COALESCE(resolved_at, CURRENT_TIMESTAMP) - created_at))/86400)::NUMERIC(10,2) AS avg_handling_days
    FROM concerns
    WHERE created_at >= CURRENT_DATE - INTERVAL '6 months'
    GROUP BY DATE_TRUNC('month', created_at)
)
SELECT 
    TO_CHAR(month, 'Month YYYY') AS month_year,
    concerns_filed,
    concerns_resolved,
    high_priority_count,
    ROUND((concerns_resolved::NUMERIC / concerns_filed * 100), 2) AS resolution_rate_percent,
    avg_handling_days
FROM monthly_stats
ORDER BY month DESC;
```

**Expected Result:**
```
   month_year   | concerns_filed | concerns_resolved | high_priority_count | resolution_rate_percent | avg_handling_days
----------------|----------------|-------------------|---------------------|------------------------|------------------
 November 2025  |       4        |         1         |          3          |         25.00          |      12.50
 October 2025   |       1        |         0         |          0          |          0.00          |      40.00
(2 rows)
```

---

#### 6.3.4 Office Performance Report
```sql
SELECT 
    o.office_name,
    COUNT(c.concern_id) AS total_assigned,
    COUNT(*) FILTER (WHERE c.status = 'resolved') AS resolved_count,
    COUNT(*) FILTER (WHERE c.status = 'closed') AS closed_count,
    COUNT(*) FILTER (WHERE c.status IN ('pending', 'in-review')) AS pending_review,
    COUNT(*) FILTER (WHERE c.status = 'in-progress') AS in_progress,
    ROUND(AVG(EXTRACT(EPOCH FROM (COALESCE(c.resolved_at, CURRENT_TIMESTAMP) - c.created_at))/86400), 2) AS avg_days_to_resolve,
    ROUND((COUNT(*) FILTER (WHERE c.status IN ('resolved', 'closed'))::NUMERIC / NULLIF(COUNT(c.concern_id), 0) * 100), 2) AS completion_rate_percent
FROM offices o
LEFT JOIN concerns c ON o.office_id = c.assigned_office_id
WHERE o.is_active = TRUE
GROUP BY o.office_id, o.office_name
ORDER BY total_assigned DESC;
```

**Expected Result:**
```
      office_name       | total_assigned | resolved_count | closed_count | pending_review | in_progress | avg_days_to_resolve | completion_rate_percent
------------------------|----------------|----------------|--------------|----------------|-------------|---------------------|------------------------
 Facility Management    |       2        |       1        |      0       |       1        |      0      |        10.00        |         50.00
 Academic Affairs       |       1        |       0        |      0       |       0        |      1      |        20.00        |          0.00
 Registrar              |       1        |       0        |      0       |       1        |      0      |        25.00        |          0.00
 OSAS                   |       1        |       0        |      0       |       1        |      0      |        15.00        |          0.00
 SSC                    |       0        |       0        |      0       |       0        |      0      |        NULL         |         NULL
(5 rows)
```

---

#### 6.3.5 Complete Concern History with Status Timeline
```sql
WITH concern_timeline AS (
    SELECT 
        c.ticket_number,
        c.title,
        u.first_name || ' ' || u.last_name AS student,
        cat.category_name,
        o.office_name,
        csh.new_status,
        csh.remarks,
        csh.created_at AS status_change_date,
        LEAD(csh.created_at) OVER (PARTITION BY c.concern_id ORDER BY csh.created_at) AS next_status_date,
        EXTRACT(EPOCH FROM (
            LEAD(csh.created_at) OVER (PARTITION BY c.concern_id ORDER BY csh.created_at) - csh.created_at
        ))/86400 AS days_in_status
    FROM concerns c
    INNER JOIN users u ON c.student_id = u.user_id
    INNER JOIN concern_categories cat ON c.category_id = cat.category_id
    LEFT JOIN offices o ON c.assigned_office_id = o.office_id
    INNER JOIN concern_status_history csh ON c.concern_id = csh.concern_id
)
SELECT 
    ticket_number,
    title,
    student,
    category_name,
    office_name,
    new_status AS status,
    remarks,
    status_change_date,
    COALESCE(ROUND(days_in_status::NUMERIC, 2), 0) AS days_in_status
FROM concern_timeline
WHERE ticket_number = 'GRV-2025-00001'
ORDER BY status_change_date;
```

**Expected Result:**
```
 ticket_number |           title            |    student      | category_name         |    office_name      |   status    |           remarks            | status_change_date  | days_in_status
---------------|----------------------------|-----------------|----------------------|---------------------|-------------|------------------------------|---------------------|---------------
 GRV-2025-00001| Broken Air Conditioning... | Juan Dela Cruz  | Services & Facilities| Facility Management | pending     | Concern created              | 2025-11-15 10:00:00 |      1.19
 GRV-2025-00001| Broken Air Conditioning... | Juan Dela Cruz  | Services & Facilities| Facility Management | in-review   | Reviewing the issue          | 2025-11-16 14:30:00 |      0.77
 GRV-2025-00001| Broken Air Conditioning... | Juan Dela Cruz  | Services & Facilities| Facility Management | in-progress | Assigned to facilities team  | 2025-11-17 09:00:00 |      3.29
 GRV-2025-00001| Broken Air Conditioning... | Juan Dela Cruz  | Services & Facilities| Facility Management | resolved    | AC unit repaired and tested  | 2025-11-20 16:00:00 |      0.00
(4 rows)
```

---

#### 6.3.6 Student's Personal Dashboard Query
```sql
SELECT 
    c.ticket_number,
    c.title,
    c.status,
    c.priority,
    cat.category_name,
    o.office_name,
    admin.first_name || ' ' || admin.last_name AS assigned_admin,
    c.created_at,
    c.updated_at,
    (SELECT COUNT(*) FROM comments WHERE concern_id = c.concern_id AND is_internal = FALSE) AS comment_count,
    (SELECT COUNT(*) FROM attachments WHERE concern_id = c.concern_id) AS attachment_count,
    CASE 
        WHEN c.status IN ('resolved', 'closed') THEN 
            EXTRACT(EPOCH FROM (c.resolved_at - c.created_at))/86400
        ELSE 
            EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - c.created_at))/86400
    END AS days_elapsed
FROM concerns c
INNER JOIN concern_categories cat ON c.category_id = cat.category_id
LEFT JOIN offices o ON c.assigned_office_id = o.office_id
LEFT JOIN users admin ON c.assigned_admin_id = admin.user_id
WHERE c.student_id = 3
ORDER BY c.created_at DESC;
```

**Expected Result:**
```
 ticket_number |            title             |  status  | priority |    category_name      |    office_name      | assigned_admin |      created_at     |      updated_at     | comment_count | attachment_count | days_elapsed
---------------|------------------------------|----------|----------|----------------------|---------------------|----------------|---------------------|---------------------|---------------|------------------|-------------
 GRV-2025-00005| Broken Faucet in CR          | pending  | normal   | Services & Facilities| Facility Management | NULL           | 2025-10-20 08:45:00 | 2025-10-20 08:45:00 |       0       |        0         |    41.50
 GRV-2025-00001| Broken Air Conditioning...   | resolved | high     | Services & Facilities| Facility Management | Admin User     | 2025-11-15 10:00:00 | 2025-11-20 16:00:00 |       5       |        2         |     5.25
(2 rows)
```

---

### 6.4 Trigger Functions in Action

#### 6.4.1 Ticket Number Auto-Generation Trigger
```sql
-- When inserting a new concern without specifying ticket_number:
INSERT INTO concerns (student_id, category_id, title, description, status, priority)
VALUES (3, 3, 'Test Concern', 'Testing auto ticket generation', 'pending', 'normal')
RETURNING concern_id, ticket_number, created_at;
```

**Expected Result:**
```
 concern_id | ticket_number  |      created_at
------------|----------------|---------------------
          6 | GRV-2025-00006 | 2025-12-01 10:00:00
(1 row)
```

**Trigger Function:**
```sql
CREATE OR REPLACE FUNCTION generate_ticket_number()
RETURNS TRIGGER AS $$
DECLARE
    year_part TEXT;
    max_seq INTEGER;
    seq_number INTEGER;
BEGIN
    IF NEW.ticket_number IS NULL THEN
        year_part := TO_CHAR(NEW.created_at, 'YYYY');
        
        SELECT COALESCE(MAX(CAST(SUBSTRING(ticket_number FROM 'GRV-' || year_part || '-([0-9]+)') AS INTEGER)), 0)
        INTO max_seq
        FROM concerns
        WHERE ticket_number LIKE 'GRV-' || year_part || '-%';
        
        seq_number := max_seq + 1;
        NEW.ticket_number := 'GRV-' || year_part || '-' || LPAD(seq_number::TEXT, 5, '0');
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

---

#### 6.4.2 Updated_at Auto-Update Trigger
```sql
-- When updating a concern:
UPDATE concerns 
SET status = 'in-progress', assigned_admin_id = 1
WHERE ticket_number = 'GRV-2025-00005'
RETURNING ticket_number, status, updated_at;
```

**Expected Result:**
```
 ticket_number  |   status    |      updated_at
----------------|-------------|---------------------
 GRV-2025-00005 | in-progress | 2025-12-01 14:30:00
(1 row)
```

**Trigger Function:**
```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

---

#### 6.4.3 Status Change Logging Trigger
```sql
-- When changing status, history is automatically logged:
UPDATE concerns 
SET status = 'resolved', 
    resolution_notes = 'Issue has been fixed',
    resolved_at = CURRENT_TIMESTAMP,
    resolved_by = 1
WHERE ticket_number = 'GRV-2025-00005';

-- Check the automatically created history entry:
SELECT * FROM concern_status_history 
WHERE concern_id = (SELECT concern_id FROM concerns WHERE ticket_number = 'GRV-2025-00005')
ORDER BY created_at DESC
LIMIT 1;
```

**Expected Result:**
```
 history_id | concern_id | old_status  | new_status | changed_by |        remarks          |      created_at
------------|------------|-------------|------------|------------|-------------------------|---------------------
         10 |          5 | in-progress | resolved   |          1 | Status changed via UI   | 2025-12-01 16:00:00
(1 row)
```

**Trigger Function:**
```sql
CREATE OR REPLACE FUNCTION log_status_change()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status IS DISTINCT FROM NEW.status THEN
        INSERT INTO concern_status_history (concern_id, old_status, new_status, changed_by, remarks)
        VALUES (NEW.concern_id, OLD.status, NEW.status, NEW.assigned_admin_id, 'Status changed via UI');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

---

### 6.5 View Queries

#### 6.5.1 Active Concerns View
```sql
-- View definition
CREATE VIEW vw_active_concerns AS
SELECT 
    c.concern_id,
    c.ticket_number,
    c.title,
    c.status,
    c.priority,
    u.first_name || ' ' || u.last_name AS student_name,
    u.sr_code,
    cat.category_name,
    o.office_name,
    admin.first_name || ' ' || admin.last_name AS assigned_admin,
    c.created_at,
    EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - c.created_at))/86400 AS days_open
FROM concerns c
INNER JOIN users u ON c.student_id = u.user_id
INNER JOIN concern_categories cat ON c.category_id = cat.category_id
LEFT JOIN offices o ON c.assigned_office_id = o.office_id
LEFT JOIN users admin ON c.assigned_admin_id = admin.user_id
WHERE c.status NOT IN ('closed', 'resolved');

-- Query the view
SELECT * FROM vw_active_concerns
ORDER BY priority DESC, days_open DESC;
```

**Expected Result:**
```
 concern_id | ticket_number |              title               |  status   | priority |  student_name   | sr_code  |    category_name      |    office_name      | assigned_admin |      created_at     | days_open
------------|---------------|----------------------------------|-----------|----------|-----------------|----------|----------------------|---------------------|----------------|---------------------|----------
          4 | GRV-2025-00004| Inappropriate Comments...        | pending   | urgent   | Lisa Mendoza    | 23-11111 | Harassment           | OSAS                | NULL           | 2025-11-15 14:30:00 |   16.25
          3 | GRV-2025-00003| Late Release of Study Permits    | in-review | high     | Pedro Garcia    | 21-54321 | Administrative...    | Registrar           | Admin User     | 2025-11-05 09:15:00 |   26.75
          2 | GRV-2025-00002| Incorrect Grade Posted           | in-progress| normal  | Ana Reyes       | 22-67890 | Academic             | Academic Affairs    | Maria Santos   | 2025-11-10 11:20:00 |   21.50
(3 rows)
```

---

#### 6.5.2 Concern Statistics View
```sql
-- View definition
CREATE VIEW vw_concern_stats AS
SELECT 
    cat.category_name,
    COUNT(*) AS total_concerns,
    COUNT(*) FILTER (WHERE c.status = 'pending') AS pending,
    COUNT(*) FILTER (WHERE c.status = 'in-review') AS in_review,
    COUNT(*) FILTER (WHERE c.status = 'in-progress') AS in_progress,
    COUNT(*) FILTER (WHERE c.status = 'resolved') AS resolved,
    COUNT(*) FILTER (WHERE c.status = 'closed') AS closed,
    ROUND(AVG(EXTRACT(EPOCH FROM (COALESCE(c.resolved_at, CURRENT_TIMESTAMP) - c.created_at))/86400), 2) AS avg_days
FROM concerns c
INNER JOIN concern_categories cat ON c.category_id = cat.category_id
GROUP BY cat.category_name;

-- Query the view
SELECT * FROM vw_concern_stats
ORDER BY total_concerns DESC;
```

**Expected Result:**
```
    category_name      | total_concerns | pending | in_review | in_progress | resolved | closed | avg_days
-----------------------|----------------|---------|-----------|-------------|----------|--------|----------
 Services & Facilities |       2        |    1    |     0     |      0      |    1     |   0    |   23.37
 Academic              |       1        |    0    |     0     |      1      |    0     |   0    |   21.50
 Administrative...     |       1        |    0    |     1     |      0      |    0     |   0    |   26.75
 Harassment            |       1        |    1    |     0     |      0      |    0     |   0    |   16.25
(4 rows)
```

---

## 7. SQL SCHEMA & VERSION CONTROL

### 7.1 Database Folder Structure

```
db/
├── schema.sql                      # Complete database schema
├── schema_unf.sql                  # Unnormalized form (educational)
├── schema_1nf.sql                  # First Normal Form
├── schema_2nf.sql                  # Second Normal Form
├── schema_3nf.sql                  # Third Normal Form (current)
├── seed_students.sql               # Sample student data
├── database_schema.md              # Schema documentation
├── normalization_documentation.md  # Normalization process guide
├── database_diagram.txt            # ASCII ERD
├── add_email_verification.sql      # Migration: Email verification
├── add_google_id_column.sql        # Migration: Google OAuth
├── drop_trigger.sql                # Utility: Drop triggers
├── add_google_id.py                # Script: Add Google ID column
├── create_admin.py                 # Script: Create admin user
├── generate_sample_concerns.py     # Script: Generate test data
├── generate_seed_students.py       # Script: Generate student accounts
└── setup_database.ps1              # PowerShell setup script
```

### 7.2 Schema Version History

| Version | Date       | Changes Made                                    | Migration Script                |
|---------|------------|------------------------------------------------|---------------------------------|
| 1.0.0   | 2025-10-01 | Initial schema design (UNF)                    | `schema_unf.sql`                |
| 1.1.0   | 2025-10-05 | Normalized to 1NF                              | `schema_1nf.sql`                |
| 1.2.0   | 2025-10-10 | Normalized to 2NF                              | `schema_2nf.sql`                |
| 1.3.0   | 2025-10-15 | Normalized to 3NF (current production)         | `schema_3nf.sql`, `schema.sql`  |
| 1.4.0   | 2025-10-20 | Added email verification system                | `add_email_verification.sql`    |
| 1.5.0   | 2025-10-25 | Added Google OAuth support                     | `add_google_id_column.sql`      |
| 1.6.0   | 2025-11-01 | Fixed ticket generation trigger                | Manual migration via psql       |
| 1.7.0   | 2025-11-10 | Added `other_category` field to concerns       | `add_other_category_field.py`   |

### 7.3 GitHub Repository

**Repository URL:**
```
https://github.com/imjoshuaromero/ssc-student-grievance
```

**Branch Structure:**
- `main` - Production-ready code
- `josh-updates` - Active development branch
- `feature/*` - Feature branches
- `hotfix/*` - Emergency fixes

**Key Files:**
- 📁 `/db/` - All database schema and migration files
- 📁 `/backend/` - Flask API implementation
- 📁 `/frontend/` - HTML/CSS/JS templates
- 📁 `/docs/` - Project documentation
- 📄 `README.md` - Project overview and setup guide
- 📄 `requirements.txt` - Python dependencies
- 📄 `schema.sql` - Latest database schema

### 7.4 Database Migration Strategy

**Manual Migration Steps:**
1. **Backup existing database:**
   ```powershell
   pg_dump -U postgres -d ssc_grievance_db > backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sql
   ```

2. **Apply new migration:**
   ```powershell
   psql -U postgres -d ssc_grievance_db -f db/migration_file.sql
   ```

3. **Verify changes:**
   ```sql
   SELECT * FROM information_schema.columns WHERE table_name = 'concerns';
   ```

4. **Rollback if needed:**
   ```powershell
   psql -U postgres -d ssc_grievance_db -f backup_20251201_143000.sql
   ```

---

## 8. SCREENSHOTS

### 8.1 Entity Relationship Diagram

![Database ERD](../db/database_diagram.png)
*Figure 1: Complete Entity Relationship Diagram showing all 8 tables and their relationships*

**Note:** The actual ERD diagram is available in ASCII format in `/db/database_diagram.txt`. For visual diagram, use tools like:
- **pgAdmin 4** - Built-in ERD tool
- **DBeaver** - Free database tool with ERD visualization
- **dbdiagram.io** - Online ERD designer
- **draw.io** - Free diagramming tool

---

### 8.2 Database Table View (pgAdmin)

```
Screenshot would show:
- PostgreSQL database "ssc_grievance_db"
- List of 8 tables in left sidebar
- Selected table showing columns, data types, constraints
- Sample data displayed in grid view
```

**Recommended Screenshot Content:**
- Database connection panel
- Schema browser showing all tables
- `concerns` table structure
- Sample data rows

---

### 8.3 SQL Query Execution Results

```
Screenshot would show:
- Query editor with SQL statement
- Execution time and rows affected
- Result grid with formatted data
- Status bar showing query success
```

**Sample Query to Screenshot:**
```sql
SELECT 
    c.ticket_number,
    c.title,
    u.first_name || ' ' || u.last_name AS student,
    cat.category_name,
    c.status,
    c.created_at
FROM concerns c
JOIN users u ON c.student_id = u.user_id
JOIN concern_categories cat ON c.category_id = cat.category_id
ORDER BY c.created_at DESC
LIMIT 10;
```

---

### 8.4 Application Connected to Database

```
Screenshots would show:
- Student Dashboard displaying concerns from database
- Admin Dashboard showing statistics
- Login page with email verification
- Concern submission form with categories from DB
- Concern details page with comments and history
```

**Key Screenshots to Include:**
1. **Student Dashboard** - Shows user's submitted concerns
2. **Admin Dashboard** - Statistics and concern management
3. **Concern Details** - Full concern thread with comments
4. **Database Connection** - Backend logs showing successful DB queries

---

### 8.5 Database Schema in pgAdmin

```
Screenshot showing:
- Tables panel with all 8 tables
- Expanded "concerns" table showing:
  - Columns tab (all fields with types)
  - Constraints tab (PK, FK, CHECK constraints)
  - Indexes tab (all indexes)
  - Triggers tab (3 triggers)
```

---

### 8.6 Trigger Function Code

```
Screenshot showing:
- pgAdmin Functions panel
- generate_ticket_number() function expanded
- Source code view of the trigger
- Function properties (language, return type, volatility)
```

---

## 9. CONCLUSION

### 9.1 Project Summary

The **SSC Student Grievance Reporting and Tracking System** successfully implements a robust, normalized PostgreSQL database that serves as the foundation for an efficient grievance management platform at Batangas State University. This documentation comprehensively covered the complete database architecture, from initial design through normalization to final implementation.

**Key Accomplishments:**

1. **Normalized Database Design (3NF)**
   - Successfully transformed initial unnormalized data structure through First, Second, and Third Normal Forms
   - Eliminated data redundancy and update anomalies
   - Ensured data integrity through proper constraints and relationships
   - Created a scalable foundation supporting future system expansion

2. **Comprehensive Data Model**
   - Designed 8 interconnected tables modeling real-world grievance workflow
   - Implemented proper primary and foreign key relationships
   - Created efficient indexes for query optimization
   - Developed views for commonly accessed data patterns

3. **Automated Business Logic**
   - Implemented 3 trigger functions handling:
     - Automatic ticket number generation (GRV-YYYY-XXXXX format)
     - Timestamp tracking for audit trails
     - Status change history logging
   - Ensured data consistency without application-level intervention

4. **Security and Authentication**
   - Integrated email verification system
   - Support for traditional password-based and Google OAuth authentication
   - Role-based access control (student vs. admin)
   - Password hashing using bcrypt

5. **Full Audit Trail**
   - `concern_status_history` table tracks every status transition
   - Timestamp columns on all tables
   - Change tracking for accountability and transparency
   - Complete visibility into concern lifecycle

### 9.2 Learning Outcomes and Reflections

Throughout this database design project, several critical database management concepts were applied and reinforced:

**Technical Skills Developed:**
- **Normalization Theory**: Practical application of 1NF, 2NF, and 3NF principles to eliminate redundancy
- **SQL Proficiency**: Writing complex queries with JOINs, CTEs, window functions, and aggregations
- **Database Design**: Translating real-world requirements into logical and physical data models
- **PostgreSQL Features**: Leveraging triggers, functions, views, and advanced constraints
- **Data Integrity**: Implementing referential integrity through foreign keys and CASCADE rules
- **Query Optimization**: Using indexes strategically to improve performance

**Problem-Solving Experience:**
- Identifying and resolving ticket generation race conditions
- Designing flexible category system with "Others" support
- Balancing normalized structure with query performance
- Handling anonymous concerns while maintaining data relationships

**Professional Development:**
- Version control practices using GitHub
- Documentation standards for technical projects
- Database migration strategies
- Testing and validation procedures

### 9.3 Database Importance in the System

The database serves as the **central nervous system** of the entire SSC Grievance platform, providing:

1. **Data Persistence**: Reliable storage of all concerns, user accounts, and system interactions
2. **Data Integrity**: Enforcement of business rules at the database level
3. **Concurrent Access**: Support for multiple users accessing and modifying data simultaneously
4. **Historical Record**: Complete audit trail for accountability and analysis
5. **Scalability Foundation**: Structure supports growth from hundreds to thousands of concerns
6. **Reporting Capability**: Rich data model enables comprehensive analytics and reporting
7. **System Integration**: Single source of truth for web application, potential mobile apps, and future integrations

**Impact on Stakeholders:**
- **Students**: Reliable tracking of submitted concerns with full transparency
- **Administrators**: Efficient workflow management with complete history
- **University Administration**: Data-driven insights into campus issues and trends
- **Developers**: Well-documented, maintainable codebase

### 9.4 Future Enhancements

Potential database improvements for future iterations:

1. **Performance Optimization**
   - Add full-text search indexes for concern titles/descriptions
   - Implement database partitioning for historical data
   - Create materialized views for dashboard statistics

2. **Feature Expansion**
   - Multi-file attachment support with cloud storage integration
   - Real-time notifications using database triggers and WebSockets
   - Survey/feedback system for resolved concerns
   - Advanced reporting with time-series analysis

3. **Security Enhancements**
   - Row-level security policies for data isolation
   - Encrypted columns for sensitive information
   - Database activity monitoring and logging

4. **Integration Capabilities**
   - REST API views for mobile applications
   - Data export functionality for external reporting tools
   - Integration with university student information system

### 9.5 Final Thoughts

This database project demonstrates the critical role of proper data modeling in building robust, scalable applications. The systematic approach—from initial requirements gathering through normalization to implementation—ensures a solid foundation that can grow with the organization's needs.

The SSC Grievance database not only meets current functional requirements but also provides flexibility for future enhancements. The comprehensive documentation ensures that future developers can understand, maintain, and extend the system effectively.

**Project Status:** ✅ **Production Ready**

**Database Version:** 1.7.0

**Last Updated:** December 1, 2025

---

## 10. REFERENCES

### 10.1 Database Theory and Design

1. **Codd, E. F.** (1970). *A Relational Model of Data for Large Shared Data Banks*. Communications of the ACM, 13(6), 377-387.
   - Foundational paper on relational database theory and normalization

2. **Date, C. J.** (2019). *Database Design and Relational Theory: Normal Forms and All That Jazz* (2nd ed.). Apress.
   - Comprehensive guide to normalization forms and relational theory

3. **Elmasri, R., & Navathe, S. B.** (2015). *Fundamentals of Database Systems* (7th ed.). Pearson.
   - Textbook covering ER modeling, normalization, and SQL

### 10.2 PostgreSQL Documentation

4. **PostgreSQL Global Development Group** (2024). *PostgreSQL 14 Documentation*.
   - Official documentation: https://www.postgresql.org/docs/14/
   - Chapters referenced:
     - Chapter 5: Data Definition
     - Chapter 9: Functions and Operators
     - Chapter 38: Triggers
     - Chapter 51: System Catalogs

5. **PostgreSQL Tutorial** (2024). *PostgreSQL Triggers*.
   - https://www.postgresqltutorial.com/postgresql-triggers/
   - Guide for implementing database triggers

### 10.3 SQL and Query Optimization

6. **Molinaro, A.** (2020). *SQL Cookbook: Query Solutions and Techniques for All SQL Users* (2nd ed.). O'Reilly Media.
   - Advanced SQL techniques and window functions

7. **Winand, M.** (2012). *SQL Performance Explained*. Markus Winand.
   - Online resource: https://sql-performance-explained.com/
   - Index optimization and query performance

### 10.4 Database Normalization

8. **Kent, W.** (1983). *A Simple Guide to Five Normal Forms in Relational Database Theory*. Communications of the ACM, 26(2), 120-125.
   - Classic paper explaining 1NF through 5NF

9. **GeeksforGeeks** (2024). *Database Normalization - Normal Forms (1NF, 2NF, 3NF, BCNF)*.
   - https://www.geeksforgeeks.org/database-normalization-normal-forms/
   - Tutorial on normalization with examples

### 10.5 Python and Flask Integration

10. **Grinberg, M.** (2018). *Flask Web Development: Developing Web Applications with Python* (2nd ed.). O'Reilly Media.
    - Flask framework patterns and database integration

11. **Psycopg Documentation** (2024). *Psycopg 2.9 Documentation*.
    - https://www.psycopg.org/docs/
    - PostgreSQL adapter for Python

### 10.6 Web Development and Security

12. **OWASP Foundation** (2024). *OWASP Top Ten Web Application Security Risks*.
    - https://owasp.org/www-project-top-ten/
    - Security best practices for web applications

13. **Mozilla Developer Network** (2024). *Web Security*.
    - https://developer.mozilla.org/en-US/docs/Web/Security
    - Authentication and authorization patterns

### 10.7 Version Control and Collaboration

14. **Chacon, S., & Straub, B.** (2014). *Pro Git* (2nd ed.). Apress.
    - Available at: https://git-scm.com/book/en/v2
    - Git fundamentals and workflows

### 10.8 Data Visualization and Diagramming

15. **dbdiagram.io** (2024). *Database Diagram Tool*.
    - https://dbdiagram.io/
    - Online ERD creation tool

16. **Lucidchart** (2024). *Database Design and ER Diagrams*.
    - https://www.lucidchart.com/pages/database-diagram
    - ERD best practices and examples

### 10.9 Academic Resources

17. **Batangas State University** (2024). *BatStateU Student Handbook 2024-2025*.
    - University policies and grievance procedures
    - Source for system requirements

18. **CS 121 Course Materials** (2024). *Database Management Systems*.
    - Lecture notes on normalization, SQL, and database design
    - Laboratory exercises and assignments

### 10.10 Online Learning Resources

19. **W3Schools** (2024). *SQL Tutorial*.
    - https://www.w3schools.com/sql/
    - Quick reference for SQL syntax

20. **SQLZoo** (2024). *SQL Tutorial and Interactive Exercises*.
    - https://sqlzoo.net/
    - Hands-on SQL practice problems

21. **Mode Analytics SQL Tutorial** (2024). *The SQL Tutorial for Data Analysis*.
    - https://mode.com/sql-tutorial/
    - Advanced SQL for analytics

### 10.11 Stack Overflow and Community Resources

22. **Stack Overflow** (2024). Questions tagged `postgresql`, `database-design`, `sql`.
    - https://stackoverflow.com/questions/tagged/postgresql
    - Community solutions for specific implementation challenges

23. **Database Administrators Stack Exchange** (2024).
    - https://dba.stackexchange.com/
    - Expert advice on database architecture

### 10.12 Project-Specific Resources

24. **GitHub Repository** (2024). *SSC Student Grievance System*.
    - https://github.com/imjoshuaromero/ssc-student-grievance
    - Source code, issues, and project wiki

25. **Project Documentation** (2024).
    - `/docs/SETUP_GUIDE.md` - Installation and configuration
    - `/docs/API_DOCS.md` - API endpoint documentation
    - `/db/database_schema.md` - Detailed schema reference
    - `/db/normalization_documentation.md` - Normalization process

---

## APPENDICES

### Appendix A: Complete Database Schema SQL
See: `/db/schema.sql` (348 lines, complete production schema)

### Appendix B: Sample Data Scripts
See: `/db/seed_students.sql`, `/db/generate_sample_concerns.py`

### Appendix C: Migration Scripts
See: `/db/add_email_verification.sql`, `/db/add_google_id_column.sql`

### Appendix D: Testing Scripts
See: `/scripts/check_database_columns.py`, `/scripts/test_reports_data.py`

### Appendix E: API Documentation
See: `/backend/API_DOCS.md` (Complete REST API reference)

---

**📄 END OF DATABASE DOCUMENTATION**

**Project:** SSC Student Grievance Reporting and Tracking System  
**Institution:** Batangas State University - The National Engineering University  
**Course:** CS 121 - Database Management Systems  
**Academic Year:** 2024-2025  
**Submitted by:** Development Team  
**Date Completed:** December 1, 2025  

---

*This comprehensive database documentation covers all aspects of the SSC Grievance System database from conceptual design through implementation. The database successfully supports a full-featured web application serving the BatStateU community.*
