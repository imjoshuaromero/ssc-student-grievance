-- ============================================
-- THIRD NORMAL FORM (3NF) - FINAL SCHEMA
-- Removed transitive dependencies
-- All non-key attributes depend ONLY on the primary key
-- ============================================

-- Drop tables if they exist (in reverse order of dependencies)
DROP TABLE IF EXISTS attachments CASCADE;
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS comments CASCADE;
DROP TABLE IF EXISTS concern_status_history CASCADE;
DROP TABLE IF EXISTS concerns CASCADE;
DROP TABLE IF EXISTS offices CASCADE;
DROP TABLE IF EXISTS concern_categories CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ============================================
-- TABLE 1: users
-- Stores all user accounts (students and admins)
-- ============================================
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
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_sr_code ON users(sr_code);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- ============================================
-- TABLE 2: concern_categories
-- Stores concern categories (ELIMINATES TRANSITIVE DEPENDENCY)
-- ============================================
CREATE TABLE concern_categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default categories
INSERT INTO concern_categories (category_name, description) VALUES
('Academic', 'Concerns related to classes, grades, curriculum, and academic matters'),
('Administrative Decisions', 'Issues with administrative policies, decisions, and procedures'),
('Services & Facilities', 'Problems with campus facilities, services, and infrastructure'),
('Harassment', 'Harassment, discrimination, or bullying reports'),
('Others', 'Other concerns not covered by the above categories');

