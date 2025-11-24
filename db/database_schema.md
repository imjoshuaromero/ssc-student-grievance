# Database Schema Design
## Student Grievance Reporting and Tracking System

---

## Tables Overview

1. **users** - Stores student and admin user accounts
2. **concerns** - Main table for all grievance reports
3. **concern_categories** - Categories for concerns (Academic, Harassment, etc.)
4. **concern_status_history** - Tracks all status changes for transparency
5. **comments** - Communication thread between student and admin
6. **notifications** - Stores notification records for users
7. **offices** - Different offices/departments that handle concerns

---

## Detailed Table Structures

### 1. **users**
Stores all user accounts (students and admins)

```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    sr_code VARCHAR(20) UNIQUE NOT NULL,  -- e.g., "21-12345"
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    program VARCHAR(100),  -- e.g., "BSCS", "BSIT"
    year_level INTEGER,  -- 1, 2, 3, 4
    role VARCHAR(20) NOT NULL DEFAULT 'student',  -- 'student' or 'admin'
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
- `idx_users_sr_code` on `sr_code`
- `idx_users_email` on `email`
- `idx_users_role` on `role`

---

### 2. **concern_categories**
Predefined categories for concerns

```sql
CREATE TABLE concern_categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL,  -- 'Academic', 'Administrative', etc.
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Initial Data:**
```sql
INSERT INTO concern_categories (category_name, description) VALUES
('Academic', 'Concerns related to classes, grades, curriculum'),
('Administrative Decisions', 'Issues with administrative policies and decisions'),
('Services & Facilities', 'Problems with campus facilities and services'),
('Harassment', 'Harassment or discrimination reports'),
('Others', 'Other concerns not covered by above categories');
```

---

### 3. **offices**
Different offices that handle concerns

