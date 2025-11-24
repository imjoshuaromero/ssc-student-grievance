-- ============================================
-- Student Grievance Reporting System Database Schema
-- BatState-U TNEU Lipa - SSC Project
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
-- TABLE: users
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
    google_id VARCHAR(255) UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_sr_code ON users(sr_code);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_google_id ON users(google_id);

-- ============================================
-- TABLE: concern_categories
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
-- TABLE: offices
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
INSERT INTO offices (office_name, description, contact_email) VALUES
('SSC', 'Supreme Student Council', 'ssc@batstateu.edu.ph'),
('Registrar', 'Office of the Registrar', 'registrar@batstateu.edu.ph'),
('OSAS', 'Office of Student Affairs and Services', 'osas@batstateu.edu.ph'),
('Facility Management', 'Campus Facility Management', 'facilities@batstateu.edu.ph'),
('Academic Affairs', 'Office of Academic Affairs', 'academics@batstateu.edu.ph');

-- ============================================
-- TABLE: concerns
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
-- TABLE: concern_status_history
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
-- TABLE: comments
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
-- TABLE: notifications
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
-- TABLE: attachments
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
-- FUNCTION: Generate Ticket Number
-- ============================================
CREATE OR REPLACE FUNCTION generate_ticket_number()
RETURNS TRIGGER AS $$
DECLARE
    year_part VARCHAR(4);
    seq_number INTEGER;
    new_ticket VARCHAR(50);
BEGIN
    year_part := TO_CHAR(CURRENT_DATE, 'YYYY');
    
    SELECT COUNT(*) + 1 INTO seq_number
    FROM concerns
    WHERE EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM CURRENT_DATE);
    
    new_ticket := 'GRV-' || year_part || '-' || LPAD(seq_number::TEXT, 5, '0');
    
    NEW.ticket_number := new_ticket;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- TRIGGER: Auto-generate ticket number
-- ============================================
CREATE TRIGGER trigger_generate_ticket_number
BEFORE INSERT ON concerns
FOR EACH ROW
WHEN (NEW.ticket_number IS NULL OR NEW.ticket_number = '')
EXECUTE FUNCTION generate_ticket_number();

-- ============================================
-- FUNCTION: Update timestamp
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- TRIGGERS: Auto-update updated_at timestamp
-- ============================================
CREATE TRIGGER trigger_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trigger_concerns_updated_at
BEFORE UPDATE ON concerns
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trigger_comments_updated_at
BEFORE UPDATE ON comments
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- FUNCTION: Log status changes
-- ============================================
CREATE OR REPLACE FUNCTION log_status_change()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'UPDATE' AND OLD.status != NEW.status) THEN
        INSERT INTO concern_status_history (concern_id, old_status, new_status, changed_by, remarks)
        VALUES (NEW.concern_id, OLD.status, NEW.status, NEW.assigned_admin_id, 'Status updated');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- TRIGGER: Auto-log status changes
-- ============================================
CREATE TRIGGER trigger_log_status_change
AFTER UPDATE ON concerns
FOR EACH ROW
EXECUTE FUNCTION log_status_change();

-- ============================================
-- Sample Data (For Testing)
-- ============================================

-- Insert sample admin user (password: admin123)
INSERT INTO users (sr_code, email, password_hash, first_name, last_name, role) VALUES
('00-00000', 'admin@ssc.batstateu.edu.ph', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg9KW', 'Admin', 'User', 'admin');

-- Insert sample student users (password: student123)
INSERT INTO users (sr_code, email, password_hash, first_name, last_name, program, year_level, role) VALUES
('21-12345', 'student1@g.batstate-u.edu.ph', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg9KW', 'Juan', 'Dela Cruz', 'BSCS', 3, 'student'),
('22-67890', 'student2@g.batstate-u.edu.ph', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg9KW', 'Maria', 'Santos', 'BSIT', 2, 'student');

-- ============================================
-- VIEWS (Useful queries as views)
-- ============================================

-- View: Active concerns summary
CREATE VIEW vw_active_concerns AS
SELECT 
    c.concern_id,
    c.ticket_number,
    c.title,
    c.status,
    c.priority,
    c.created_at,
    u.first_name || ' ' || u.last_name AS student_name,
    u.sr_code,
    cat.category_name,
    o.office_name
FROM concerns c
JOIN users u ON c.student_id = u.user_id
JOIN concern_categories cat ON c.category_id = cat.category_id
LEFT JOIN offices o ON c.assigned_office_id = o.office_id
WHERE c.status NOT IN ('closed', 'resolved')
ORDER BY 
    CASE c.priority
        WHEN 'urgent' THEN 1
        WHEN 'high' THEN 2
        WHEN 'normal' THEN 3
        WHEN 'low' THEN 4
    END,
    c.created_at DESC;

-- View: Concern statistics
CREATE VIEW vw_concern_stats AS
SELECT 
    status,
    COUNT(*) as count,
    COUNT(CASE WHEN priority = 'urgent' THEN 1 END) as urgent_count,
    COUNT(CASE WHEN priority = 'high' THEN 1 END) as high_count
FROM concerns
GROUP BY status;

-- ============================================
-- Grant permissions (adjust as needed)
-- ============================================
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_db_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_db_user;

