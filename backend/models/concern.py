from backend.config.database import Database
import datetime

class Concern:
    """Concern model for database operations"""
    
    @staticmethod
    def create(student_id, category_id, title, description, assigned_office_id=None,
               location=None, incident_date=None, is_anonymous=False, priority='normal', other_category=None):
        """Create a new concern"""
        query = """
            INSERT INTO concerns (student_id, category_id, title, description, 
                                assigned_office_id, location, incident_date, 
                                is_anonymous, priority, status, other_category)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending', %s)
            RETURNING concern_id, ticket_number, title, status, priority, created_at
        """
        params = (student_id, category_id, title, description, assigned_office_id,
                 location, incident_date, is_anonymous, priority, other_category)
        result = Database.execute_query(query, params, fetch_one=True)
        
        # Log initial status
        if result:
            Concern.add_status_history(
                result['concern_id'], 
                None, 
                'pending', 
                student_id, 
                'Concern created'
            )
        
        return result
    
    @staticmethod
    def find_by_id(concern_id):
        """Get concern by ID with related information"""
        query = """
            SELECT c.*, 
                   u.first_name || ' ' || u.last_name AS student_name,
                   u.sr_code,
                   u.email AS student_email,
                   cat.category_name,
                   cat.description AS category_description,
                   o.office_name,
                   o.contact_email AS office_email,
                   admin.first_name || ' ' || admin.last_name AS admin_name,
                   c.other_category
            FROM concerns c
            JOIN users u ON c.student_id = u.user_id
            JOIN concern_categories cat ON c.category_id = cat.category_id
            LEFT JOIN offices o ON c.assigned_office_id = o.office_id
            LEFT JOIN users admin ON c.assigned_admin_id = admin.user_id
            WHERE c.concern_id = %s
        """
        return Database.execute_query(query, (concern_id,), fetch_one=True)
    
    @staticmethod
    def get_by_student(student_id):
        """Get all concerns by student"""
        query = """
            SELECT c.concern_id, c.ticket_number, c.title, c.description, c.status, c.priority,
                   c.created_at, c.updated_at, c.is_anonymous, c.location, c.incident_date,
                   c.category_id, c.assigned_office_id,
                   cat.category_name,
                   o.office_name
            FROM concerns c
            JOIN concern_categories cat ON c.category_id = cat.category_id
            LEFT JOIN offices o ON c.assigned_office_id = o.office_id
            WHERE c.student_id = %s
            ORDER BY c.created_at DESC
        """
        return Database.execute_query(query, (student_id,), fetch_all=True)
    
    @staticmethod
    def get_all(status=None, category_id=None, priority=None):
        """Get all concerns with optional filters"""
        query = """
            SELECT c.concern_id, c.ticket_number, c.title, c.description, c.status, c.priority,
                   c.created_at, c.updated_at, c.is_anonymous, c.location, c.incident_date,
                   c.category_id, c.assigned_office_id, c.student_id,
                   CASE WHEN c.is_anonymous THEN 'Anonymous' 
                        ELSE u.first_name || ' ' || u.last_name END AS student_name,
                   u.sr_code,
                   cat.category_name,
                   o.office_name
            FROM concerns c
            JOIN users u ON c.student_id = u.user_id
            JOIN concern_categories cat ON c.category_id = cat.category_id
            LEFT JOIN offices o ON c.assigned_office_id = o.office_id
            WHERE 1=1
        """
        params = []
        
        if status:
            query += " AND c.status = %s"
            params.append(status)
        
        if category_id:
            query += " AND c.category_id = %s"
            params.append(int(category_id))
        
        if priority:
            query += " AND c.priority = %s"
            params.append(priority)
        
        query += " ORDER BY c.created_at DESC"
        
        return Database.execute_query(query, tuple(params) if params else (), fetch_all=True)
    
    @staticmethod
    def update_status(concern_id, new_status, admin_id, remarks=None):
        """Update concern status"""
        # Get current status
        current = Database.execute_query(
            "SELECT status FROM concerns WHERE concern_id = %s",
            (concern_id,),
            fetch_one=True
        )
        
        if not current:
            return None
        
        old_status = current['status']
        
        # Update status
        query = """
            UPDATE concerns 
            SET status = %s, updated_at = CURRENT_TIMESTAMP
            WHERE concern_id = %s
            RETURNING concern_id, ticket_number, status
        """
        result = Database.execute_query(query, (new_status, concern_id), fetch_one=True)
        
        # Log status change
        if result:
            Concern.add_status_history(concern_id, old_status, new_status, admin_id, remarks)
        
        return result
    
    @staticmethod
    def assign_to_office(concern_id, office_id, admin_id):
        """Assign concern to an office"""
        query = """
            UPDATE concerns 
            SET assigned_office_id = %s, assigned_admin_id = %s, 
                updated_at = CURRENT_TIMESTAMP
            WHERE concern_id = %s
            RETURNING concern_id, ticket_number
        """
        return Database.execute_query(query, (office_id, admin_id, concern_id), fetch_one=True)
    
    @staticmethod
    def update_priority(concern_id, priority):
        """Update concern priority"""
        query = """
            UPDATE concerns 
            SET priority = %s, updated_at = CURRENT_TIMESTAMP
            WHERE concern_id = %s
            RETURNING concern_id, ticket_number, priority
        """
        return Database.execute_query(query, (priority, concern_id), fetch_one=True)
    
    @staticmethod
    def resolve(concern_id, admin_id, resolution_notes):
        """Mark concern as resolved"""
        query = """
            UPDATE concerns 
            SET status = 'resolved', resolved_by = %s, resolved_at = CURRENT_TIMESTAMP,
                resolution_notes = %s, updated_at = CURRENT_TIMESTAMP
            WHERE concern_id = %s
            RETURNING concern_id, ticket_number, status
        """
        result = Database.execute_query(query, (admin_id, resolution_notes, concern_id), fetch_one=True)
        
        if result:
            Concern.add_status_history(concern_id, 'in-progress', 'resolved', admin_id, 
                                      'Concern resolved: ' + resolution_notes)
        
        return result
    
    @staticmethod
    def add_status_history(concern_id, old_status, new_status, changed_by, remarks=None):
        """Add entry to status history"""
        query = """
            INSERT INTO concern_status_history 
            (concern_id, old_status, new_status, changed_by, remarks)
            VALUES (%s, %s, %s, %s, %s)
        """
        Database.execute_query(query, (concern_id, old_status, new_status, changed_by, remarks))
    
    @staticmethod
    def get_status_history(concern_id):
        """Get status history for a concern"""
        query = """
            SELECT h.*, u.first_name || ' ' || u.last_name AS changed_by_name
            FROM concern_status_history h
            JOIN users u ON h.changed_by = u.user_id
            WHERE h.concern_id = %s
            ORDER BY h.created_at ASC
        """
        return Database.execute_query(query, (concern_id,), fetch_all=True)
    
    @staticmethod
    def add_comment(concern_id, user_id, comment_text, is_internal=False):
        """Add comment to concern"""
        query = """
            INSERT INTO comments (concern_id, user_id, comment_text, is_internal)
            VALUES (%s, %s, %s, %s)
            RETURNING comment_id, comment_text, created_at
        """
        return Database.execute_query(query, (concern_id, user_id, comment_text, is_internal), 
                                     fetch_one=True)
    
    @staticmethod
    def get_comments(concern_id, include_internal=False):
        """Get comments for a concern"""
        query = """
            SELECT c.*, u.first_name || ' ' || u.last_name AS author_name, u.role AS author_role
            FROM comments c
            JOIN users u ON c.user_id = u.user_id
            WHERE c.concern_id = %s
        """
        
        if not include_internal:
            query += " AND c.is_internal = false"
        
        query += " ORDER BY c.created_at ASC"
        
        return Database.execute_query(query, (concern_id,), fetch_all=True)
    
    @staticmethod
    def get_statistics():
        """Get concern statistics"""
        query = """
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending,
                COUNT(CASE WHEN status = 'in-review' THEN 1 END) as in_review,
                COUNT(CASE WHEN status = 'in-progress' THEN 1 END) as in_progress,
                COUNT(CASE WHEN status = 'resolved' THEN 1 END) as resolved,
                COUNT(CASE WHEN status = 'closed' THEN 1 END) as closed,
                COUNT(CASE WHEN priority = 'urgent' THEN 1 END) as urgent,
                COUNT(CASE WHEN priority = 'high' THEN 1 END) as high
            FROM concerns
        """
        return Database.execute_query(query, fetch_one=True)
