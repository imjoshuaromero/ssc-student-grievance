-- Update Offices in Database
-- This script will clear existing offices and add the new list

-- First, disable foreign key checks temporarily by deleting in proper order
DELETE FROM concern_status_history WHERE concern_id IN (SELECT concern_id FROM concerns WHERE assigned_office_id IS NOT NULL);
DELETE FROM comments WHERE concern_id IN (SELECT concern_id FROM concerns WHERE assigned_office_id IS NOT NULL);
DELETE FROM notifications WHERE concern_id IN (SELECT concern_id FROM concerns WHERE assigned_office_id IS NOT NULL);
DELETE FROM attachments WHERE concern_id IN (SELECT concern_id FROM concerns WHERE assigned_office_id IS NOT NULL);

-- Update concerns to remove office assignments before deleting offices
UPDATE concerns SET assigned_office_id = NULL WHERE assigned_office_id IS NOT NULL;

-- Now delete all existing offices
DELETE FROM offices;

-- Reset the sequence
ALTER SEQUENCE offices_office_id_seq RESTART WITH 1;

-- Insert new offices
INSERT INTO offices (office_name, description, contact_email) VALUES
('SSC', 'Supreme Student Council', 'ssc@batstateu.edu.ph'),
('Registrar', 'Office of the Registrar', 'registrar@batstateu.edu.ph'),
('Office of the Student Discipline', 'Office of the Student Discipline', 'discipline@batstateu.edu.ph'),
('Scholarship and Financial Assistance Office', 'Scholarship and Financial Assistance Office', 'scholarship@batstateu.edu.ph'),
('Office of the Guidance and Counseling', 'Office of the Guidance and Counseling', 'guidance@batstateu.edu.ph'),
('Academic Affairs', 'Office of Academic Affairs', 'academics@batstateu.edu.ph'),
('General Services Office (GSO)', 'General Services Office', 'gso@batstateu.edu.ph'),
('ICT Office', 'Information and Communications Technology Office', 'ict@batstateu.edu.ph');

-- Verify the changes
SELECT office_id, office_name, description, contact_email FROM offices ORDER BY office_id;
