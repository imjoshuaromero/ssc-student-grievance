import psycopg2
from psycopg2.extras import RealDictCursor
from backend.config.config import Config
import os

class Database:
    """Database connection manager"""
    
    @staticmethod
    def get_connection():
        """Get database connection"""
        try:
            # Support DATABASE_URL for Render/Heroku deployment
            database_url = os.getenv('DATABASE_URL')
            
            if database_url:
                # Parse DATABASE_URL (format: postgresql://user:pass@host:port/dbname)
                conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
            else:
                # Use individual environment variables (local development)
                conn = psycopg2.connect(
                    host=Config.DB_HOST,
                    port=Config.DB_PORT,
                    database=Config.DB_NAME,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    cursor_factory=RealDictCursor
                )
            return conn
        except psycopg2.Error as e:
            print(f"Database connection error: {e}")
            raise
    
    @staticmethod
    def execute_query(query, params=None, fetch_one=False, fetch_all=False):
        """Execute a query and return results"""
        conn = None
        cursor = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            # Handle empty tuple for params
            if params == ():
                cursor.execute(query)
            else:
                cursor.execute(query, params)
            
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
                # Return empty list instead of None if no results
                if result is None:
                    result = []
            else:
                result = None
            
            conn.commit()
            return result
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            print(f"Query execution error: {e}")
            print(f"Query: {query}")
            print(f"Params: {params}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