-- ============================================
-- TABLE 3: offices
-- Stores office information (ELIMINATES TRANSITIVE DEPENDENCY)
-- ============================================
CREATE TABLE offices (
    office_id SERIAL PRIMARY KEY,
    office_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    contact_email VARCHAR(255),
    contact_number VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default offices
INSERT INTO offices (office_name, description, contact_email, contact_number) VALUES
('SSC', 'Supreme Student Council', 'ssc@batstateu.edu.ph', '043-778-2170'),
('Registrar', 'Office of the Registrar', 'registrar@batstateu.edu.ph', '043-778-2171'),
('OSAS', 'Office of Student Affairs and Services', 'osas@batstateu.edu.ph', '043-778-2172'),
('Facility Management', 'Campus Facility Management', 'facilities@batstateu.edu.ph', '043-778-2173'),
('Academic Affairs', 'Office of Academic Affairs', 'academics@batstateu.edu.ph', '043-778-2174');

-- ============================================
-- TABLE 4: concerns
-- Main table for grievance reports (NO TRANSITIVE DEPENDENCIES)
-- ============================================
CREATE TABLE concerns (
    concern_id SERIAL PRIMARY KEY,
    ticket_number VARCHAR(50) UNIQUE NOT NULL,
    student_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    assigned_office_id INTEGER,
    assigned_admin_id INTEGER,
    
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(255),
    incident_date DATE,
    
    status VARCHAR(50) NOT NULL DEFAULT 'pending' 
        CHECK (status IN ('pending', 'in-review', 'in-progress', 'resolved', 'closed', 'rejected')),
    priority VARCHAR(20) DEFAULT 'normal' 
        CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    
    is_anonymous BOOLEAN DEFAULT FALSE,
    
    resolution_notes TEXT,
    resolved_at TIMESTAMP,
    resolved_by INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES concern_categories(category_id),
    FOREIGN KEY (assigned_office_id) REFERENCES offices(office_id),
    FOREIGN KEY (assigned_admin_id) REFERENCES users(user_id),
    FOREIGN KEY (resolved_by) REFERENCES users(user_id)
);

CREATE INDEX idx_concerns_student_id ON concerns(student_id);
CREATE INDEX idx_concerns_status ON concerns(status);
CREATE INDEX idx_concerns_category_id ON concerns(category_id);
CREATE INDEX idx_concerns_ticket_number ON concerns(ticket_number);
CREATE INDEX idx_concerns_created_at ON concerns(created_at);

-- ============================================
-- TABLE 5: concern_status_history
-- Tracks all status changes for audit trail
-- ============================================
CREATE TABLE concern_status_history (
    history_id SERIAL PRIMARY KEY,
    concern_id INTEGER NOT NULL,
    old_status VARCHAR(50),
    new_status VARCHAR(50) NOT NULL,
    changed_by INTEGER NOT NULL,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (concern_id) REFERENCES concerns(concern_id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users(user_id)
);

CREATE INDEX idx_history_concern_id ON concern_status_history(concern_id);
CREATE INDEX idx_history_created_at ON concern_status_history(created_at);

-- ============================================
-- TABLE 6: comments
-- Communication thread between students and admins
-- ============================================
CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    concern_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    comment_text TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (concern_id) REFERENCES concerns(concern_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE INDEX idx_comments_concern_id ON comments(concern_id);
CREATE INDEX idx_comments_user_id ON comments(user_id);
CREATE INDEX idx_comments_created_at ON comments(created_at);

-- ============================================
-- TABLE 7: notifications
-- Notification system for users
-- ============================================
CREATE TABLE notifications (
    notification_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    concern_id INTEGER,
    notification_type VARCHAR(50) NOT NULL 
        CHECK (notification_type IN ('concern_created', 'status_changed', 'comment_added', 'concern_assigned', 'concern_resolved')),
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (concern_id) REFERENCES concerns(concern_id) ON DELETE CASCADE
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);
CREATE INDEX idx_notifications_created_at ON notifications(created_at);

-- ============================================
-- TABLE 8: attachments
-- File attachments for concerns
-- ============================================
CREATE TABLE attachments (
    attachment_id SERIAL PRIMARY KEY,
    concern_id INTEGER NOT NULL,
    uploaded_by INTEGER NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(50),
    file_size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (concern_id) REFERENCES concerns(concern_id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(user_id)
);

CREATE INDEX idx_attachments_concern_id ON attachments(concern_id);

-- ============================================
-- SAMPLE DATA
-- ============================================

-- Insert users
INSERT INTO users (sr_code, email, password_hash, first_name, last_name, program, year_level, role) VALUES
('21-12345', 'juan@g.batstate-u.edu.ph', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg9KW', 'Juan', 'Dela Cruz', 'BSCS', 3, 'student'),
('22-67890', 'maria@g.batstate-u.edu.ph', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg9KW', 'Maria', 'Santos', 'BSIT', 2, 'student'),
('00-00000', 'admin@ssc.batstateu.edu.ph', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg9KW', 'Admin', 'User', NULL, NULL, 'admin');

-- Insert concern (now using foreign keys instead of embedded data)
INSERT INTO concerns (
    ticket_number, student_id, category_id, assigned_office_id, assigned_admin_id,
    title, description, location, incident_date, status, priority, is_anonymous,
    resolution_notes, resolved_at, resolved_by, created_at
) VALUES (
    'GRV-2025-00001', 1, 3, 4, 3,
    'Broken AC in Room 401', 
    'The AC has been broken for 2 weeks affecting classes. Students are uncomfortable during lectures.',
    'Room 401', '2025-11-01', 
    'resolved', 'high', false,
    'AC unit was replaced with a new energy-efficient model. Tested and working properly.',
    '2025-11-05 16:00:00', 3,
    '2025-11-01 10:00:00'
);

-- Insert status history
INSERT INTO concern_status_history (concern_id, old_status, new_status, changed_by, remarks, created_at) VALUES
(1, NULL, 'pending', 1, 'Concern filed by student', '2025-11-01 10:00:00'),
(1, 'pending', 'in-review', 3, 'Assigned to Facility Management office', '2025-11-02 14:30:00'),
(1, 'in-review', 'in-progress', 3, 'Technician dispatched to assess the issue', '2025-11-03 09:00:00'),
(1, 'in-progress', 'resolved', 3, 'AC unit replaced and tested successfully', '2025-11-05 16:00:00');

-- Insert comments
INSERT INTO comments (concern_id, user_id, comment_text, is_internal, created_at) VALUES
(1, 1, 'The AC has been broken for 2 weeks now. Need urgent repair as classes are very hot.', false, '2025-11-01 10:05:00'),
(1, 3, 'Thank you for reporting. This has been assigned to the Facility Management office.', false, '2025-11-02 14:35:00'),
(1, 3, 'Internal note: Check budget approval for AC replacement vs repair', true, '2025-11-02 14:40:00'),
(1, 3, 'Update: Technician confirmed AC unit needs replacement. Work order approved.', false, '2025-11-03 09:15:00'),
(1, 3, 'Resolved: New AC unit installed and tested. Please verify if working properly.', false, '2025-11-05 16:10:00'),
(1, 1, 'Thank you! The new AC is working great.', false, '2025-11-06 08:00:00');

-- Insert attachments
INSERT INTO attachments (concern_id, uploaded_by, file_name, file_path, file_type, file_size, created_at) VALUES
(1, 1, 'broken_ac.jpg', '/uploads/2025/11/01/broken_ac.jpg', 'image/jpeg', 245678, '2025-11-01 10:06:00'),
(1, 3, 'assessment_report.pdf', '/uploads/2025/11/03/assessment_report.pdf', 'application/pdf', 156789, '2025-11-03 09:20:00'),
(1, 3, 'repair_invoice.pdf', '/uploads/2025/11/05/repair_invoice.pdf', 'application/pdf', 98765, '2025-11-05 16:05:00');

-- Insert notifications
INSERT INTO notifications (user_id, concern_id, notification_type, title, message, is_read, read_at, created_at) VALUES
(1, 1, 'concern_created', 'Concern Received', 'Your concern GRV-2025-00001 has been successfully received by SSC.', true, '2025-11-01 10:30:00', '2025-11-01 10:00:00'),
(1, 1, 'status_changed', 'Status Updated: In Review', 'Your concern is now being reviewed by the Facility Management office.', true, '2025-11-02 15:00:00', '2025-11-02 14:30:00'),
(1, 1, 'comment_added', 'New Comment Added', 'Admin has added a comment to your concern.', true, '2025-11-02 15:30:00', '2025-11-02 14:35:00'),
(1, 1, 'status_changed', 'Work in Progress', 'Work has started on your concern. A technician has been dispatched.', true, '2025-11-03 10:00:00', '2025-11-03 09:00:00'),
(1, 1, 'concern_resolved', 'Concern Resolved', 'Your concern has been successfully resolved. Please verify the resolution.', false, NULL, '2025-11-05 16:00:00');

-- ============================================
-- BENEFITS OF 3NF:
-- ============================================
-- ✅ No transitive dependencies
-- ✅ Minimal data redundancy
-- ✅ Easy to update category/office information (single location)
-- ✅ Data integrity enforced through foreign keys
-- ✅ No update anomalies
-- ✅ No insertion anomalies
-- ✅ No deletion anomalies
-- ✅ Scalable and maintainable
-- ✅ Supports audit trail (SDG 16: Transparency)
-- ✅ Clean separation of concerns

-- ============================================
-- EXAMPLE QUERIES DEMONSTRATING 3NF BENEFITS
-- ============================================

-- Query 1: Get concern with all related information (using JOINs)
SELECT 
    c.ticket_number,
    c.title,
    c.status,
    c.priority,
    u.first_name || ' ' || u.last_name AS student_name,
    u.sr_code,
    cat.category_name,
    o.office_name,
    o.contact_email,
    admin.first_name || ' ' || admin.last_name AS assigned_admin
FROM concerns c
JOIN users u ON c.student_id = u.user_id
JOIN concern_categories cat ON c.category_id = cat.category_id
LEFT JOIN offices o ON c.assigned_office_id = o.office_id
LEFT JOIN users admin ON c.assigned_admin_id = admin.user_id
WHERE c.concern_id = 1;

-- Query 2: Update category description (affects only 1 row, not multiple concerns)
UPDATE concern_categories 
SET description = 'Updated: Issues related to campus facilities, infrastructure, and maintenance'
WHERE category_name = 'Services & Facilities';
-- In 2NF, this would require updating ALL concerns with this category!

-- Query 3: Update office contact info (affects only 1 row)
UPDATE offices 
SET contact_email = 'new.facilities@batstateu.edu.ph',
    contact_number = '043-778-2999'
WHERE office_name = 'Facility Management';
-- In 2NF, this would require updating ALL concerns assigned to this office!

-- Query 4: Get complete concern history (demonstrates proper relationships)
SELECT 
    h.history_id,
    h.old_status,
    h.new_status,
    h.created_at,
    u.first_name || ' ' || u.last_name AS changed_by,
    h.remarks
FROM concern_status_history h
JOIN users u ON h.changed_by = u.user_id
WHERE h.concern_id = 1
ORDER BY h.created_at;

-- Query 5: Statistics by category (efficient with proper normalization)
SELECT 
    cat.category_name,
    COUNT(c.concern_id) AS total_concerns,
    COUNT(CASE WHEN c.status = 'resolved' THEN 1 END) AS resolved,
    COUNT(CASE WHEN c.status = 'pending' THEN 1 END) AS pending
FROM concern_categories cat
LEFT JOIN concerns c ON cat.category_id = c.category_id
GROUP BY cat.category_id, cat.category_name
ORDER BY total_concerns DESC;

-- ============================================
-- THIS IS THE FINAL, PRODUCTION-READY SCHEMA
-- ============================================
