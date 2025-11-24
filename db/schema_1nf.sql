-- ============================================
-- FIRST NORMAL FORM (1NF)
-- Eliminated repeating groups and multi-valued attributes
-- Each cell contains only atomic values
-- ============================================

DROP TABLE IF EXISTS student_concerns_1nf CASCADE;

CREATE TABLE student_concerns_1nf (
    -- Primary Key
    record_id SERIAL PRIMARY KEY,
    
    -- Student Information (Repeated for each concern/comment/attachment)
    sr_code VARCHAR(20),
    student_email VARCHAR(255),
    student_password_hash VARCHAR(255),
    student_first_name VARCHAR(100),
    student_last_name VARCHAR(100),
    student_middle_name VARCHAR(100),
    student_program VARCHAR(100),
    student_year_level INTEGER,
    student_role VARCHAR(20) DEFAULT 'student',
    
    -- Concern Information (Repeated for each status change/comment/attachment)
    concern_ticket_number VARCHAR(50),
    concern_title VARCHAR(255),
    concern_description TEXT,
    concern_location VARCHAR(255),
    concern_incident_date DATE,
    concern_status VARCHAR(50),
    concern_priority VARCHAR(20),
    concern_is_anonymous BOOLEAN,
    concern_created_at TIMESTAMP,
    concern_resolution_notes TEXT,
    
    -- Category Information (Repeated)
    category_name VARCHAR(100),
    category_description TEXT,
    
    -- Office Information (Repeated)
    office_name VARCHAR(100),
    office_description TEXT,
    office_email VARCHAR(255),
    office_contact_number VARCHAR(20),
    
    -- Admin Information (Repeated)
    admin_sr_code VARCHAR(20),
    admin_first_name VARCHAR(100),
    admin_last_name VARCHAR(100),
    admin_email VARCHAR(255),
    admin_role VARCHAR(20) DEFAULT 'admin',
    
    -- Status Change Information (Now atomic - one per row)
    status_change_old VARCHAR(50),
    status_change_new VARCHAR(50),
    status_change_date TIMESTAMP,
    status_change_by_name VARCHAR(200),
    status_change_remarks TEXT,
    
    -- Comment Information (Now atomic - one per row)
    comment_text TEXT,
    comment_date TIMESTAMP,
    comment_by_name VARCHAR(200),
    comment_is_internal BOOLEAN,
    
    -- Attachment Information (Now atomic - one per row)
    attachment_file_name VARCHAR(255),
    attachment_file_path VARCHAR(500),
    attachment_file_type VARCHAR(50),
    attachment_uploaded_date TIMESTAMP,
    attachment_uploaded_by_name VARCHAR(200),
    
    -- Notification Information (Now atomic - one per row)
    notification_type VARCHAR(50),
    notification_title VARCHAR(255),
    notification_message TEXT,
    notification_is_read BOOLEAN,
    notification_date TIMESTAMP
);

-- IMPROVEMENTS IN 1NF:
-- ✅ Primary key added (record_id)
-- ✅ No multi-valued attributes
-- ✅ Each cell contains only atomic (single) values
-- ✅ Repeating groups eliminated by creating separate rows

