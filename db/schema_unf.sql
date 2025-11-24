-- ============================================
-- UNNORMALIZED FORM (UNF)
-- Single table with repeating groups and multi-valued attributes
-- ============================================

-- Note: This is a conceptual representation
-- PostgreSQL doesn't support multi-valued attributes in a single cell
-- This shows the problematic structure before normalization

CREATE TABLE student_grievance_system_unf (
    -- Student Information
    sr_code VARCHAR(20),
    student_email VARCHAR(255),
    student_password VARCHAR(255),
    student_first_name VARCHAR(100),
    student_last_name VARCHAR(100),
    student_middle_name VARCHAR(100),
    student_program VARCHAR(100),
    student_year_level INTEGER,
    
    -- Concern Information
    concern_ticket_number VARCHAR(50),
    concern_title VARCHAR(255),
    concern_description TEXT,
    concern_location VARCHAR(255),
    concern_incident_date DATE,
    concern_status VARCHAR(50),
    concern_priority VARCHAR(20),
    concern_created_at TIMESTAMP,
    
    -- Category Information
    concern_category_name VARCHAR(100),
    concern_category_description TEXT,
    
    -- Office Information
    office_name VARCHAR(100),
    office_email VARCHAR(255),
    office_contact_number VARCHAR(20),
    
    -- Admin Information
    admin_sr_code VARCHAR(20),
    admin_first_name VARCHAR(100),
    admin_last_name VARCHAR(100),
    admin_email VARCHAR(255),
    
    -- Repeating Groups (Multi-valued attributes - BAD DESIGN)
    -- In reality, these would be stored as comma-separated strings or arrays
    status_history TEXT,  -- Contains: "pending,2025-11-01,admin1;in-review,2025-11-02,admin2;..."
    comments TEXT,        -- Contains: "comment1,2025-11-01,user1;comment2,2025-11-02,user2;..."
    attachments TEXT,     -- Contains: "file1.jpg,2025-11-01;file2.pdf,2025-11-02;..."
    notifications TEXT,   -- Contains: "notif1,2025-11-01,unread;notif2,2025-11-02,read;..."
    
    resolution_notes TEXT
);

-- PROBLEMS WITH UNF:
-- 1. No primary key
-- 2. Repeating groups (multiple statuses, comments, attachments in one row)
-- 3. Multi-valued attributes stored as text
-- 4. Massive data redundancy
-- 5. Update anomalies
-- 6. Insertion anomalies
-- 7. Deletion anomalies
-- 8. Difficult to query
-- 9. No data integrity
-- 10. Violates atomicity principle

-- Sample data showing the problems:
INSERT INTO student_grievance_system_unf VALUES (
    '21-12345', 'juan@g.batstate-u.edu.ph', 'hashedpass123', 'Juan', 'Dela Cruz', 'M', 'BSCS', 3,
    'GRV-2025-00001', 'Broken AC in Room 401', 'The AC has been broken for 2 weeks', 'Room 401', '2025-11-01',
    'resolved', 'high', '2025-11-01 10:00:00',
    'Services & Facilities', 'Problems with campus facilities and services',
    'Facility Management', 'facilities@batstateu.edu.ph', '043-123-4567',
    '00-00000', 'Admin', 'User', 'admin@ssc.batstateu.edu.ph',
    'pending,2025-11-01,Admin User;in-review,2025-11-02,Admin User;in-progress,2025-11-03,Admin User;resolved,2025-11-05,Admin User',
    'Need repair ASAP,2025-11-01,Juan Dela Cruz;Assigned to facilities,2025-11-02,Admin User;Work in progress,2025-11-03,Admin User;Fixed,2025-11-05,Admin User',
    'broken_ac.jpg,2025-11-01;repair_report.pdf,2025-11-05',
    'Concern received,2025-11-01,false;Status updated,2025-11-02,true;Concern resolved,2025-11-05,false',
    'AC unit was replaced with a new one. Issue resolved.'
);
