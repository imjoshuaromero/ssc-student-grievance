# 🎓 SSC Grievance System

> **A comprehensive web-based platform for managing student concerns and grievances at Batangas State University - Supreme Student Council**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [Deployment](#-deployment)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 👨‍🎓 Student Features
- **User Registration & Authentication**
  - Email verification with 6-digit codes
  - Secure password hashing (bcrypt)
  - JWT-based session management
  - Google OAuth integration

- **Concern Management**
  - Submit grievances with file attachments
  - Track concern status in real-time
  - View concern history
  - Receive email notifications on updates
  - Comment on concerns

- **Dashboard**
  - Overview of submitted concerns
  - Filter by status (Pending, In Progress, Resolved)
  - Search functionality

### 👨‍💼 Admin Features
- **User Management**
  - View all registered users
  - Edit user information
  - Delete users (with CASCADE handling)
  - Role management (Student/Admin)

- **Concern Management**
  - View all concerns across the system
  - Assign concerns to administrators
  - Update concern status
  - Add resolution comments
  - File attachment management

- **Reports & Analytics**
  - Total concerns overview
  - Resolution rate statistics
  - Average resolution time
  - Category-wise breakdown
  - Time-based filtering (7/30/90 days)
  - Export to CSV

- **Email Notifications**
  - Automatic status change notifications
  - Comment notifications
  - Concern assignment alerts

---

## 🛠️ Tech Stack

### Backend
- **Framework:** Flask 3.0.0
- **Database:** PostgreSQL 14+
- **Authentication:** JWT (PyJWT), bcrypt
- **Email:** Flask-Mail (SMTP)
- **File Upload:** Pillow
- **OAuth:** Google Auth

### Frontend
- **HTML5, CSS3, JavaScript (Vanilla)**
- **Styling:** Custom CSS with responsive design
- **Icons:** Font Awesome
- **Charts:** Chart.js (for analytics)

### DevOps
- **Production Server:** Gunicorn
- **Deployment:** Render.com / Railway / Fly.io
- **Version Control:** Git & GitHub

---

## 📁 Project Structure

```
SSC-GRIEVANCE-SYSTEM/
├── backend/
│   ├── config/          # Configuration files
│   │   ├── config.py    # App configuration
│   │   └── database.py  # Database connection manager
│   ├── models/          # Database models
│   │   ├── user.py
│   │   ├── concern.py
│   │   └── category.py
│   ├── routes/          # API endpoints
│   │   ├── auth_routes.py
│   │   ├── concern_routes.py
│   │   └── user_routes.py
│   ├── utils/           # Utility functions
│   │   ├── auth.py              # JWT helpers
│   │   ├── email_service.py     # Email sender
│   │   ├── email_verification.py # Verification codes
│   │   └── google_auth.py       # Google OAuth
│   └── app.py           # Application entry point
├── frontend/
│   ├── static/
│   │   ├── css/         # Stylesheets
│   │   ├── js/          # JavaScript files
│   │   └── images/      # Static images
│   └── templates/       # HTML templates
│       ├── login.html
│       ├── register.html
│       ├── verify-email.html
│       ├── student-dashboard.html
│       └── admin-dashboard.html
├── db/
│   ├── schema.sql       # Database schema
│   ├── seed_students.sql # Sample data
│   └── *.md             # Database documentation
├── scripts/             # Utility scripts
│   ├── check_*.py       # Database check scripts
│   ├── fix_*.py         # Migration scripts
│   └── reset_*.py       # Reset utilities
├── docs/                # Documentation
│   ├── DEPLOYMENT_GUIDE.md
│   ├── SETUP_GUIDE.md
│   ├── EMAIL_VERIFICATION_GUIDE.md
│   └── *.md
├── .env.example         # Environment variables template
├── .gitignore
├── requirements.txt     # Python dependencies
├── Procfile             # Deployment configuration
├── render.yaml          # Render.com config
├── runtime.txt          # Python version
└── README.md            # This file
```

---

## 📦 Prerequisites

- **Python 3.11+**
- **PostgreSQL 14+**
- **Git**
- **Gmail Account** (for email verification)

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone [https://github.com/imjoshuaromero/oop-final-project.git](https://github.com/imjoshuaromero/ssc-student-grievance.git)
cd ssc-student-grievance
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL Database

```bash
# Create database
psql -U postgres
CREATE DATABASE ssc_grievance_system;
\q

# Import schema
psql -U postgres -d ssc_grievance_system -f db/schema.sql

# (Optional) Import sample data
psql -U postgres -d ssc_grievance_system -f db/seed_students.sql
```

### 5. Configure Environment Variables

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
FLASK_ENV=development

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ssc_grievance_system
DB_USER=postgres
DB_PASSWORD=your-postgres-password

# Email Configuration (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Google OAuth (Optional)
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:5000/api/auth/google/callback
```

**Generate Secret Keys:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

---

## ⚙️ Configuration

### Gmail App Password Setup

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification**
3. Go to **App Passwords**
4. Generate password for "Mail"
5. Copy password to `.env` as `MAIL_PASSWORD`

### Create Admin Account

```bash
python scripts/check_admin.py
# Follow prompts to create admin user
```

---

## 🏃 Running the Application

### Development Mode

```bash
python backend/app.py
```

Visit: http://localhost:5000

### Using PowerShell Script

```bash
.\run.ps1
```

### Production Mode

```bash
gunicorn backend.app:app --bind 0.0.0.0:5000
```

---

## 🌐 Deployment

Deploy to free hosting platforms:

### **Render.com** (Recommended)
- Free PostgreSQL database (90 days, renewable)
- Free web service with HTTPS
- See: [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)

### **Railway.app**
- $5 free credit/month
- Auto-deployment from GitHub

### **Fly.io**
- Free tier includes PostgreSQL
- Global edge network

**Full deployment instructions:** [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)

---

## 📖 API Documentation

### Authentication Endpoints

```
POST /api/auth/register          - Register new user
POST /api/auth/login             - Login user
POST /api/auth/send-verification-code - Send email verification
POST /api/auth/verify-code       - Verify email with code
GET  /api/auth/verify-email      - Verify via link
```

### Concern Endpoints

```
GET    /api/concerns             - Get all concerns (filtered)
POST   /api/concerns             - Create new concern
GET    /api/concerns/:id         - Get concern details
PUT    /api/concerns/:id         - Update concern
DELETE /api/concerns/:id         - Delete concern
POST   /api/concerns/:id/comments - Add comment
```

### User Management

```
GET    /api/users                - Get all users (admin)
GET    /api/users/:id            - Get user details
PUT    /api/users/:id            - Update user
DELETE /api/users/:id            - Delete user (admin)
```

**Full API documentation:** [backend/API_DOCS.md](backend/API_DOCS.md)

---

## 🧪 Testing

### Run Database Checks

```bash
python scripts/check_db.py
python scripts/check_tables.py
```

### Test Email Verification

```bash
python scripts/test_reports_data.py
```

---

## 📊 Database Schema

The system uses PostgreSQL with normalized database design (3NF):

- **users** - User accounts
- **concerns** - Student grievances
- **categories** - Concern categories
- **concern_status_history** - Status change logs
- **comments** - Concern comments
- **attachments** - File uploads
- **notifications** - User notifications

**Schema documentation:** [db/database_schema.md](db/database_schema.md)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Joshua Romero** - [@imjoshuaromero](https://github.com/imjoshuaromero)
- **Development Team** - Batangas State University

---

## 🙏 Acknowledgments

- **Batangas State University** - Supreme Student Council
- **CS 121 Course** - Final Project
- **Flask Community** - Excellent documentation
- **PostgreSQL Team** - Robust database system

---

## 📞 Support

For issues, questions, or contributions:

- **GitHub Issues:** [Create an issue](https://github.com/imjoshuaromero/oop-final-project/issues)
- **Email:** 24-31688@g.batstate-u.edu.ph

---

## 🎯 Roadmap

- [ ] Mobile app (React Native)
- [ ] SMS notifications
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Dark mode
- [ ] PWA support

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ by the BatStateU SSC Team

</div>
