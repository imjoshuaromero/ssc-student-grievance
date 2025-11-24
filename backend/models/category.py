from backend.config.database import Database

class Category:
    """Category model for database operations"""
    
    @staticmethod
    def get_all():
        """Get all active categories"""
        query = """
            SELECT category_id, category_name, description, created_at
            FROM concern_categories
            WHERE is_active = true
            ORDER BY category_name
        """
        return Database.execute_query(query, fetch_all=True)
    
    @staticmethod
    def find_by_id(category_id):
        """Find category by ID"""
        query = """
            SELECT * FROM concern_categories 
            WHERE category_id = %s AND is_active = true
        """
        return Database.execute_query(query, (category_id,), fetch_one=True)
    
    @staticmethod
    def create(category_name, description=None):
        """Create a new category"""
        query = """
            INSERT INTO concern_categories (category_name, description, is_active)
            VALUES (%s, %s, true)
            RETURNING category_id, category_name, description, created_at
        """
        return Database.execute_query(query, (category_name, description), fetch_one=True)
    
    @staticmethod
    def update(category_id, category_name, description=None):
        """Update a category"""
        query = """
            UPDATE concern_categories
            SET category_name = %s, description = %s
            WHERE category_id = %s AND is_active = true
            RETURNING category_id
        """
        result = Database.execute_query(query, (category_name, description, category_id), fetch_one=True)
        return result is not None
    
    @staticmethod
    def delete(category_id):
        """Soft delete a category (mark as inactive)"""
        # Check if category has associated concerns
        check_query = """
            SELECT COUNT(*) as concern_count
            FROM concerns
            WHERE category_id = %s
        """
        result = Database.execute_query(check_query, (category_id,), fetch_one=True)
        
        if result and result['concern_count'] > 0:
            return False  # Cannot delete category with associated concerns
        
        # Soft delete
        query = """
            UPDATE concern_categories
            SET is_active = false
            WHERE category_id = %s
            RETURNING category_id
        """
        result = Database.execute_query(query, (category_id,), fetch_one=True)
        return result is not None

class Office:
    """Office model for database operations"""
    
    @staticmethod
    def get_all():
        """Get all active offices"""
        query = """
            SELECT office_id, office_name, description, contact_email, contact_number
            FROM offices
            WHERE is_active = true
            ORDER BY office_name
        """
        return Database.execute_query(query, fetch_all=True)
    
    @staticmethod
    def find_by_id(office_id):
        """Find office by ID"""
        query = """
            SELECT * FROM offices 
            WHERE office_id = %s AND is_active = true
        """
        return Database.execute_query(query, (office_id,), fetch_one=True)

class Notification:
    """Notification model for database operations"""
    
    @staticmethod
    def create(user_id, concern_id, notification_type, title, message):
        """Create a new notification"""
        query = """
            INSERT INTO notifications 
            (user_id, concern_id, notification_type, title, message)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING notification_id, created_at
        """
        return Database.execute_query(query, 
                                     (user_id, concern_id, notification_type, title, message),
                                     fetch_one=True)
    
    @staticmethod
    def get_by_user(user_id, unread_only=False):
        """Get notifications for a user"""
        query = """
            SELECT n.*, c.ticket_number
            FROM notifications n
            LEFT JOIN concerns c ON n.concern_id = c.concern_id
            WHERE n.user_id = %s
        """
        
        if unread_only:
            query += " AND n.is_read = false"
        
        query += " ORDER BY n.created_at DESC LIMIT 50"
        
        return Database.execute_query(query, (user_id,), fetch_all=True)
    
    @staticmethod
    def mark_as_read(notification_id):
        """Mark notification as read"""
        query = """
            UPDATE notifications 
            SET is_read = true, read_at = CURRENT_TIMESTAMP
            WHERE notification_id = %s
        """
        Database.execute_query(query, (notification_id,))
        return True
    
    @staticmethod
    def mark_all_as_read(user_id):
        """Mark all notifications as read for a user"""
        query = """
            UPDATE notifications 
            SET is_read = true, read_at = CURRENT_TIMESTAMP
            WHERE user_id = %s AND is_read = false
        """
        Database.execute_query(query, (user_id,))
        return True
