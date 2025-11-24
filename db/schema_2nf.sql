-- ============================================
-- SECOND NORMAL FORM (2NF)
-- Removed partial dependencies
-- All non-key attributes depend on the entire primary key
-- ============================================

-- Drop tables if they exist
DROP TABLE IF EXISTS notifications_2nf CASCADE;
DROP TABLE IF EXISTS attachments_2nf CASCADE;
DROP TABLE IF EXISTS comments_2nf CASCADE;
DROP TABLE IF EXISTS status_history_2nf CASCADE;
DROP TABLE IF EXISTS concerns_2nf CASCADE;
DROP TABLE IF EXISTS users_2nf CASCADE;

-- ============================================
-- TABLE 1: users_2nf
-- Stores all user information (students and admins)
-- ============================================
CREATE TABLE users_2nf (
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

CREATE INDEX idx_users_2nf_sr_code ON users_2nf(sr_code);
CREATE INDEX idx_users_2nf_email ON users_2nf(email);
CREATE INDEX idx_users_2nf_role ON users_2nf(role);

-- ============================================
-- TABLE 2: concerns_2nf
-- Stores concern information
-- ============================================
CREATE TABLE concerns_2nf (
    concern_id SERIAL PRIMARY KEY,
    ticket_number VARCHAR(50) UNIQUE NOT NULL,
    student_user_id INTEGER NOT NULL,
    admin_user_id INTEGER,
    
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(255),
    incident_date DATE,
    
    -- Category information (still embedded - has transitive dependency)
    category_name VARCHAR(100) NOT NULL,
    category_description TEXT,
    
    -- Office information (still embedded - has transitive dependency)
    office_name VARCHAR(100),
    office_description TEXT,
    office_email VARCHAR(255),
    office_contact_number VARCHAR(20),
    
    status VARCHAR(50) NOT NULL DEFAULT 'pending' 
        CHECK (status IN ('pending', 'in-review', 'in-progress', 'resolved', 'closed', 'rejected')),
    priority VARCHAR(20) DEFAULT 'normal' 
        CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    
    is_anonymous BOOLEAN DEFAULT FALSE,
    resolution_notes TEXT,
    resolved_at TIMESTAMP,
    resolved_by_user_id INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (student_user_id) REFERENCES users_2nf(user_id) ON DELETE CASCADE,
    FOREIGN KEY (admin_user_id) REFERENCES users_2nf(user_id),
    FOREIGN KEY (resolved_by_user_id) REFERENCES users_2nf(user_id)
);

CREATE INDEX idx_concerns_2nf_student ON concerns_2nf(student_user_id);
CREATE INDEX idx_concerns_2nf_status ON concerns_2nf(status);
CREATE INDEX idx_concerns_2nf_ticket ON concerns_2nf(ticket_number);

-- ============================================
-- TABLE 3: status_history_2nf
-- Tracks all status changes
-- ============================================
CREATE TABLE status_history_2nf (
    history_id SERIAL PRIMARY KEY,
    concern_id INTEGER NOT NULL,
    changed_by_user_id INTEGER NOT NULL,
    old_status VARCHAR(50),
    new_status VARCHAR(50) NOT NULL,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (concern_id) REFERENCES concerns_2nf(concern_id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by_user_id) REFERENCES users_2nf(user_id)
);

CREATE INDEX idx_status_history_2nf_concern ON status_history_2nf(concern_id);

-- ============================================
-- TABLE 4: comments_2nf
-- Stores comments on concerns
-- ============================================
CREATE TABLE comments_2nf (
    comment_id SERIAL PRIMARY KEY,
    concern_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    comment_text TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (concern_id) REFERENCES concerns_2nf(concern_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users_2nf(user_id) ON DELETE CASCADE
);

CREATE INDEX idx_comments_2nf_concern ON comments_2nf(concern_id);
CREATE INDEX idx_comments_2nf_user ON comments_2nf(user_id);

-- ============================================
-- TABLE 5: attachments_2nf
-- Stores file attachments
-- ============================================
CREATE TABLE attachments_2nf (
    attachment_id SERIAL PRIMARY KEY,
    concern_id INTEGER NOT NULL,
    uploaded_by_user_id INTEGER NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(50),
    file_size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (concern_id) REFERENCES concerns_2nf(concern_id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by_user_id) REFERENCES users_2nf(user_id)
);

CREATE INDEX idx_attachments_2nf_concern ON attachments_2nf(concern_id);

-- ============================================
-- TABLE 6: notifications_2nf
-- Stores notifications
-- ============================================
CREATE TABLE notifications_2nf (
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
    
    FOREIGN KEY (user_id) REFERENCES users_2nf(user_id) ON DELETE CASCADE,
    FOREIGN KEY (concern_id) REFERENCES concerns_2nf(concern_id) ON DELETE CASCADE
);

CREATE INDEX idx_notifications_2nf_user ON notifications_2nf(user_id);
CREATE INDEX idx_notifications_2nf_read ON notifications_2nf(is_read);

-- ============================================
-- SAMPLE DATA
-- ============================================

-- Insert users
INSERT INTO users_2nf (sr_code, email, password_hash, first_name, last_name, program, year_level, role) VALUES
('21-12345', 'juan@g.batstate-u.edu.ph', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg9KW', 'Juan', 'Dela Cruz', 'BSCS', 3, 'student'),
('22-67890', 'maria@g.batstate-u.edu.ph', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg9KW', 'Maria', 'Santos', 'BSIT', 2, 'student'),
('00-00000', 'admin@ssc.batstateu.edu.ph', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg9KW', 'Admin', 'User', NULL, NULL, 'admin');

-- Insert concern
INSERT INTO concerns_2nf (
    ticket_number, student_user_id, admin_user_id, title, description, location, incident_date,
    category_name, category_description, office_name, office_email, office_contact_number,
    status, priority, is_anonymous, created_at
) VALUES (
    'GRV-2025-00001', 1, 3, 'Broken AC in Room 401', 
    'The AC has been broken for 2 weeks affecting classes',
    'Room 401', '2025-11-01',
    'Services & Facilities', 'Problems with campus facilities and services',
    'Facility Management', 'facilities@batstateu.edu.ph', '043-123-4567',
    'resolved', 'high', false, '2025-11-01 10:00:00'
);

-- Insert status history
INSERT INTO status_history_2nf (concern_id, changed_by_user_id, old_status, new_status, remarks, created_at) VALUES
(1, 1, NULL, 'pending', 'Concern filed', '2025-11-01 10:00:00'),
(1, 3, 'pending', 'in-review', 'Assigned to facilities department', '2025-11-02 14:30:00'),
(1, 3, 'in-review', 'in-progress', 'Technician dispatched', '2025-11-03 09:00:00'),
(1, 3, 'in-progress', 'resolved', 'AC unit replaced', '2025-11-05 16:00:00');

-- Insert comments
INSERT INTO comments_2nf (concern_id, user_id, comment_text, is_internal, created_at) VALUES
(1, 1, 'Need repair ASAP, classes are very hot', false, '2025-11-01 10:05:00'),
(1, 3, 'Assigned to facilities department', false, '2025-11-02 14:35:00'),
(1, 3, 'Internal note: Check budget for replacement', true, '2025-11-02 14:40:00'),
(1, 3, 'Work in progress, technician on site', false, '2025-11-03 09:15:00'),
(1, 3, 'Fixed and tested. New AC unit installed.', false, '2025-11-05 16:10:00');

-- Insert attachments
INSERT INTO attachments_2nf (concern_id, uploaded_by_user_id, file_name, file_path, file_type, created_at) VALUES
(1, 1, 'broken_ac.jpg', '/uploads/2025/11/broken_ac.jpg', 'image/jpeg', '2025-11-01 10:06:00'),
(1, 3, 'repair_report.pdf', '/uploads/2025/11/repair_report.pdf', 'application/pdf', '2025-11-05 16:05:00');

-- Insert notifications
INSERT INTO notifications_2nf (user_id, concern_id, notification_type, title, message, is_read, created_at) VALUES
(1, 1, 'concern_created', 'Concern Received', 'Your concern GRV-2025-00001 has been received', true, '2025-11-01 10:00:00'),
(1, 1, 'status_changed', 'Status Updated', 'Your concern is now in review', true, '2025-11-02 14:30:00'),
(1, 1, 'status_changed', 'Work in Progress', 'Work has started on your concern', true, '2025-11-03 09:00:00'),
(1, 1, 'concern_resolved', 'Concern Resolved', 'Your concern has been resolved', false, '2025-11-05 16:00:00');

-- ============================================
-- IMPROVEMENTS IN 2NF:
-- ============================================
-- ✅ No partial dependencies
-- ✅ Significantly reduced redundancy
-- ✅ Each table focuses on a specific entity
-- ✅ Easier to update user information
-- ✅ Can add users without concerns
-- ✅ Deleting a concern doesn't delete user info

-- ============================================
-- REMAINING PROBLEMS (Transitive Dependencies):
-- ============================================
-- ❌ category_description depends on category_name (not primary key)
-- ❌ office_email depends on office_name (not primary key)
-- ❌ If category description changes, must update all concerns with that category
-- ❌ If office info changes, must update all concerns assigned to that office

-- Example query showing the transitive dependency problem:
SELECT 
    concern_id, 
    category_name, 
    category_description,
    office_name,
    office_email
FROM concerns_2nf
WHERE category_name = 'Services & Facilities';
-- If we need to update category description, we must update all matching rows!

-- Better approach: Move categories and offices to separate tables (→ 3NF)
