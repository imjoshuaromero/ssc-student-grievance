# 🚀 PythonAnywhere Deployment Guide
## SSC Student Grievance System

**Last Updated:** December 8, 2025

---

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [PythonAnywhere Account Setup](#pythonanywhere-account-setup)
3. [Database Setup (PostgreSQL)](#database-setup-postgresql)
4. [Upload Code to PythonAnywhere](#upload-code-to-pythonanywhere)
5. [Virtual Environment Setup](#virtual-environment-setup)
6. [Configure Environment Variables](#configure-environment-variables)
7. [WSGI Configuration](#wsgi-configuration)
8. [Static Files Configuration](#static-files-configuration)
9. [Database Migration](#database-migration)
10. [Testing the Deployment](#testing-the-deployment)
11. [Troubleshooting](#troubleshooting)
12. [Post-Deployment Tasks](#post-deployment-tasks)

---

## 1. Prerequisites

### Required Accounts
- ✅ **PythonAnywhere Account** (Free or Paid)
  - Free tier: Limited to 1 web app, 512MB disk space
  - Paid tier: Recommended for production (PostgreSQL support)
  - Sign up: https://www.pythonanywhere.com/registration/register/beginner/

### Required Information
- 📧 Email service credentials (Gmail/SMTP)
- 🔑 Google OAuth credentials (if using Google login)
- 🗄️ Database credentials (will be created on PythonAnywhere)

### Local Setup
- ✅ Code pushed to GitHub (already done)
- ✅ requirements.txt file present
- ✅ All environment variables documented

---

## 2. PythonAnywhere Account Setup

### Step 1: Create Account
1. Go to https://www.pythonanywhere.com/
2. Click **"Start running Python online"** or **"Pricing & signup"**
3. Choose a plan:
   - **Beginner (Free)**: 1 web app, limited features, **NO PostgreSQL**
   - **Hacker ($5/month)**: PostgreSQL support, custom domains
   - **Web Dev ($12/month)**: More resources, recommended for production

4. Complete registration with your email

### Step 2: Verify Email
- Check your email for verification link
- Click the link to activate your account

### Step 3: Login to Dashboard
- Go to https://www.pythonanywhere.com/login/
- Enter credentials
- You'll see your dashboard with tabs: Dashboard, Consoles, Files, Web, Databases, etc.

---

## 3. Database Setup (PostgreSQL)

### ⚠️ Important Note
**PostgreSQL is only available on paid plans ($5/month minimum)**

If you're on the free tier, you'll need to use MySQL instead. See Alternative Database Options below.

### Option A: PostgreSQL (Recommended - Paid Plan Required)

#### Step 1: Enable PostgreSQL
1. Go to **"Databases"** tab
2. Click **"Initialize PostgreSQL"** (only visible on paid plans)
3. Set a PostgreSQL password (save this!)

#### Step 2: Note Database Connection Details
```
Host: your-username.postgres.pythonanywhere-services.com
Port: 10XXX (will be shown in dashboard)
Database: your-username$dbname
Username: your-username
Password: (the one you just set)
```

#### Step 3: Create Database
Open a **Bash console** from the "Consoles" tab:

```bash
# Connect to PostgreSQL
psql -h your-username.postgres.pythonanywhere-services.com -p 10XXX -U your-username -d postgres

# Create database
CREATE DATABASE ssc_grievance_db;

# Connect to the new database
\c ssc_grievance_db

# Exit psql
\q
```

### Option B: MySQL (Free Tier Compatible)

If using free tier, use MySQL instead:

#### Step 1: Initialize MySQL
1. Go to **"Databases"** tab
2. Set a MySQL password
3. Create a new database: `yourusername$ssc_grievance`

#### Step 2: Update Code for MySQL
You'll need to modify `backend/config/database.py` to use MySQL:

```python
import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='yourusername.mysql.pythonanywhere-services.com',
                database='yourusername$ssc_grievance',
                user='yourusername',
                password=os.environ.get('DB_PASSWORD')
            )
            # ... rest of the code
```

**For this guide, we'll proceed with PostgreSQL (paid plan).**

---

## 4. Upload Code to PythonAnywhere

### Method 1: Clone from GitHub (Recommended)

#### Step 1: Open Bash Console
- Go to **"Consoles"** tab
- Click **"$ Bash"** to start a new console

#### Step 2: Clone Your Repository
```bash
cd ~
git clone https://github.com/imjoshuaromero/ssc-student-grievance.git
cd ssc-student-grievance
```

#### Step 3: Switch to Correct Branch
```bash
git checkout josh-updates
```

#### Step 4: Verify Files
```bash
ls -la
# You should see: backend/, frontend/, db/, requirements.txt, etc.
```

### Method 2: Upload via Files Tab (Alternative)

1. Go to **"Files"** tab
2. Navigate to `/home/yourusername/`
3. Create folder: `ssc-student-grievance`
4. Upload files manually (tedious, not recommended)

---

## 5. Virtual Environment Setup

### Step 1: Create Virtual Environment
In your Bash console:

```bash
cd ~/ssc-student-grievance

# Create virtual environment with Python 3.10
mkvirtualenv --python=/usr/bin/python3.10 ssc-grievance-env
```

### Step 2: Activate Virtual Environment
```bash
workon ssc-grievance-env
```

You should see `(ssc-grievance-env)` in your prompt.

### Step 3: Upgrade pip
```bash
pip install --upgrade pip
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

**Common packages installed:**
- Flask==3.0.0
- Flask-CORS
- psycopg2-binary (for PostgreSQL)
- python-dotenv
- bcrypt
- PyJWT
- Flask-Mail
- google-auth
- google-auth-oauthlib

### Step 5: Verify Installation
```bash
pip list
```

---

## 6. Configure Environment Variables

### Step 1: Create .env File
```bash
cd ~/ssc-student-grievance
nano .env
```

### Step 2: Add Environment Variables
Paste the following (replace with your actual values):

```bash
# Database Configuration (PostgreSQL)
DB_HOST=yourusername.postgres.pythonanywhere-services.com
DB_PORT=10XXX
DB_NAME=yourusername$ssc_grievance_db
DB_USER=yourusername
DB_PASSWORD=your_postgres_password

# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here-change-this
JWT_SECRET_KEY=your-jwt-secret-key-here-change-this

# Email Configuration (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Google OAuth (Optional)
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Application URL
APP_URL=https://yourusername.pythonanywhere.com
FRONTEND_URL=https://yourusername.pythonanywhere.com

# File Upload Configuration
UPLOAD_FOLDER=/home/yourusername/ssc-student-grievance/uploads
MAX_FILE_SIZE=5242880
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,pdf,doc,docx
```

**Press:** `Ctrl+O` (save), `Enter` (confirm), `Ctrl+X` (exit)

### Step 3: Generate Secret Keys
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Use these outputs for `SECRET_KEY` and `JWT_SECRET_KEY`.

### Step 4: Gmail App Password Setup
1. Go to https://myaccount.google.com/security
2. Enable **2-Step Verification**
3. Go to **App passwords**
4. Generate password for "Mail"
5. Use this 16-character password in `MAIL_PASSWORD`

### Step 5: Create Uploads Directory
```bash
mkdir -p ~/ssc-student-grievance/uploads
chmod 755 ~/ssc-student-grievance/uploads
```

---

## 7. WSGI Configuration

### Step 1: Go to Web Tab
1. Click **"Web"** in the top menu
2. Click **"Add a new web app"**
3. Choose domain: `yourusername.pythonanywhere.com` (free subdomain)
4. Select **"Manual configuration"**
5. Choose **Python 3.10**

### Step 2: Configure Source Code Path
In the Web tab, find **"Code"** section:

**Source code:** `/home/yourusername/ssc-student-grievance`

### Step 3: Configure Virtual Environment
In **"Virtualenv"** section:

**Path:** `/home/yourusername/.virtualenvs/ssc-grievance-env`

### Step 4: Edit WSGI Configuration File
Click the **WSGI configuration file** link (e.g., `/var/www/yourusername_pythonanywhere_com_wsgi.py`)

**Replace ALL contents** with:

```python
# +++++++++++ FLASK +++++++++++
import sys
import os
from dotenv import load_dotenv

# Add your project directory to the sys.path
project_home = '/home/yourusername/ssc-student-grievance'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables
load_dotenv(os.path.join(project_home, '.env'))

# Import Flask app
from backend.app import app as application

# Set up logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('WSGI application starting...')
```

**Important:** Replace `yourusername` with your actual PythonAnywhere username!

**Save the file:** `Ctrl+S` or click "Save"

---

## 8. Static Files Configuration

### Step 1: Configure Static Files Mapping
In the **Web** tab, scroll to **"Static files"** section.

Add two mappings:

#### Mapping 1: CSS/JS/Images
- **URL:** `/static/`
- **Directory:** `/home/yourusername/ssc-student-grievance/frontend/static/`

#### Mapping 2: Uploads
- **URL:** `/uploads/`
- **Directory:** `/home/yourusername/ssc-student-grievance/uploads/`

### Step 2: Verify Static Files Exist
```bash
ls -la ~/ssc-student-grievance/frontend/static/
# Should show: css/, js/, images/
```

---

## 9. Database Migration

### Step 1: Connect to PostgreSQL
```bash
psql -h yourusername.postgres.pythonanywhere-services.com \
     -p 10XXX \
     -U yourusername \
     -d yourusername\$ssc_grievance_db
```

### Step 2: Run Schema Script
From Bash console:

```bash
cd ~/ssc-student-grievance
psql -h yourusername.postgres.pythonanywhere-services.com \
     -p 10XXX \
     -U yourusername \
     -d yourusername\$ssc_grievance_db \
     -f db/schema.sql
```

### Step 3: Verify Tables Created
```bash
psql -h yourusername.postgres.pythonanywhere-services.com \
     -p 10XXX \
     -U yourusername \
     -d yourusername\$ssc_grievance_db \
     -c "\dt"
```

You should see:
- users
- concerns
- concern_categories
- offices
- concern_status_history
- comments
- notifications
- attachments

### Step 4: Seed Sample Data (Optional)
```bash
psql -h yourusername.postgres.pythonanywhere-services.com \
     -p 10XXX \
     -U yourusername \
     -d yourusername\$ssc_grievance_db \
     -f db/seed_students.sql
```

### Step 5: Create Admin User
```bash
cd ~/ssc-student-grievance
workon ssc-grievance-env
python db/create_admin.py
```

---

## 10. Testing the Deployment

### Step 1: Reload Web App
In the **Web** tab, click the big green **"Reload yourusername.pythonanywhere.com"** button.

### Step 2: Check Error Logs
Scroll down to **"Log files"** section:
- Click **"Error log"** to see any errors
- Click **"Server log"** to see access logs

### Step 3: Visit Your Site
Open: `https://yourusername.pythonanywhere.com`

You should see the login page.

### Step 4: Test Basic Functionality

#### Test 1: Registration
1. Go to `/register`
2. Create a new student account
3. Check email for verification code
4. Verify email

#### Test 2: Login
1. Go to `/login`
2. Login with your account
3. Should redirect to student dashboard

#### Test 3: Submit Concern
1. Click "Submit New Concern"
2. Fill out form
3. Submit
4. Check if it appears in your dashboard

#### Test 4: Admin Login
1. Logout
2. Login with admin credentials
3. Should see admin dashboard
4. Verify concern appears

---

## 11. Troubleshooting

### Issue 1: 502 Bad Gateway

**Cause:** WSGI configuration error

**Solution:**
```bash
# Check error log in Web tab
# Common fixes:

# 1. Verify WSGI file path is correct
# 2. Check virtual environment path
# 3. Ensure all imports work:

workon ssc-grievance-env
cd ~/ssc-student-grievance
python -c "from backend.app import app; print('Success!')"
```

### Issue 2: Database Connection Failed

**Cause:** Wrong database credentials or PostgreSQL not initialized

**Solution:**
```bash
# Verify .env file has correct values
cat ~/.env

# Test connection manually
psql -h yourusername.postgres.pythonanywhere-services.com \
     -p 10XXX \
     -U yourusername \
     -d postgres
```

### Issue 3: ModuleNotFoundError

**Cause:** Missing packages or wrong Python version

**Solution:**
```bash
workon ssc-grievance-env
pip install -r requirements.txt

# Verify installation
pip list | grep Flask
pip list | grep psycopg2
```

### Issue 4: Static Files Not Loading

**Cause:** Wrong static file paths

**Solution:**
1. Go to Web tab
2. Check **"Static files"** mappings
3. Verify paths are absolute: `/home/yourusername/...`
4. Reload web app

### Issue 5: Email Not Sending

**Cause:** Gmail blocking or wrong credentials

**Solution:**
```bash
# Test email configuration
workon ssc-grievance-env
python

>>> from backend.utils.email_service import send_email
>>> send_email('test@example.com', 'Test', 'This is a test')
```

Check Gmail:
- Enable 2-Step Verification
- Generate App Password
- Allow less secure apps (if needed)

### Issue 6: 413 Request Entity Too Large

**Cause:** File upload size limit

**Solution:**
Edit WSGI file to increase limit:

```python
# Add after imports
from werkzeug.middleware.proxy_fix import ProxyFix
application.wsgi_app = ProxyFix(application.wsgi_app)
application.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

### Issue 7: Permission Denied on Uploads

**Cause:** Upload directory permissions

**Solution:**
```bash
chmod 755 ~/ssc-student-grievance/uploads
chmod 644 ~/ssc-student-grievance/uploads/*
```

---

## 12. Post-Deployment Tasks

### ✅ Security Checklist

1. **Change Default Admin Password**
```bash
cd ~/ssc-student-grievance
workon ssc-grievance-env
python scripts/reset_admin_password.py
```

2. **Enable HTTPS** (Free with PythonAnywhere)
   - Already enabled by default!
   - Your app is at: `https://yourusername.pythonanywhere.com`

3. **Set Strong Secret Keys**
   - Verify `.env` has secure random keys
   - Never commit `.env` to Git

4. **Configure CORS** (if needed)
   - Already configured in `backend/app.py`
   - Update allowed origins if using custom domain

5. **Review Environment Variables**
```bash
cat ~/.env | grep -v PASSWORD
```

### 🔄 Regular Maintenance

#### Update Code from GitHub
```bash
cd ~/ssc-student-grievance
git pull origin josh-updates
workon ssc-grievance-env
pip install -r requirements.txt
# Reload web app from Web tab
```

#### View Logs
```bash
# Real-time error monitoring
tail -f /var/log/yourusername.pythonanywhere.com.error.log

# Access logs
tail -f /var/log/yourusername.pythonanywhere.com.access.log
```

#### Database Backup
```bash
# Create backup
pg_dump -h yourusername.postgres.pythonanywhere-services.com \
        -p 10XXX \
        -U yourusername \
        -d yourusername\$ssc_grievance_db \
        -f ~/backup_$(date +%Y%m%d).sql

# Download backup via Files tab
```

### 📊 Monitoring

#### Check Disk Space
```bash
du -sh ~/ssc-student-grievance
du -sh ~/ssc-student-grievance/uploads
```

#### Check Database Size
```sql
SELECT 
    pg_size_pretty(pg_database_size('yourusername$ssc_grievance_db')) as db_size;
```

#### View Active Users
```sql
SELECT COUNT(*) FROM users WHERE is_active = true;
```

### 🚀 Performance Optimization

1. **Enable Gzip Compression** (add to WSGI):
```python
from flask_compress import Compress
Compress(application)
```

2. **Add Caching**:
```bash
pip install Flask-Caching
```

3. **Optimize Database Queries**:
   - Add indexes (already done in schema.sql)
   - Use connection pooling

### 📱 Custom Domain (Optional - Paid Plan)

1. Go to **Web** tab
2. Add custom domain: `yourdomain.com`
3. Update DNS records:
   - **CNAME**: `www` → `webapp-XXXX.pythonanywhere.com`
   - **A Record**: `@` → `provided IP address`
4. Update `.env`:
```bash
APP_URL=https://yourdomain.com
FRONTEND_URL=https://yourdomain.com
```

---

## 📞 Support & Resources

### PythonAnywhere Help
- **Documentation:** https://help.pythonanywhere.com/
- **Forums:** https://www.pythonanywhere.com/forums/
- **Support:** help@pythonanywhere.com

### Flask Documentation
- **Official Docs:** https://flask.palletsprojects.com/
- **Deployment Guide:** https://flask.palletsprojects.com/en/2.3.x/deploying/

### PostgreSQL Documentation
- **Official Docs:** https://www.postgresql.org/docs/
- **PythonAnywhere PostgreSQL:** https://help.pythonanywhere.com/pages/Postgres

---

## ✅ Deployment Checklist

Use this checklist to ensure everything is set up correctly:

### Pre-Deployment
- [ ] PythonAnywhere account created (paid plan for PostgreSQL)
- [ ] Code pushed to GitHub
- [ ] Gmail app password generated
- [ ] Google OAuth credentials configured (if using)
- [ ] requirements.txt is up to date

### Database Setup
- [ ] PostgreSQL initialized
- [ ] Database created (`ssc_grievance_db`)
- [ ] Schema migrated (`db/schema.sql`)
- [ ] Sample data seeded (optional)
- [ ] Admin user created

### Code Deployment
- [ ] Repository cloned to PythonAnywhere
- [ ] Correct branch checked out (`josh-updates`)
- [ ] Virtual environment created
- [ ] Dependencies installed (`requirements.txt`)
- [ ] `.env` file configured with all variables
- [ ] Uploads directory created with permissions

### Web Configuration
- [ ] Web app created (Manual configuration, Python 3.10)
- [ ] Source code path set
- [ ] Virtual environment path set
- [ ] WSGI file configured
- [ ] Static files mapped (`/static/` and `/uploads/`)
- [ ] Web app reloaded

### Testing
- [ ] Homepage loads without errors
- [ ] Registration works
- [ ] Email verification works
- [ ] Login works
- [ ] Student dashboard accessible
- [ ] Concern submission works
- [ ] Admin dashboard accessible
- [ ] File uploads work
- [ ] Error logs checked

### Security
- [ ] Admin password changed
- [ ] Strong secret keys set
- [ ] HTTPS enabled (automatic)
- [ ] `.env` file not in Git
- [ ] Database credentials secure

### Post-Deployment
- [ ] Documentation updated with live URL
- [ ] Team members notified
- [ ] Monitoring set up
- [ ] Backup strategy in place
- [ ] Update procedure documented

---

## 🎉 Congratulations!

Your SSC Student Grievance System is now live on PythonAnywhere!

**Live URL:** `https://yourusername.pythonanywhere.com`

### Next Steps:
1. Share the URL with your team for testing
2. Monitor error logs for the first 24 hours
3. Create a few test concerns to verify functionality
4. Document any issues and fixes
5. Prepare for user onboarding

---

**Need Help?**
- Check the [Troubleshooting](#troubleshooting) section
- Review PythonAnywhere error logs
- Contact PythonAnywhere support
- Review Flask documentation

**Good luck with your deployment! 🚀**
