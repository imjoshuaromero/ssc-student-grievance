from backend.config.database import Database

class User:
    """User model for database operations"""
    
    @staticmethod
    def create(sr_code, email, password_hash, first_name, last_name, middle_name=None, 
               program=None, year_level=None, role='student', google_id=None):
        """Create a new user"""
        query = """
            INSERT INTO users (sr_code, email, password_hash, first_name, last_name, 
                             middle_name, program, year_level, role, google_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING user_id, sr_code, email, first_name, last_name, role, created_at
        """
        params = (sr_code, email, password_hash, first_name, last_name, 
                 middle_name, program, year_level, role, google_id)
        return Database.execute_query(query, params, fetch_one=True)
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        query = "SELECT * FROM users WHERE email = %s AND is_active = true"
        return Database.execute_query(query, (email,), fetch_one=True)
    
    @staticmethod
    def find_by_google_id(google_id):
        """Find user by Google ID"""
        query = "SELECT * FROM users WHERE google_id = %s AND is_active = true"
        return Database.execute_query(query, (google_id,), fetch_one=True)
    
    @staticmethod
    def find_by_sr_code(sr_code):
        """Find user by SR code"""
        query = "SELECT * FROM users WHERE sr_code = %s AND is_active = true"
        return Database.execute_query(query, (sr_code,), fetch_one=True)
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        query = """
            SELECT user_id, sr_code, email, first_name, last_name, middle_name,
                   program, year_level, role, is_active, created_at
            FROM users WHERE user_id = %s
        """
        return Database.execute_query(query, (user_id,), fetch_one=True)
    
    @staticmethod
    def get_all_students():
        """Get all student users"""
        query = """
            SELECT user_id, sr_code, email, first_name, last_name, middle_name,
                   program, year_level, created_at
            FROM users 
            WHERE role = 'student' AND is_active = true
            ORDER BY last_name, first_name
        """
        return Database.execute_query(query, fetch_all=True)
    
    @staticmethod
    def get_all_admins():
        """Get all admin users"""
        query = """
            SELECT user_id, sr_code, email, first_name, last_name, created_at
            FROM users 
            WHERE role = 'admin' AND is_active = true
            ORDER BY last_name, first_name
        """
        return Database.execute_query(query, fetch_all=True)
    
    @staticmethod
    def update_profile(user_id, first_name, last_name, middle_name=None, 
                      program=None, year_level=None):
        """Update user profile"""
        query = """
            UPDATE users 
            SET first_name = %s, last_name = %s, middle_name = %s, 
                program = %s, year_level = %s, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = %s
            RETURNING user_id, sr_code, email, first_name, last_name, 
                     middle_name, program, year_level, role
        """
        params = (first_name, last_name, middle_name, program, year_level, user_id)
        return Database.execute_query(query, params, fetch_one=True)
    
    @staticmethod
    def deactivate(user_id):
        """Deactivate user account"""
        query = "UPDATE users SET is_active = false WHERE user_id = %s"
        Database.execute_query(query, (user_id,))
        return True
    
    @staticmethod
    def delete(user_id):
        """Delete user account (hard delete with CASCADE)"""
        query = "DELETE FROM users WHERE user_id = %s"
        Database.execute_query(query, (user_id,))
        return True
