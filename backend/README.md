# Student Grievance Reporting System - Backend

Complete Flask REST API for the Student Grievance Reporting and Tracking System.

## Setup Instructions

### 1. Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies (if not already installed)

```powershell
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Edit `.env` file and set your PostgreSQL password:

```
DB_PASSWORD=your_actual_postgres_password
```

### 4. Run the Application

```powershell
python backend/app.py
```

The API will be available at: `http://localhost:5000`

## API Endpoints

### Authentication (`/api/auth`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/register` | Register new student | Public |
| POST | `/login` | Login user | Public |
| GET | `/verify` | Verify token | Protected |

### Concerns (`/api/concerns`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/` | Create concern | Student |
| GET | `/` | Get concerns | Protected |
| GET | `/<id>` | Get concern details | Protected |
| PATCH | `/<id>/status` | Update status | Admin |
| PATCH | `/<id>/assign` | Assign to office | Admin |
| PATCH | `/<id>/resolve` | Resolve concern | Admin |
| POST | `/<id>/comments` | Add comment | Protected |
| GET | `/categories` | Get categories | Public |
| GET | `/offices` | Get offices | Protected |
| GET | `/statistics` | Get statistics | Admin |

### Users (`/api/users`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/profile` | Get profile | Protected |
| PUT | `/profile` | Update profile | Protected |
| GET | `/notifications` | Get notifications | Protected |
| PATCH | `/notifications/<id>/read` | Mark as read | Protected |
| PATCH | `/notifications/read-all` | Mark all as read | Protected |
| GET | `/students` | Get all students | Admin |
| GET | `/admins` | Get all admins | Admin |

## Testing the API

### 1. Health Check

```powershell
curl http://localhost:5000/api/health
```

### 2. Register a Student

```powershell
curl -X POST http://localhost:5000/api/auth/register `
  -H "Content-Type: application/json" `
  -d '{
    "sr_code": "21-12345",
    "email": "juan@g.batstate-u.edu.ph",
    "password": "password123",
    "first_name": "Juan",
    "last_name": "Dela Cruz",
    "program": "BSCS",
    "year_level": 3
  }'
```

### 3. Login

```powershell
curl -X POST http://localhost:5000/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{
    "email": "juan@g.batstate-u.edu.ph",
    "password": "password123"
  }'
```

### 4. Create a Concern (use token from login)

```powershell
curl -X POST http://localhost:5000/api/concerns/ `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer YOUR_TOKEN_HERE" `
  -d '{
    "category_id": 3,
    "title": "Broken AC in Room 401",
    "description": "The AC has been broken for 2 weeks",
    "location": "Room 401",
    "priority": "high"
  }'
```

## Project Structure

```
backend/
├── config/
│   ├── config.py           # Application configuration
│   └── database.py         # Database connection
├── models/
│   ├── user.py            # User model
│   ├── concern.py         # Concern model
│   └── category.py        # Category, Office, Notification models
├── routes/
│   ├── auth_routes.py     # Authentication endpoints
│   ├── concern_routes.py  # Concern management endpoints
│   └── user_routes.py     # User management endpoints
├── utils/
│   └── auth.py            # Authentication utilities
└── app.py                 # Main application file
```

## Features

✅ **Authentication & Authorization**
- JWT-based authentication
- Role-based access control (Student/Admin)
- Password hashing with bcrypt
- SR-Code validation

✅ **Concern Management**
- Create, read, update concerns
- Status tracking with history
- Priority levels (low, normal, high, urgent)
- Anonymous reporting option
- Office assignment
- Resolution tracking

✅ **Communication**
- Comment system
- Internal admin notes
- Real-time notifications
- Status change alerts

✅ **Admin Features**
- Dashboard statistics
- Concern assignment
- Status management
- User management
- Complete audit trail

## Security Features

- JWT token authentication
- Password hashing with bcrypt
- Role-based access control
- SQL injection prevention (parameterized queries)
- CORS configuration
- Environment variable protection

## Database

Connects to PostgreSQL database `grievance_system` with the schema defined in `schema.sql`.

## Dependencies

- Flask 3.1.2
- Flask-CORS 6.0.1
- psycopg2-binary 2.9.11
- python-dotenv 1.2.1
- bcrypt 5.0.0
- PyJWT 2.10.1
- Werkzeug 3.1.3