```sql
CREATE TABLE offices (
    office_id SERIAL PRIMARY KEY,
    office_name VARCHAR(100) UNIQUE NOT NULL,  -- 'SSC', 'Registrar', 'OSAS', etc.
    description TEXT,
    contact_email VARCHAR(255),
    contact_number VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Initial Data:**
```sql
INSERT INTO offices (office_name, description, contact_email) VALUES
('SSC', 'Supreme Student Council', 'ssc@batstateu.edu.ph'),
('Registrar', 'Office of the Registrar', 'registrar@batstateu.edu.ph'),
('OSAS', 'Office of Student Affairs and Services', 'osas@batstateu.edu.ph'),
('Facility Management', 'Campus Facility Management', 'facilities@batstateu.edu.ph');
```

---

### 4. **concerns**
Main table for all grievance reports

```sql
CREATE TABLE concerns (
    concern_id SERIAL PRIMARY KEY,
    ticket_number VARCHAR(50) UNIQUE NOT NULL,  -- e.g., "GRV-2025-00001"
    student_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    assigned_office_id INTEGER,
    assigned_admin_id INTEGER,
    
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(255),  -- Where incident occurred
    incident_date DATE,  -- When incident happened
    
    status VARCHAR(50) NOT NULL DEFAULT 'pending',  
    -- 'pending', 'in-review', 'in-progress', 'resolved', 'closed', 'rejected'
    
    priority VARCHAR(20) DEFAULT 'normal',  -- 'low', 'normal', 'high', 'urgent'
    
    is_anonymous BOOLEAN DEFAULT FALSE,
    
    resolution_notes TEXT,
    resolved_at TIMESTAMP,
    resolved_by INTEGER,  -- admin user_id
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES concern_categories(category_id),
    FOREIGN KEY (assigned_office_id) REFERENCES offices(office_id),
    FOREIGN KEY (assigned_admin_id) REFERENCES users(user_id),
    FOREIGN KEY (resolved_by) REFERENCES users(user_id)
);
```

**Indexes:**
- `idx_concerns_student_id` on `student_id`
- `idx_concerns_status` on `status`
- `idx_concerns_category_id` on `category_id`
- `idx_concerns_ticket_number` on `ticket_number`

---

### 5. **concern_status_history**
Tracks all status changes for full transparency and audit trail

```sql
CREATE TABLE concern_status_history (
    history_id SERIAL PRIMARY KEY,
    concern_id INTEGER NOT NULL,
    old_status VARCHAR(50),
    new_status VARCHAR(50) NOT NULL,
    changed_by INTEGER NOT NULL,  -- user_id of who made the change
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (concern_id) REFERENCES concerns(concern_id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users(user_id)
);
```

**Indexes:**
- `idx_history_concern_id` on `concern_id`

---

### 6. **comments**
Communication thread between students and admins

```sql
CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    concern_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    comment_text TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT FALSE,  -- Internal admin notes not visible to student
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (concern_id) REFERENCES concerns(concern_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
```

**Indexes:**
- `idx_comments_concern_id` on `concern_id`
- `idx_comments_user_id` on `user_id`

---

### 7. **notifications**
Stores notification records

```sql
CREATE TABLE notifications (
    notification_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    concern_id INTEGER,
    notification_type VARCHAR(50) NOT NULL,  
    -- 'concern_created', 'status_changed', 'comment_added', 'concern_assigned', 'concern_resolved'
    
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (concern_id) REFERENCES concerns(concern_id) ON DELETE CASCADE
);
```

**Indexes:**
- `idx_notifications_user_id` on `user_id`
- `idx_notifications_is_read` on `is_read`

---

### 8. **attachments** (Optional but Recommended)
Store file attachments for concerns

```sql
CREATE TABLE attachments (
    attachment_id SERIAL PRIMARY KEY,
    concern_id INTEGER NOT NULL,
    uploaded_by INTEGER NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(50),  -- 'image/jpeg', 'application/pdf', etc.
    file_size INTEGER,  -- in bytes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (concern_id) REFERENCES concerns(concern_id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(user_id)
);
```

---

## Entity Relationships

### Relationship Diagram (Text Format)

```
users (1) ----< (M) concerns
    - A user can file multiple concerns
    - Each concern is filed by one user

concern_categories (1) ----< (M) concerns
    - A category can have multiple concerns
    - Each concern belongs to one category

offices (1) ----< (M) concerns
    - An office can handle multiple concerns
    - Each concern can be assigned to one office

users (admin) (1) ----< (M) concerns (assigned_admin_id)
    - An admin can be assigned to multiple concerns
    - Each concern can be assigned to one admin

concerns (1) ----< (M) concern_status_history
    - A concern has multiple status changes tracked
    - Each history entry belongs to one concern

concerns (1) ----< (M) comments
    - A concern can have multiple comments
    - Each comment belongs to one concern

users (1) ----< (M) comments
    - A user can write multiple comments
    - Each comment is written by one user

concerns (1) ----< (M) notifications
    - A concern can generate multiple notifications
    - Each notification can be related to one concern

users (1) ----< (M) notifications
    - A user can receive multiple notifications
    - Each notification is for one user

concerns (1) ----< (M) attachments
    - A concern can have multiple attachments
    - Each attachment belongs to one concern
```

---

## Key Design Decisions

### 1. **Status Workflow**
```
Pending → In Review → In Progress → Resolved → Closed
                          ↓
                      Rejected
```

### 2. **Ticket Number Format**
- Format: `GRV-YYYY-XXXXX`
- Example: `GRV-2025-00001`
- Generated automatically on concern creation

### 3. **SR-Code Validation**
- Format: `YY-XXXXX` (e.g., `21-12345`)
- Must be enforced at application level

### 4. **User Roles**
- `student`: Can file concerns and view their own submissions
- `admin`: SSC officers, can view all concerns and manage them

### 5. **Anonymous Reporting**
- Field: `is_anonymous` in concerns table
- If true, student name hidden from public view
- Admin can still see who filed it (for accountability)

### 6. **Audit Trail**
- `concern_status_history` provides complete tracking
- Every status change is logged with timestamp and who made it
- Promotes transparency and accountability (SDG 16)

---

## Sample Queries

### Get all pending concerns for a specific student
```sql
SELECT c.*, cat.category_name, o.office_name
FROM concerns c
JOIN concern_categories cat ON c.category_id = cat.category_id
LEFT JOIN offices o ON c.assigned_office_id = o.office_id
WHERE c.student_id = ? AND c.status = 'pending'
ORDER BY c.created_at DESC;
```

### Get concern with full history
```sql
SELECT 
    c.*,
    u.first_name || ' ' || u.last_name as student_name,
    cat.category_name,
    json_agg(
        json_build_object(
            'old_status', h.old_status,
            'new_status', h.new_status,
            'changed_at', h.created_at,
            'changed_by', admin.first_name || ' ' || admin.last_name
        ) ORDER BY h.created_at
    ) as status_history
FROM concerns c
JOIN users u ON c.student_id = u.user_id
JOIN concern_categories cat ON c.category_id = cat.category_id
LEFT JOIN concern_status_history h ON c.concern_id = h.concern_id
LEFT JOIN users admin ON h.changed_by = admin.user_id
WHERE c.concern_id = ?
GROUP BY c.concern_id, u.user_id, cat.category_id;
```

---

## Database Setup Script

See `schema.sql` for the complete PostgreSQL setup script.

