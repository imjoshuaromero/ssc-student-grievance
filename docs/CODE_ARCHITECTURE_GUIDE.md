# SSC Grievance System — Code Architecture & Backend Deep Dive

**Last Updated:** December 16, 2025  
**Purpose:** Technical guide explaining code structure, routing, backend operations, and how everything connects

---

## Table of Contents
1. [Project Structure Overview](#1-project-structure-overview)
2. [Navigation Guide - Where to Find Everything](#2-navigation-guide---where-to-find-everything)
3. [Application Entry Point & Initialization](#3-application-entry-point--initialization)
4. [Routing System Deep Dive](#4-routing-system-deep-dive)
5. [Backend Architecture Explained](#5-backend-architecture-explained)
6. [Request Flow - From Frontend to Database](#6-request-flow---from-frontend-to-database)
7. [Authentication System Implementation](#7-authentication-system-implementation)
8. [Database Layer & Models](#8-database-layer--models)
9. [Email System Implementation](#9-email-system-implementation)
10. [Frontend-Backend Communication](#10-frontend-backend-communication)
11. [Code Examples - Common Operations](#11-code-examples---common-operations)
12. [Error Handling & Debugging](#12-error-handling--debugging)

---

## 1. Project Structure Overview

```
ssc-student-grievance/
│
├── backend/                    # Backend application code
│   ├── __init__.py
│   ├── app.py                 # 🎯 Main application entry point
│   │
│   ├── config/                # Configuration modules
│   │   ├── __init__.py
│   │   ├── config.py          # 🔧 Environment variables & settings
│   │   └── database.py        # 🗄️ Database connection manager
│   │
│   ├── models/                # Database models (data layer)
│   │   ├── __init__.py
│   │   ├── user.py            # 👤 User CRUD operations
│   │   ├── concern.py         # 📝 Concern CRUD operations
│   │   └── category.py        # 📂 Categories, Offices, Notifications
│   │
│   ├── routes/                # API endpoints (controllers)
│   │   ├── __init__.py
│   │   ├── auth_routes.py     # 🔐 Authentication endpoints
│   │   ├── concern_routes.py  # 📋 Concern management endpoints
│   │   └── user_routes.py     # 👥 User profile endpoints
│   │
│   └── utils/                 # Helper utilities
│       ├── __init__.py
│       ├── auth.py            # 🔑 JWT & password hashing
│       ├── email_service.py   # 📧 Email sending
│       ├── email_verification.py  # ✅ Email verification
│       └── google_auth.py     # 🔗 Google OAuth
│
├── frontend/                  # Frontend templates & static files
│   ├── templates/             # HTML Jinja templates
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── student-dashboard.html
│   │   └── admin-dashboard.html
│   │
│   └── static/                # CSS, JS, images
│       ├── css/
│       │   └── styles.css
│       ├── js/
│       │   └── auth.js        # 🌐 Frontend API calls
│       └── images/
│
├── db/                        # Database files
│   ├── schema.sql             # 📊 Database schema
│   ├── seed_students.sql      # 🌱 Sample data
│   └── create_admin.py        # 👨‍💼 Admin creation script
│
├── uploads/                   # File upload storage
├── .env                       # 🔒 Environment variables (not in git)
├── requirements.txt           # 📦 Python dependencies
├── wsgi.py                    # 🚀 WSGI entry point
└── README.md                  # 📖 Project documentation
```

---

## 2. Navigation Guide - Where to Find Everything

### 2.1 Want to Understand Application Startup?
**Go to:** `backend/app.py`
- Line 8-12: Import blueprints and utilities
- Line 14-21: `create_app()` function - app factory pattern
- Line 27-38: CORS configuration
- Line 41: Flask-Mail initialization
- Line 47-49: Blueprint registration
- Line 78-81: Development server startup

### 2.2 Want to See User Registration?
**Go to:** `backend/routes/auth_routes.py`
- Line 28-115: `register()` function
  - Line 33-36: Validation of required fields
  - Line 39-40: SR-Code format validation
  - Line 43-44: Email format validation
  - Line 48-54: Year level validation
  - Line 57-62: Check for existing user
  - Line 65: Password hashing
  - Line 68-76: User creation
  - Line 80-86: Verification code generation
  - Line 90: Send verification email

### 2.3 Want to See Login Process?
**Go to:** `backend/routes/auth_routes.py`
- Line 117-171: `login()` function
  - Line 123-124: Input validation
  - Line 127: Find user by email
  - Line 133: Password verification
  - Line 137-142: Email verification check
  - Line 145: Generate JWT token

### 2.4 Want to See Concern Creation?
**Go to:** `backend/routes/concern_routes.py`
- Line 23-97: `create_concern()` function
  - Line 26-27: Role check (only students)
  - Line 30-35: Handle JSON/FormData
  - Line 38-41: Validate required fields
  - Line 44-46: Validate category
  - Line 49-59: File upload handling
  - Line 62-64: Anonymous flag conversion
  - Line 67-79: Create concern in DB
  - Line 82: Send creation email

### 2.5 Want to See Database Queries?
**Go to:** `backend/models/user.py` or `backend/models/concern.py`
- User model: CRUD operations for users table
- Concern model: CRUD operations for concerns table

### 2.6 Want to See Authentication Logic?
**Go to:** `backend/utils/auth.py`
- Line 8-11: `hash_password()` - bcrypt hashing
- Line 13-15: `verify_password()` - password checking
- Line 17-24: `generate_token()` - JWT creation
- Line 26-32: `decode_token()` - JWT verification
- Line 34-52: `token_required` - decorator for protected routes
- Line 54-62: `admin_required` - decorator for admin-only routes

### 2.7 Want to See Email Sending?
**Go to:** `backend/utils/email_service.py`
- Line 8-10: `init_mail()` - Initialize Flask-Mail
- Line 12-49: `send_email()` - Core email function with retry
- Line 51-88: `send_concern_created_email()` - Concern notification
- Line 90-135: `send_status_update_email()` - Status change notification

### 2.8 Want to See Frontend API Calls?
**Go to:** `frontend/static/js/auth.js`
- Line 3: API base URL configuration
- Line 80-113: `initLoginForm()` - Login submission
- Line 115-193: `initRegisterForm()` - Registration submission

---

## 3. Application Entry Point & Initialization

### 3.1 Main Application File (`backend/app.py`)

```python
# Lines 1-12: Imports and path setup
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template
from flask_cors import CORS
from backend.config.config import config
from backend.routes.auth_routes import auth_bp
from backend.routes.concern_routes import concern_bp
from backend.routes.user_routes import user_bp
from backend.utils.email_service import init_mail
```

**Why path manipulation?** The `sys.path.insert(0, ...)` ensures Python can find the `backend` package from any working directory.

```python
# Lines 14-21: Application Factory Pattern
def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__, 
                template_folder='../frontend/templates',
                static_folder='../frontend/static')
    app.config.from_object(config[config_name])
```

**Why factory pattern?**
- Allows creating multiple app instances (testing, production)
- Configuration can be passed as parameter
- Makes testing easier

**Template & Static folders:** Points Flask to frontend directory so it can serve HTML and static files.

```python
# Lines 24-38: CORS Configuration
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "max_age": 3600
    }
})
```

**What this does:**
- Allows frontend (different port in dev) to call backend APIs
- `r"/api/*"` - Only applies to API routes
- `origins: "*"` - Allow all origins (restrict in production!)
- `allow_headers` - Accept Authorization header (for JWT)

```python
# Lines 41: Initialize Extensions
init_mail(app)
```

**Email initialization:** Configures Flask-Mail with SMTP settings from `config.py`.

```python
# Lines 44: Create Upload Directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
```

**File uploads:** Creates `uploads/` folder if it doesn't exist.

```python
# Lines 47-49: Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(concern_bp, url_prefix='/api/concerns')
app.register_blueprint(user_bp, url_prefix='/api/users')
```

**Blueprint registration:**
- `auth_bp` → All routes start with `/api/auth`
- `concern_bp` → All routes start with `/api/concerns`
- `user_bp` → All routes start with `/api/users`

```python
# Lines 52-54: Health Check
@app.route('/api/health')
def health_check():
    return {'status': 'healthy', 'message': 'Grievance System API is running'}, 200
```

**Purpose:** Quick endpoint to test if API is running.

```python
# Lines 57-73: Frontend Routes
@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/student-dashboard')
def student_dashboard():
    return render_template('student-dashboard.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    return render_template('admin-dashboard.html')
```

**Frontend routes:** These serve the HTML pages. No authentication here - auth is checked in JavaScript.

---

## 4. Routing System Deep Dive

### 4.1 What is a Blueprint?

A Blueprint is Flask's way of organizing routes into modules. Think of it like a mini-application.

**Example from `auth_routes.py`:**
```python
from flask import Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    # Registration logic
    pass
```

When registered with `url_prefix='/api/auth'`:
- Route becomes: `/api/auth/register`
- Full URL: `http://localhost:5000/api/auth/register`

### 4.2 Complete Route Map

#### Authentication Routes (`/api/auth/*`)
```
POST   /api/auth/register              → Register new user
POST   /api/auth/login                 → Login user
POST   /api/auth/verify                → Verify email code
POST   /api/auth/resend-verification   → Resend verification code
GET    /api/auth/google                → Get Google OAuth URL
GET    /api/auth/google/callback       → Google OAuth callback
```

#### Concern Routes (`/api/concerns/*`)
```
POST   /api/concerns/                  → Create concern (student)
GET    /api/concerns/                  → List concerns (filtered by role)
GET    /api/concerns/:id               → Get concern details
PATCH  /api/concerns/:id/status        → Update status (admin)
POST   /api/concerns/:id/assign        → Assign concern (admin)
POST   /api/concerns/:id/comments      → Add comment
GET    /api/concerns/:id/comments      → Get comments
GET    /api/concerns/:id/history       → Get status history
GET    /api/concerns/:id/attachments   → Get attachments
```

#### User Routes (`/api/users/*`)
```
GET    /api/users/profile              → Get current user profile
PUT    /api/users/profile              → Update profile
GET    /api/users/notifications        → Get notifications
PATCH  /api/users/notifications/:id/read  → Mark notification as read
GET    /api/users/students (admin)     → List all students
GET    /api/users/admins (admin)       → List all admins
```

### 4.3 Route Protection

**Unprotected routes** (anyone can access):
- `/api/auth/register`
- `/api/auth/login`
- `/api/auth/google`
- `/api/auth/google/callback`

**Protected routes** (requires JWT):
- All concern routes
- All user routes

**Admin-only routes:**
- `PATCH /api/concerns/:id/status`
- `POST /api/concerns/:id/assign`
- `GET /api/users/students`
- `GET /api/users/admins`

### 4.4 How Route Protection Works

```python
# From backend/utils/auth.py
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Extract token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # Decode and validate token
        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        # Add user info to request context
        request.user_id = payload['user_id']
        request.user_role = payload['role']
        
        return f(*args, **kwargs)
    
    return decorated
```

**Usage in routes:**
```python
@concern_bp.route('/', methods=['POST'])
@token_required  # ← This decorator runs first
def create_concern():
    # request.user_id is now available
    # request.user_role is now available
    pass
```

---

## 5. Backend Architecture Explained

### 5.1 Layered Architecture

```
┌──────────────────────────────────────┐
│  Frontend (HTML/JS)                  │
│  - Makes HTTP requests               │
└────────────┬─────────────────────────┘
             │ HTTP Request (JSON)
             ↓
┌──────────────────────────────────────┐
│  Routes Layer (Controllers)          │
│  - Validate input                    │
│  - Check permissions                 │
│  - Call models                       │
│  - Return JSON response              │
└────────────┬─────────────────────────┘
             │ Function calls
             ↓
┌──────────────────────────────────────┐
│  Models Layer (Data Access)          │
│  - SQL queries                       │
│  - Data transformation               │
│  - Business logic                    │
└────────────┬─────────────────────────┘
             │ SQL queries
             ↓
┌──────────────────────────────────────┐
│  Database Layer                      │
│  - Connection management             │
│  - Query execution                   │
│  - Transaction handling              │
└────────────┬─────────────────────────┘
             │ PostgreSQL protocol
             ↓
┌──────────────────────────────────────┐
│  PostgreSQL Database                 │
│  - Tables, triggers, constraints     │
└──────────────────────────────────────┘
```

### 5.2 Configuration Layer (`backend/config/`)

#### `config.py` - Environment Variables

```python
class Config:
    # Database credentials
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'grievance_system')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # JWT settings
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    
    # Email settings
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
```

**How it works:**
1. Loads from `.env` file using `dotenv`
2. Falls back to defaults if env variable not set
3. Different config classes for dev/production

#### `database.py` - Connection Manager

```python
class Database:
    @staticmethod
    def get_connection():
        """Get database connection"""
        try:
            # Support DATABASE_URL for cloud deployment
            database_url = os.getenv('DATABASE_URL')
            
            if database_url:
                conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
            else:
                # Local development - individual variables
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
```

**Key points:**
- Uses `RealDictCursor` - returns rows as dictionaries instead of tuples
- Supports both `DATABASE_URL` (cloud) and individual variables (local)
- Raises exception if connection fails

```python
    @staticmethod
    def execute_query(query, params=None, fetch_one=False, fetch_all=False):
        """Execute a query and return results"""
        conn = None
        cursor = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(query, params)
            
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
                if result is None:
                    result = []
            else:
                result = None
            
            conn.commit()  # Auto-commit every query
            return result
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Query error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
```

**What this does:**
- Opens connection
- Executes query with parameters (prevents SQL injection)
- Fetches results if requested
- Commits transaction
- Handles errors with rollback
- **Always closes connection** (important!)

---

## 6. Request Flow - From Frontend to Database

Let's trace a complete request: **Student creates a concern**

### Step 1: Frontend Makes Request (`frontend/static/js/auth.js` or similar)

```javascript
const response = await fetch(`${API_BASE_URL}/concerns`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`  // JWT from localStorage
    },
    body: JSON.stringify({
        category_id: 1,
        title: 'Broken AC',
        description: 'AC in Room 301 not working',
        location: 'Room 301',
        priority: 'high'
    })
});
```

### Step 2: Flask Routes Request (`backend/app.py`)

Flask receives the request and routes it:
- URL: `/api/concerns/`
- Method: `POST`
- Matches: `concern_bp` with prefix `/api/concerns`
- Calls: Route handler in `concern_routes.py`

### Step 3: Decorator Runs First (`backend/utils/auth.py`)

```python
@concern_bp.route('/', methods=['POST'])
@token_required  # ← This runs BEFORE create_concern()
def create_concern():
    pass
```

**Token validation happens:**
1. Extract `Authorization` header
2. Parse token: `Bearer <token>` → extract `<token>`
3. Decode JWT using `JWT_SECRET_KEY`
4. Verify expiration
5. Set `request.user_id` and `request.user_role`
6. If invalid → return 401, stop here
7. If valid → continue to route handler

### Step 4: Route Handler Validates Input (`backend/routes/concern_routes.py`)

```python
def create_concern():
    # Check role
    if request.user_role != 'student':
        return jsonify({'error': 'Only students can file concerns'}), 403
    
    # Get JSON data
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['category_id', 'title', 'description']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Validate category exists
    category = Category.find_by_id(data['category_id'])
    if not category:
        return jsonify({'error': 'Invalid category'}), 400
```

### Step 5: Model Creates Database Record (`backend/models/concern.py`)

```python
    # Create concern in database
    concern = Concern.create(
        student_id=request.user_id,  # From JWT
        category_id=data['category_id'],
        title=data['title'],
        description=data['description'],
        location=data.get('location'),
        priority=data.get('priority', 'normal'),
        is_anonymous=data.get('is_anonymous', False)
    )
```

**In `Concern.create()` method:**
```python
@staticmethod
def create(student_id, category_id, title, description, ...):
    query = """
        INSERT INTO concerns (student_id, category_id, title, description, 
                            location, priority, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'pending')
        RETURNING concern_id, ticket_number, title, status, created_at
    """
    params = (student_id, category_id, title, description, location, priority)
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
```

### Step 6: Database Trigger Runs (`db/schema.sql`)

**PostgreSQL trigger automatically generates ticket number:**

```sql
CREATE OR REPLACE FUNCTION generate_ticket_number()
RETURNS TRIGGER AS $$
DECLARE
    year_part TEXT;
    max_seq INTEGER;
    seq_number INTEGER;
BEGIN
    IF NEW.ticket_number IS NULL THEN
        year_part := TO_CHAR(NEW.created_at, 'YYYY');
        
        SELECT COALESCE(MAX(CAST(SUBSTRING(ticket_number FROM 'GRV-' || year_part || '-([0-9]+)') AS INTEGER)), 0)
        INTO max_seq
        FROM concerns
        WHERE ticket_number LIKE 'GRV-' || year_part || '-%';
        
        seq_number := max_seq + 1;
        NEW.ticket_number := 'GRV-' || year_part || '-' || LPAD(seq_number::TEXT, 5, '0');
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

**Result:** `ticket_number` is set to something like `GRV-2025-00001`

### Step 7: Email Notification Sent (`backend/routes/concern_routes.py`)

```python
    if concern:
        # Get student info for email
        student = User.find_by_id(request.user_id)
        
        # Send creation email
        if not data.get('is_anonymous'):
            send_concern_created_email(
                student['email'],
                f"{student['first_name']} {student['last_name']}",
                concern['ticket_number'],
                concern['title']
            )
```

**In `email_service.py`:**
```python
def send_concern_created_email(student_email, student_name, ticket_number, title):
    subject = f"Concern Received - {ticket_number}"
    
    body_html = f"""
    <html>
    <body>
        <h2>Concern Received</h2>
        <p>Dear {student_name},</p>
        <p>Your concern has been successfully received.</p>
        <p><strong>Ticket:</strong> {ticket_number}</p>
        <p><strong>Title:</strong> {title}</p>
    </body>
    </html>
    """
    
    return send_email(student_email, subject, body_html, body_html)
```

### Step 8: Response Returned to Frontend

```python
        return jsonify({
            'message': 'Concern created successfully',
            'concern': {
                'concern_id': concern['concern_id'],
                'ticket_number': concern['ticket_number'],
                'title': concern['title'],
                'status': concern['status'],
                'created_at': concern['created_at']
            }
        }), 201
```

### Step 9: Frontend Receives Response

```javascript
if (response.ok) {
    const data = await response.json();
    console.log('Concern created:', data.concern);
    // Show success message
    // Redirect to dashboard
}
```

**Complete flow visualization:**

```
Frontend JS
    │
    ├─ POST /api/concerns with JWT token
    │
    ↓
Flask Router
    │
    ├─ Routes to concern_bp
    │
    ↓
@token_required Decorator
    │
    ├─ Validates JWT
    ├─ Sets request.user_id
    │
    ↓
Route Handler (create_concern)
    │
    ├─ Validates input
    ├─ Checks permissions
    │
    ↓
Concern Model
    │
    ├─ Builds SQL query
    ├─ Calls Database.execute_query()
    │
    ↓
Database Layer
    │
    ├─ Opens connection
    ├─ Executes INSERT
    │
    ↓
PostgreSQL
    │
    ├─ Trigger generates ticket_number
    ├─ Returns inserted row
    │
    ↓
Model adds status history
    │
    ↓
Email Service
    │
    ├─ Sends notification email
    │
    ↓
Route Handler returns JSON
    │
    ↓
Frontend receives response
```

---

## 7. Authentication System Implementation

### 7.1 Password Hashing with bcrypt

**Registration - Hash password:**
```python
from backend.utils.auth import hash_password

def hash_password(password):
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()  # Generate random salt
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
```

**What happens:**
1. User enters: `"mypassword123"`
2. bcrypt generates random salt
3. Combines password + salt
4. Hashes with bcrypt algorithm (multiple rounds)
5. Result: `$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEg9KW`
6. Store this in database

**Login - Verify password:**
```python
def verify_password(password, hashed_password):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
```

**What happens:**
1. User enters: `"mypassword123"`
2. Get stored hash from database
3. bcrypt extracts salt from hash
4. Hashes input with same salt
5. Compares hashes
6. Returns `True` or `False`

**Why bcrypt?**
- Slow by design (prevents brute force)
- Automatic salt generation
- Resistant to rainbow table attacks

### 7.2 JWT Token Generation

**After successful login:**
```python
import jwt
import datetime

def generate_token(user_id, role):
    """Generate JWT token"""
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600),  # 1 hour
        'iat': datetime.datetime.utcnow()  # Issued at
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
```

**Example token payload:**
```json
{
    "user_id": 123,
    "role": "student",
    "exp": 1734359999,
    "iat": 1734356399
}
```

**Token encoding:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInJvbGUiOiJzdHVkZW50IiwiZXhwIjoxNzM0MzU5OTk5LCJpYXQiOjE3MzQzNTYzOTl9.dQw4w9WgXcQ
│                                      │                                                                              │
└─────────────────┬──────────────────┘└──────────────────────────┬──────────────────────────────────────────────────┘└──────┬─────────┘
              Header                                         Payload (base64)                                        Signature
```

**Decoding token:**
```python
def decode_token(token):
    """Decode JWT token"""
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
```

### 7.3 Protected Route Flow

```python
# 1. Frontend sends request
fetch('/api/concerns', {
    headers: {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
    }
})

# 2. Backend receives request
@concern_bp.route('/', methods=['GET'])
@token_required  # ← Decorator intercepts
def get_concerns():
    # If we reach here, token is valid
    user_id = request.user_id  # Available from decorator
    role = request.user_role   # Available from decorator
```

**Decorator implementation:**
```python
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # 1. Extract token from header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            token = auth_header.split(' ')[1]  # "Bearer <token>"
        except IndexError:
            return jsonify({'error': 'Invalid token format'}), 401
        
        # 2. Decode and validate
        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        # 3. Add user info to request
        request.user_id = payload['user_id']
        request.user_role = payload['role']
        
        # 4. Call original function
        return f(*args, **kwargs)
    
    return decorated
```

### 7.4 Email Verification Flow

**1. Registration generates code:**
```python
from backend.utils.email_verification import generate_verification_code

def generate_verification_code():
    """Generate 6-digit verification code"""
    return ''.join(random.choices('0123456789', k=6))

# In register():
code = generate_verification_code()  # e.g., "483926"
expires = datetime.now() + timedelta(minutes=15)

# Store in database
Database.execute_query(
    """UPDATE users 
       SET verification_code = %s, verification_code_expires = %s 
       WHERE user_id = %s""",
    (code, expires, user['user_id'])
)
```

**2. Email sent with code:**
```python
send_verification_code_email(user['email'], name, code)
```

**3. User submits verification:**
```python
# POST /api/auth/verify
@auth_bp.route('/verify', methods=['POST'])
def verify_email():
    data = request.get_json()
    
    # Find user by email and code
    query = """
        SELECT user_id FROM users 
        WHERE email = %s 
        AND verification_code = %s 
        AND verification_code_expires > CURRENT_TIMESTAMP
    """
    user = Database.execute_query(query, (email, code), fetch_one=True)
    
    if user:
        # Mark as verified
        Database.execute_query(
            """UPDATE users 
               SET email_verified = TRUE, 
                   verification_code = NULL 
               WHERE user_id = %s""",
            (user['user_id'],)
        )
        return jsonify({'message': 'Email verified'}), 200
    
    return jsonify({'error': 'Invalid or expired code'}), 400
```

---

## 8. Database Layer & Models

### 8.1 Model Structure

**All models follow this pattern:**

```python
class ModelName:
    """Model description"""
    
    @staticmethod
    def create(...):
        """Create new record"""
        query = "INSERT INTO table (...) VALUES (...) RETURNING *"
        return Database.execute_query(query, params, fetch_one=True)
    
    @staticmethod
    def find_by_id(id):
        """Find record by ID"""
        query = "SELECT * FROM table WHERE id = %s"
        return Database.execute_query(query, (id,), fetch_one=True)
    
    @staticmethod
    def get_all():
        """Get all records"""
        query = "SELECT * FROM table ORDER BY created_at DESC"
        return Database.execute_query(query, fetch_all=True)
    
    @staticmethod
    def update(...):
        """Update record"""
        query = "UPDATE table SET ... WHERE id = %s RETURNING *"
        return Database.execute_query(query, params, fetch_one=True)
    
    @staticmethod
    def delete(id):
        """Delete or soft-delete record"""
        query = "DELETE FROM table WHERE id = %s"  # or UPDATE is_active = FALSE
        return Database.execute_query(query, (id,))
```

### 8.2 User Model Example (`backend/models/user.py`)

```python
class User:
    @staticmethod
    def create(sr_code, email, password_hash, first_name, last_name, ...):
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
```

**What gets returned:**
```python
{
    'user_id': 123,
    'sr_code': '21-12345',
    'email': 'juan.delacruz@g.batstate-u.edu.ph',
    'first_name': 'Juan',
    'last_name': 'Dela Cruz',
    'role': 'student',
    'created_at': datetime(2025, 12, 16, 10, 30, 0)
}
```

**Find by email:**
```python
@staticmethod
def find_by_email(email):
    """Find user by email"""
    query = "SELECT * FROM users WHERE email = %s AND is_active = true"
    return Database.execute_query(query, (email,), fetch_one=True)
```

**Why `fetch_one=True`?** We expect one user or None.

### 8.3 Concern Model with JOINs

```python
@staticmethod
def find_by_id(concern_id):
    """Get concern by ID with related information"""
    query = """
        SELECT c.*, 
               u.first_name || ' ' || u.last_name AS student_name,
               u.sr_code,
               u.email AS student_email,
               cat.category_name,
               o.office_name,
               admin.first_name || ' ' || admin.last_name AS admin_name
        FROM concerns c
        JOIN users u ON c.student_id = u.user_id
        JOIN concern_categories cat ON c.category_id = cat.category_id
        LEFT JOIN offices o ON c.assigned_office_id = o.office_id
        LEFT JOIN users admin ON c.assigned_admin_id = admin.user_id
        WHERE c.concern_id = %s
    """
    return Database.execute_query(query, (concern_id,), fetch_one=True)
```

**What gets returned:**
```python
{
    'concern_id': 1,
    'ticket_number': 'GRV-2025-00001',
    'student_id': 123,
    'student_name': 'Juan Dela Cruz',
    'sr_code': '21-12345',
    'student_email': 'juan.delacruz@g.batstate-u.edu.ph',
    'category_id': 3,
    'category_name': 'Services & Facilities',
    'office_id': 4,
    'office_name': 'Facility Management',
    'admin_name': 'Admin User',
    'title': 'Broken AC',
    'description': 'AC not working...',
    'status': 'in-progress',
    'priority': 'high',
    'created_at': datetime(...)
}
```

**Why LEFT JOIN?** `assigned_office_id` and `assigned_admin_id` can be NULL initially.

### 8.4 Status History Tracking

```python
@staticmethod
def add_status_history(concern_id, old_status, new_status, changed_by, remarks=None):
    """Add entry to status history"""
    query = """
        INSERT INTO concern_status_history (concern_id, old_status, new_status, changed_by, remarks)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING history_id, created_at
    """
    return Database.execute_query(
        query, 
        (concern_id, old_status, new_status, changed_by, remarks), 
        fetch_one=True
    )
```

**Called automatically:**
1. When concern is created (old_status = NULL, new_status = 'pending')
2. When status is updated by admin

**Get history:**
```python
@staticmethod
def get_status_history(concern_id):
    """Get status change history"""
    query = """
        SELECT h.*, 
               u.first_name || ' ' || u.last_name AS changed_by_name
        FROM concern_status_history h
        JOIN users u ON h.changed_by = u.user_id
        WHERE h.concern_id = %s
        ORDER BY h.created_at ASC
    """
    return Database.execute_query(query, (concern_id,), fetch_all=True)
```

---

## 9. Email System Implementation

### 9.1 Flask-Mail Configuration

**Initialize in `app.py`:**
```python
from backend.utils.email_service import init_mail

def create_app(config_name='default'):
    app = Flask(__name__)
    # ...config...
    init_mail(app)  # Initialize Flask-Mail
```

**In `email_service.py`:**
```python
from flask_mail import Mail, Message

mail = Mail()

def init_mail(app):
    """Initialize Flask-Mail with app"""
    mail.init_app(app)
```

**Configuration from `config.py`:**
```python
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'
MAIL_DEFAULT_SENDER = 'your-email@gmail.com'
```

### 9.2 Sending Email with Retry Logic

```python
def send_email(to, subject, body_text, body_html=None, max_retries=3):
    """Send email notification with retry logic"""
    
    for attempt in range(max_retries):
        try:
            msg = Message(
                subject=subject,
                recipients=[to] if isinstance(to, str) else to,
                body=body_text,
                html=body_html or body_text,
                sender=current_app.config.get('MAIL_DEFAULT_SENDER')
            )
            mail.send(msg)
            print(f"✓ Email sent successfully to {to}")
            return True
        except Exception as e:
            print(f"Email attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retry
            else:
                print(f"✗ Failed to send email to {to}")
                return False
```

**Retry logic:**
- Tries 3 times
- Waits 2 seconds between attempts
- Returns `True` if successful, `False` if all attempts fail

### 9.3 Email Templates

**Concern Created Email:**
```python
def send_concern_created_email(student_email, student_name, ticket_number, title):
    """Send email when concern is created"""
    subject = f"Concern Received - {ticket_number}"
    
    body_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #004d99;">Concern Received</h2>
            <p>Dear {student_name},</p>
            <p>Your concern has been successfully received and is being reviewed.</p>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
                <p><strong>Ticket Number:</strong> {ticket_number}</p>
                <p><strong>Title:</strong> {title}</p>
                <p><strong>Status:</strong> Pending</p>
            </div>
            
            <p>You will receive email updates when there are changes to your concern status.</p>
            
            <p style="margin-top: 30px;">Thank you,<br>
            <strong>Supreme Student Council</strong><br>
            BatState-U TNEU Lipa</p>
        </div>
    </body>
    </html>
    """
    
    return send_email(student_email, subject, body_html, body_html)
```

**Status Update Email:**
```python
def send_status_update_email(student_email, student_name, ticket_number, title, old_status, new_status, remarks=None):
    """Send email when concern status is updated"""
    subject = f"Status Update - {ticket_number}"
    
    # Status display mapping
    status_display = {
        'pending': 'Pending Review',
        'in-review': 'Under Review',
        'in-progress': 'In Progress',
        'resolved': 'Resolved',
        'closed': 'Closed'
    }
    
    body_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2>Concern Status Updated</h2>
        <p>Dear {student_name},</p>
        <p>Your concern status has been updated.</p>
        
        <div style="background-color: #f5f5f5; padding: 15px;">
            <p><strong>Ticket:</strong> {ticket_number}</p>
            <p><strong>Title:</strong> {title}</p>
            <p><strong>Previous Status:</strong> {status_display.get(old_status, old_status)}</p>
            <p><strong>New Status:</strong> {status_display.get(new_status, new_status)}</p>
            {f'<p><strong>Remarks:</strong> {remarks}</p>' if remarks else ''}
        </div>
        
        <p>Thank you,<br>Supreme Student Council</p>
    </body>
    </html>
    """
    
    return send_email(student_email, subject, body_html, body_html)
```

### 9.4 When Emails Are Sent

**Registration:**
```python
# backend/routes/auth_routes.py - register()
send_verification_code_email(user['email'], name, code)
```

**Concern Created:**
```python
# backend/routes/concern_routes.py - create_concern()
if not data.get('is_anonymous'):
    send_concern_created_email(student_email, student_name, ticket_number, title)
```

**Status Updated:**
```python
# backend/routes/concern_routes.py - update_status()
send_status_update_email(student_email, student_name, ticket_number, title, old_status, new_status, remarks)
```

**Comment Added:**
```python
# backend/routes/concern_routes.py - add_comment()
send_comment_notification_email(student_email, student_name, ticket_number, title, commenter_name, comment_text)
```

---

## 10. Frontend-Backend Communication

### 10.1 API Base URL Configuration

**Frontend (`frontend/static/js/auth.js`):**
```javascript
// Use same origin to avoid CORS issues
const API_BASE_URL = `${window.location.protocol}//${window.location.host}/api`;
```

**What this does:**
- Development: `http://localhost:5000/api`
- Production: `https://yourdomain.com/api`

### 10.2 Making API Calls

**Login example:**
```javascript
async function login(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Store token
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            
            // Redirect based on role
            if (data.user.role === 'admin') {
                window.location.href = '/admin-dashboard';
            } else {
                window.location.href = '/student-dashboard';
            }
        } else {
            showAlert(data.error, 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showAlert('Failed to connect to server', 'error');
    }
}
```

**Protected API call example:**
```javascript
async function getConcerns() {
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_BASE_URL}/concerns`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`  // Include JWT
            }
        });
        
        if (response.status === 401) {
            // Token expired or invalid
            localStorage.removeItem('token');
            window.location.href = '/login';
            return;
        }
        
        const data = await response.json();
        return data.concerns;
    } catch (error) {
        console.error('Get concerns error:', error);
        return [];
    }
}
```

**File upload example:**
```javascript
async function submitConcernWithFiles(formData) {
    const token = localStorage.getItem('token');
    
    // FormData automatically sets Content-Type: multipart/form-data
    const response = await fetch(`${API_BASE_URL}/concerns`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
            // Don't set Content-Type for FormData
        },
        body: formData  // FormData object, not JSON
    });
    
    return await response.json();
}
```

### 10.3 Token Storage & Retrieval

**After login:**
```javascript
localStorage.setItem('token', data.token);
localStorage.setItem('user', JSON.stringify(data.user));
```

**On page load (dashboard):**
```javascript
const token = localStorage.getItem('token');
const user = JSON.parse(localStorage.getItem('user'));

if (!token) {
    window.location.href = '/login';
}
```

**On logout:**
```javascript
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
}
```

---

## 11. Code Examples - Common Operations

### 11.1 Create a New User

```python
# In backend/routes/auth_routes.py
from backend.models.user import User
from backend.utils.auth import hash_password

# Hash the password
password_hash = hash_password('user_password')

# Create user
user = User.create(
    sr_code='21-12345',
    email='juan@example.com',
    password_hash=password_hash,
    first_name='Juan',
    last_name='Dela Cruz',
    middle_name='Pablo',
    program='BSCS',
    year_level=3,
    role='student'
)

# Returns:
# {
#     'user_id': 123,
#     'sr_code': '21-12345',
#     'email': 'juan@example.com',
#     'first_name': 'Juan',
#     'last_name': 'Dela Cruz',
#     'role': 'student',
#     'created_at': datetime(...)
# }
```

### 11.2 Query Concerns with Filters

```python
# In backend/models/concern.py

@staticmethod
def get_all(status=None, category_id=None, priority=None):
    """Get all concerns with optional filters"""
    query = """
        SELECT c.*, 
               u.first_name || ' ' || u.last_name AS student_name,
               cat.category_name
        FROM concerns c
        JOIN users u ON c.student_id = u.user_id
        JOIN concern_categories cat ON c.category_id = cat.category_id
        WHERE 1=1
    """
    params = []
    
    if status:
        query += " AND c.status = %s"
        params.append(status)
    
    if category_id:
        query += " AND c.category_id = %s"
        params.append(category_id)
    
    if priority:
        query += " AND c.priority = %s"
        params.append(priority)
    
    query += " ORDER BY c.created_at DESC"
    
    return Database.execute_query(query, tuple(params), fetch_all=True)

# Usage:
all_concerns = Concern.get_all()
pending_concerns = Concern.get_all(status='pending')
high_priority = Concern.get_all(priority='high')
pending_academic = Concern.get_all(status='pending', category_id=1)
```

### 11.3 Update Concern Status

```python
# In backend/routes/concern_routes.py

@concern_bp.route('/<int:concern_id>/status', methods=['PATCH'])
@admin_required
def update_status(concern_id):
    data = request.get_json()
    
    # Get current concern
    concern = Concern.find_by_id(concern_id)
    if not concern:
        return jsonify({'error': 'Concern not found'}), 404
    
    old_status = concern['status']
    new_status = data['status']
    remarks = data.get('remarks')
    
    # Update status
    Concern.update_status(concern_id, new_status)
    
    # Add to history
    Concern.add_status_history(
        concern_id, 
        old_status, 
        new_status, 
        request.user_id,  # Admin making the change
        remarks
    )
    
    # Send email notification
    send_status_update_email(
        concern['student_email'],
        concern['student_name'],
        concern['ticket_number'],
        concern['title'],
        old_status,
        new_status,
        remarks
    )
    
    return jsonify({'message': 'Status updated'}), 200
```

### 11.4 Add Comment to Concern

```python
@concern_bp.route('/<int:concern_id>/comments', methods=['POST'])
@token_required
def add_comment(concern_id):
    data = request.get_json()
    
    # Validate
    if not data.get('comment_text'):
        return jsonify({'error': 'Comment text is required'}), 400
    
    # Add comment
    comment = {
        'concern_id': concern_id,
        'user_id': request.user_id,
        'comment_text': data['comment_text'],
        'is_internal': data.get('is_internal', False)
    }
    
    query = """
        INSERT INTO comments (concern_id, user_id, comment_text, is_internal)
        VALUES (%s, %s, %s, %s)
        RETURNING comment_id, created_at
    """
    result = Database.execute_query(
        query, 
        (concern_id, request.user_id, data['comment_text'], data.get('is_internal', False)),
        fetch_one=True
    )
    
    # Send notification (if not internal)
    if not data.get('is_internal'):
        concern = Concern.find_by_id(concern_id)
        commenter = User.find_by_id(request.user_id)
        
        send_comment_notification_email(
            concern['student_email'],
            concern['student_name'],
            concern['ticket_number'],
            concern['title'],
            f"{commenter['first_name']} {commenter['last_name']}",
            data['comment_text']
        )
    
    return jsonify({
        'message': 'Comment added',
        'comment_id': result['comment_id']
    }), 201
```

---

## 12. Error Handling & Debugging

### 12.1 Common Error Patterns

**Database errors:**
```python
try:
    user = User.find_by_email(email)
except Exception as e:
    print(f"Database error: {e}")
    return jsonify({'error': 'Database connection failed'}), 500
```

**Validation errors:**
```python
if not data.get('email'):
    return jsonify({'error': 'Email is required'}), 400

if not validate_email(data['email']):
    return jsonify({'error': 'Invalid email format'}), 400
```

**Authentication errors:**
```python
if not token:
    return jsonify({'error': 'Token is missing'}), 401

if not verify_password(password, user['password_hash']):
    return jsonify({'error': 'Invalid credentials'}), 401
```

**Permission errors:**
```python
if request.user_role != 'admin':
    return jsonify({'error': 'Admin access required'}), 403
```

### 12.2 Debugging Techniques

**Print statements:**
```python
print(f"User ID: {request.user_id}")
print(f"Request data: {request.get_json()}")
print(f"Query result: {result}")
```

**Check database connection:**
```python
# In Python console or route
from backend.config.database import Database

try:
    conn = Database.get_connection()
    print("✓ Database connected")
    conn.close()
except Exception as e:
    print(f"✗ Database error: {e}")
```

**Test email sending:**
```python
from backend.utils.email_service import send_email

result = send_email(
    'test@example.com',
    'Test Subject',
    'Test body'
)
print(f"Email sent: {result}")
```

**Check JWT token:**
```python
from backend.utils.auth import decode_token

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
payload = decode_token(token)
print(f"Token payload: {payload}")
```

### 12.3 Error Logs

**Check Flask console output:**
- Database connection errors
- Email sending failures
- Print statements
- Exception tracebacks

**Check browser console:**
- API response status codes
- Response JSON data
- JavaScript errors
- Network requests

---

## Summary

This guide covered:
1. ✅ Project structure and where to find code
2. ✅ Complete routing system with URL mapping
3. ✅ Application initialization and configuration
4. ✅ Request flow from frontend to database
5. ✅ Authentication (bcrypt, JWT, decorators)
6. ✅ Database layer and model patterns
7. ✅ Email system implementation
8. ✅ Frontend-backend communication
9. ✅ Code examples for common operations
10. ✅ Error handling and debugging

**Key takeaways:**
- Flask Blueprints organize routes by feature
- Decorators (`@token_required`) protect routes
- Models handle all database operations
- JWT tokens enable stateless authentication
- Email notifications keep users informed
- Request flow: Frontend → Route → Model → Database → Model → Route → Frontend

Good luck with your presentation! 🚀
