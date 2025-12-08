# 🚀 Student Grievance System - Setup Guide

## Web-Based Features Overview

This is a **modern web-based** Student Grievance Reporting and Tracking System with the following enhancements:

### ✨ Key Features

1. **🔐 Google OAuth Authentication**
   - Sign in with BatState-U Google account
   - No need to remember passwords
   - Secure and convenient

2. **📧 Email Notifications**
   - Receive emails when your grievance is updated
   - Get notified when status changes
   - Email alerts for new comments
   - Resolution notifications

3. **📱 Web-Optimized**
   - Accessible from any device (desktop, tablet, mobile)
   - Modern UI with Tailwind CSS + daisyUI
   - Real-time dashboard with statistics
   - File upload support (images, PDFs)

4. **🔔 Real-time Notifications**
   - In-app notifications
   - Email notifications
   - Track all updates in one place

---

## 📋 Prerequisites

Before starting, make sure you have:

- ✅ PostgreSQL 16 installed
- ✅ Python 3.11.9 installed
- ✅ Node.js (for frontend development later)
- ✅ Gmail account (for email notifications)
- ✅ Google Cloud Console account (for OAuth)

---

## 🛠️ Installation Steps

### 1️⃣ Install Python Dependencies

```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Install all dependencies
pip install Flask Flask-CORS psycopg2-binary python-dotenv bcrypt PyJWT Werkzeug google-auth google-auth-oauthlib google-auth-httplib2 Flask-Mail Pillow
```

### 2️⃣ Setup PostgreSQL Database

Run the updated schema:

```powershell
# Connect to PostgreSQL
psql -U postgres

# Create and use database
CREATE DATABASE grievance_system;
\c grievance_system

# Run the schema file
\i "C:/Users/bakaj/2NDYR IT/CS 121/FINAL PROJECT/db/schema.sql"
```

### 3️⃣ Configure Google OAuth

1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**

2. **Create a New Project**
   - Click "Select a project" → "New Project"
   - Name: "BatState Grievance System"
   - Click "Create"

3. **Enable Google OAuth**
   - Go to "APIs & Services" → "OAuth consent screen"
   - Select "External" → Click "Create"
   - Fill in:
     - App name: `BatState Grievance System`
     - User support email: Your email
     - Developer contact: Your email
   - Click "Save and Continue"

4. **Create OAuth Credentials**
   - Go to "Credentials" → "Create Credentials" → "OAuth client ID"
   - Application type: "Web application"
   - Name: "Grievance System Web Client"
   - Authorized redirect URIs:
     ```
     http://localhost:5000/api/auth/google/callback
     ```
   - Click "Create"
   - **Save the Client ID and Client Secret** - you'll need these!

### 4️⃣ Configure Gmail for Email Notifications

1. **Enable 2-Step Verification**
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Enable 2-Step Verification

2. **Create App Password**
   - Go to [App Passwords](https://myaccount.google.com/apppasswords)
   - Select app: "Mail"
   - Select device: "Other (Custom name)"
   - Name it: "Grievance System"
   - Click "Generate"
   - **Save the 16-character password** - you'll need this!

### 5️⃣ Update Environment Variables

Edit the `.env` file and fill in your credentials:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=grievance_system
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRESQL_PASSWORD_HERE

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-12345-change-in-production

# JWT Configuration
JWT_SECRET_KEY=jwt-secret-key-67890-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id_from_step3
GOOGLE_CLIENT_SECRET=your_google_client_secret_from_step3
GOOGLE_REDIRECT_URI=http://localhost:5000/api/auth/google/callback

# Email Configuration (Gmail SMTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_gmail@gmail.com
MAIL_PASSWORD=your_16_character_app_password_from_step4
MAIL_DEFAULT_SENDER=your_gmail@gmail.com
MAIL_ADMIN_EMAIL=ssc@batstateu.edu.ph
```

---

## 🚀 Running the Backend

```powershell
# Make sure you're in the project directory
cd "C:\Users\bakaj\2NDYR IT\CS 121\FINAL PROJECT"

# Activate virtual environment
.\venv\Scripts\activate

# Run the Flask app
python backend/app.py
```

The server will start at: `http://localhost:5000`

Test the health check: `http://localhost:5000/api/health`

---

## 📡 API Endpoints

### Authentication

#### Traditional Registration
```http
POST /api/auth/register
Content-Type: application/json

{
  "sr_code": "24-12345",
  "email": "student@batstateu.edu.ph",
  "password": "SecurePassword123",
  "first_name": "Juan",
  "last_name": "Dela Cruz",
  "middle_name": "Santos",
  "program": "BS Computer Science",
  "year_level": 3
}
```

#### Traditional Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "student@batstateu.edu.ph",
  "password": "SecurePassword123"
}
```

#### Google OAuth Sign-In

**Step 1: Get Authorization URL**
```http
GET /api/auth/google
```

Response:
```json
{
  "auth_url": "https://accounts.google.com/o/oauth2/v2/auth?client_id=..."
}
```

**Step 2: User clicks the auth_url and signs in with Google**

**Step 3: Google redirects to callback**
```http
GET /api/auth/google/callback?code=AUTHORIZATION_CODE
```

**If New User:**
```json
{
  "message": "New user detected",
  "google_user": {
    "email": "student@batstateu.edu.ph",
    "first_name": "Juan",
    "last_name": "Dela Cruz",
    "google_id": "1234567890"
  },
  "is_new_user": true,
  "requires_registration": true
}
```

**Step 4: Complete registration for new Google users**
```http
POST /api/auth/google/register
Content-Type: application/json

