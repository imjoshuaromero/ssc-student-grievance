import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template
from flask_cors import CORS
from backend.config.config import config
from backend.routes.auth_routes import auth_bp
from backend.routes.concern_routes import concern_bp
from backend.routes.user_routes import user_bp
from backend.utils.email_service import init_mail

def create_app(config_name='default'):
    """Application factory pattern"""
    # Set template and static folders to frontend directory
    app = Flask(__name__, 
                template_folder='../frontend/templates',
                static_folder='../frontend/static')
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",  # Allow all origins in development
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "max_age": 3600
        }
    })
    
    # Initialize Flask-Mail
    init_mail(app)
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(concern_bp, url_prefix='/api/concerns')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    
    # Health check route
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Grievance System API is running'}, 200
    
    # Frontend routes
    @app.route('/')
    @app.route('/login')
    def login():
        return render_template('login.html')
    
    @app.route('/register')
    def register():
        return render_template('register.html')
    
    @app.route('/verify-email')
    def verify_email_page():
        return render_template('verify-email.html')
    
    @app.route('/student-dashboard')
    def student_dashboard():
        return render_template('student-dashboard.html')
    
    @app.route('/admin-dashboard')
    def admin_dashboard():
        return render_template('admin-dashboard.html')
    
    return app

if __name__ == '__main__':
    # Run the application
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    port = int(os.getenv('PORT', 5000))
    app.run(debug=(config_name == 'development'), host='0.0.0.0', port=port)

# For production servers (gunicorn)
app = create_app(os.getenv('FLASK_ENV', 'production'))
