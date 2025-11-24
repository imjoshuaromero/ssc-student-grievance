# 🎓 Student Grievance Reporting System - Backend API

## Overview

A modern web-based grievance reporting and tracking system for BatState-U TNEU Lipa Supreme Student Council with **Google OAuth** authentication and **email notifications**.

### ✨ Key Web Features

- ✅ **Google Sign-In** - OAuth 2.0 authentication
- ✅ **Email Notifications** - Automated updates via Gmail SMTP
- ✅ **RESTful API** - Clean, documented endpoints
- ✅ **JWT Authentication** - Secure token-based auth
- ✅ **Role-Based Access** - Student and Admin roles
- ✅ **File Upload Support** - Images, PDFs, documents
- ✅ **Real-time Updates** - Status tracking and history

---

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 16+
- Gmail account (for email notifications)
- Google Cloud Console account (for OAuth)

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install Flask Flask-CORS psycopg2-binary python-dotenv bcrypt PyJWT Werkzeug google-auth google-auth-oauthlib google-auth-httplib2 Flask-Mail Pillow
```

### 2. Setup Database

```sql
-- Run in PostgreSQL
CREATE DATABASE grievance_system;
\c grievance_system
\i db/schema.sql
```

### 3. Configure Environment

Copy `.env.example` to `.env` and fill in:

```env
# Database
DB_PASSWORD=your_postgresql_password

# Google OAuth (get from Google Cloud Console)
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here

# Gmail SMTP (get app password from Google Account)
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_16_character_app_password
```

### 4. Run Server

```bash
python backend/app.py
```

Server starts at: `http://localhost:5000`

---

## 🔐 Authentication Endpoints

### Traditional Auth

#### Register
```http
POST /api/auth/register
Content-Type: application/json

{
  "sr_code": "24-12345",
  "email": "student@batstateu.edu.ph",
  "password": "SecurePassword123",
  "first_name": "Juan",
  "last_name": "Dela Cruz",
  "program": "BS Computer Science",
  "year_level": 3
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "student@batstateu.edu.ph",
  "password": "SecurePassword123"
}
```

### Google OAuth

#### Step 1: Get Auth URL
```http
GET /api/auth/google
```

Response:
```json
{
  "auth_url": "https://accounts.google.com/o/oauth2/v2/auth?..."
}
```

#### Step 2: Handle Callback (Automatic)
```http
GET /api/auth/google/callback?code=...
```

#### Step 3: Complete Registration (New Users)
```http
POST /api/auth/google/register
Content-Type: application/json

{
  "google_id": "1234567890",
  "email": "student@batstateu.edu.ph",
  "sr_code": "24-12345",
  "first_name": "Juan",
  "last_name": "Dela Cruz",
  "program": "BS Computer Science",
  "year_level": 3
}
```

---

## 📝 Concern Endpoints

### Create Concern
```http
POST /api/concerns/
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "category_id": 1,
  "title": "Damaged Equipment",
  "description": "Computers in Lab 203 not working",
  "location": "Computer Lab 203",
  "priority": "high"
}
```

**✉️ Sends email:** "Concern Received" to student

### Update Status (Admin)
```http
PATCH /api/concerns/{concern_id}/status
Authorization: Bearer {admin_jwt_token}
Content-Type: application/json

{
  "status": "in-progress",
  "remarks": "Investigating the issue"
}
```

**✉️ Sends email:** "Status Updated" to student

### Resolve Concern (Admin)
```http
PATCH /api/concerns/{concern_id}/resolve
Authorization: Bearer {admin_jwt_token}
Content-Type: application/json

{
  "resolution_notes": "All computers repaired and tested"
}
```

**✉️ Sends email:** "Concern Resolved" to student

---

## 📧 Email Notifications

Automated emails sent for:

1. **Concern Created** - Confirmation with ticket number
2. **Status Updated** - Old status → New status with remarks
3. **Concern Assigned** - Office/department assignment
4. **New Comment** - Comment from admin
5. **Concern Resolved** - Resolution details

---

## 📁 Project Structure

```
backend/
├── app.py                 # Main Flask application
├── config/
│   ├── config.py         # Configuration classes
│   └── database.py       # Database connection
├── models/
│   ├── user.py           # User model (Google OAuth support)
│   ├── concern.py        # Concern model
│   └── category.py       # Category, Office, Notification models
├── routes/
│   ├── auth_routes.py    # Auth endpoints (Google OAuth)
│   ├── concern_routes.py # Concern endpoints (Email notifications)
│   └── user_routes.py    # User endpoints
├── utils/
│   ├── auth.py           # JWT utilities
│   ├── email_service.py  # Email notification service (NEW)
│   └── google_auth.py    # Google OAuth utilities (NEW)
└── README.md
```

---

**Built with ❤️ for BatState-U TNEU Lipa**