{
  "google_id": "1234567890",
  "email": "student@batstateu.edu.ph",
  "sr_code": "24-12345",
  "first_name": "Juan",
  "last_name": "Dela Cruz",
  "middle_name": "Santos",
  "program": "BS Computer Science",
  "year_level": 3
}
```

### Concerns (Grievances)

#### Create Concern (with Email Notification)
```http
POST /api/concerns/
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "category_id": 1,
  "title": "Damaged Computer Lab Equipment",
  "description": "Several computers in Lab 203 are not working properly",
  "location": "Computer Lab 203",
  "incident_date": "2024-11-20",
  "priority": "high",
  "is_anonymous": false
}
```

**✉️ Email sent to student:** "Concern Received" with ticket number

#### Update Status (Admin - with Email Notification)
```http
PATCH /api/concerns/1/status
Authorization: Bearer ADMIN_JWT_TOKEN
Content-Type: application/json

{
  "status": "in-progress",
  "remarks": "We are currently investigating this issue"
}
```

**✉️ Email sent to student:** "Status Update" with old status, new status, and remarks

#### Resolve Concern (Admin - with Email Notification)
```http
PATCH /api/concerns/1/resolve
Authorization: Bearer ADMIN_JWT_TOKEN
Content-Type: application/json

{
  "resolution_notes": "All computers have been repaired and tested. Lab is now fully operational."
}
```

**✉️ Email sent to student:** "Concern Resolved" with resolution details

#### Add Comment (with Email Notification)
```http
POST /api/concerns/1/comments
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "comment_text": "Thank you for the quick response!",
  "is_internal": false
}
```

**✉️ Email sent to recipient:** "New Comment" with commenter name and comment text

---

## 📧 Email Notification Types

1. **Concern Created**
   - Sent when: Student submits a new grievance
   - Recipient: Student
   - Contains: Ticket number, title, status

2. **Status Updated**
   - Sent when: Admin changes grievance status
   - Recipient: Student
   - Contains: Ticket number, title, old status, new status, remarks

3. **Concern Assigned**
   - Sent when: Admin assigns grievance to an office
   - Recipient: Student
   - Contains: Ticket number, title, assigned office name

4. **Comment Added**
   - Sent when: Admin adds a comment
   - Recipient: Student
   - Contains: Ticket number, title, commenter name, comment text

5. **Concern Resolved**
   - Sent when: Admin resolves the grievance
   - Recipient: Student
   - Contains: Ticket number, title, resolution notes

---

## 🎨 Frontend Development (Next Steps)

The backend is ready! Now you can build the frontend with:

- **HTML** pages
- **Tailwind CSS** for styling
- **daisyUI** components
- **JavaScript** for API calls

### Recommended Pages:

1. **Landing Page** - Introduction and "Sign in with Google" button
2. **Login/Register** - Traditional auth option
3. **Student Dashboard** - View concerns, create new, notifications
4. **Admin Dashboard** - View all concerns, statistics, manage
5. **Concern Detail** - View full concern with comments and history

---

## 🔍 Testing the Backend

### Test Email Notifications

```powershell
# Test with Python (quick test)
python -c "
from backend.utils.email_service import send_email
send_email('your_email@gmail.com', 'Test Email', 'This is a test from Grievance System')
"
```

### Test Google OAuth Flow

1. Start the server: `python backend/app.py`
2. Visit: `http://localhost:5000/api/auth/google`
3. Copy the `auth_url` from the response
4. Open the URL in your browser
5. Sign in with your Google account
6. Check the callback response

---

## 🐛 Troubleshooting

### Email Not Sending?

- ✅ Check Gmail App Password is correct (16 characters, no spaces)
- ✅ Verify 2-Step Verification is enabled
- ✅ Check MAIL_USERNAME and MAIL_PASSWORD in `.env`
- ✅ Make sure less secure app access is NOT needed (App Passwords work better)

### Google OAuth Not Working?

- ✅ Check GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in `.env`
- ✅ Verify redirect URI matches exactly: `http://localhost:5000/api/auth/google/callback`
- ✅ Check OAuth consent screen is configured
- ✅ Make sure you're using HTTP (not HTTPS) for localhost

### Database Connection Issues?

- ✅ PostgreSQL service is running
- ✅ DB_PASSWORD in `.env` is correct
- ✅ Database `grievance_system` exists
- ✅ Schema has been executed (includes `google_id` column)

---

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google OAuth 2.0 Guide](https://developers.google.com/identity/protocols/oauth2)
- [Flask-Mail Documentation](https://pythonhosted.org/Flask-Mail/)
- [Tailwind CSS](https://tailwindcss.com/)
- [daisyUI Components](https://daisyui.com/)

---

## 🎯 What Makes This Web-Based?

Unlike the Java console project, this system features:

| Feature | Console (Java) | Web-Based (This Project) |
|---------|---------------|--------------------------|
| Access | Single computer only | Any device with browser |
| Authentication | Username/Password only | Google OAuth + Traditional |
| Notifications | None | Email + In-app |
| File Uploads | Not supported | Images, PDFs, Documents |
| Real-time Updates | No | Yes, through API |
| Mobile Access | No | Fully responsive |
| Multi-user | Sequential only | Concurrent users |
| Collaboration | Limited | Comments, assignments |
| Analytics | Basic | Dashboard with statistics |

---

## ✅ Next Steps

1. ✅ Update `.env` with all credentials
2. ✅ Run database schema
3. ✅ Test backend endpoints
4. ✅ Verify email notifications
5. ✅ Test Google OAuth
6. ⏳ Build frontend HTML pages
7. ⏳ Style with Tailwind CSS + daisyUI
8. ⏳ Connect frontend to backend API

---

**Happy Coding! 🚀**

*BatState-U TNEU Lipa - Supreme Student Council*