-- REMAINING PROBLEMS:
-- ❌ Massive data redundancy (student info repeated in every row)
-- ❌ Update anomalies (changing student email requires updating multiple rows)
-- ❌ Insertion anomalies (can't add student without concern)
-- ❌ Deletion anomalies (deleting last concern deletes student info)
-- ❌ Partial dependencies exist

-- Sample data showing 1NF structure:
-- Note: Same concern with multiple status changes, comments, and attachments
-- creates multiple rows with repeated information

INSERT INTO student_concerns_1nf (
    sr_code, student_email, student_password_hash, student_first_name, student_last_name, 
    student_program, student_year_level, student_role,
    concern_ticket_number, concern_title, concern_description, concern_location, 
    concern_incident_date, concern_status, concern_priority, concern_is_anonymous, concern_created_at,
    category_name, category_description,
    office_name, office_email, office_contact_number,
    admin_sr_code, admin_first_name, admin_last_name, admin_email, admin_role,
    status_change_old, status_change_new, status_change_date, status_change_by_name,
    comment_text, comment_date, comment_by_name, comment_is_internal,
    attachment_file_name, attachment_file_path, attachment_uploaded_date,
    notification_type, notification_title, notification_message, notification_is_read, notification_date
) VALUES
-- Row 1: Initial status change + first comment + first attachment + notification
(
    '21-12345', 'juan@g.batstate-u.edu.ph', 'hashedpass123', 'Juan', 'Dela Cruz', 
    'BSCS', 3, 'student',
    'GRV-2025-00001', 'Broken AC in Room 401', 'The AC has been broken for 2 weeks', 'Room 401',
    '2025-11-01', 'pending', 'high', false, '2025-11-01 10:00:00',
    'Services & Facilities', 'Problems with campus facilities and services',
    'Facility Management', 'facilities@batstateu.edu.ph', '043-123-4567',
    '00-00000', 'Admin', 'User', 'admin@ssc.batstateu.edu.ph', 'admin',
    NULL, 'pending', '2025-11-01 10:00:00', 'Juan Dela Cruz',
    'Need repair ASAP', '2025-11-01 10:05:00', 'Juan Dela Cruz', false,
    'broken_ac.jpg', '/uploads/broken_ac.jpg', '2025-11-01 10:06:00',
    'concern_created', 'New Concern Filed', 'Your concern has been received', false, '2025-11-01 10:00:00'
),
-- Row 2: Same concern, second status change
(
    '21-12345', 'juan@g.batstate-u.edu.ph', 'hashedpass123', 'Juan', 'Dela Cruz',
    'BSCS', 3, 'student',
    'GRV-2025-00001', 'Broken AC in Room 401', 'The AC has been broken for 2 weeks', 'Room 401',
    '2025-11-01', 'in-review', 'high', false, '2025-11-01 10:00:00',
    'Services & Facilities', 'Problems with campus facilities and services',
    'Facility Management', 'facilities@batstateu.edu.ph', '043-123-4567',
    '00-00000', 'Admin', 'User', 'admin@ssc.batstateu.edu.ph', 'admin',
    'pending', 'in-review', '2025-11-02 14:30:00', 'Admin User',
    'Assigned to facilities department', '2025-11-02 14:35:00', 'Admin User', false,
    NULL, NULL, NULL,
    'status_changed', 'Status Updated', 'Your concern is now in review', false, '2025-11-02 14:30:00'
),
-- Row 3: Same concern, third status change
(
    '21-12345', 'juan@g.batstate-u.edu.ph', 'hashedpass123', 'Juan', 'Dela Cruz',
    'BSCS', 3, 'student',
    'GRV-2025-00001', 'Broken AC in Room 401', 'The AC has been broken for 2 weeks', 'Room 401',
    '2025-11-01', 'in-progress', 'high', false, '2025-11-01 10:00:00',
    'Services & Facilities', 'Problems with campus facilities and services',
    'Facility Management', 'facilities@batstateu.edu.ph', '043-123-4567',
    '00-00000', 'Admin', 'User', 'admin@ssc.batstateu.edu.ph', 'admin',
    'in-review', 'in-progress', '2025-11-03 09:00:00', 'Admin User',
    'Work in progress', '2025-11-03 09:15:00', 'Admin User', false,
    NULL, NULL, NULL,
    'status_changed', 'Status Updated', 'Work has started on your concern', false, '2025-11-03 09:00:00'
),
-- Row 4: Same concern, final status change + resolution
(
    '21-12345', 'juan@g.batstate-u.edu.ph', 'hashedpass123', 'Juan', 'Dela Cruz',
    'BSCS', 3, 'student',
    'GRV-2025-00001', 'Broken AC in Room 401', 'The AC has been broken for 2 weeks', 'Room 401',
    '2025-11-01', 'resolved', 'high', false, '2025-11-01 10:00:00',
    'Services & Facilities', 'Problems with campus facilities and services',
    'Facility Management', 'facilities@batstateu.edu.ph', '043-123-4567',
    '00-00000', 'Admin', 'User', 'admin@ssc.batstateu.edu.ph', 'admin',
    'in-progress', 'resolved', '2025-11-05 16:00:00', 'Admin User',
    'Fixed and tested', '2025-11-05 16:10:00', 'Admin User', false,
    'repair_report.pdf', '/uploads/repair_report.pdf', '2025-11-05 16:05:00',
    'concern_resolved', 'Concern Resolved', 'Your concern has been resolved', false, '2025-11-05 16:00:00'
);

-- Query example showing redundancy:
-- Getting all information about one concern requires joining multiple rows
SELECT DISTINCT
    concern_ticket_number,
    concern_title,
    student_first_name || ' ' || student_last_name as student_name
FROM student_concerns_1nf
WHERE concern_ticket_number = 'GRV-2025-00001';

-- This query shows the redundancy problem:
SELECT 
    COUNT(*) as total_rows,
    COUNT(DISTINCT concern_ticket_number) as unique_concerns
FROM student_concerns_1nf;
-- Result: 4 rows for 1 concern = 75% redundancy!
