# Scripts Directory

This folder contains utility scripts for database management, testing, and migrations.

## 📁 Contents

### Database Check Scripts
- **check_admin.py** - Verify admin account exists / create admin
- **check_db.py** - Check database connection and basic queries
- **check_tables.py** - Verify all tables exist and structure
- **check_user_emails.py** - List all user emails in system

### Migration Scripts
- **add_verification_columns.py** - Add email verification columns to users table
- **fix_api_urls.py** - Update API URLs in templates
- **fix_delete_cascade.py** - Fix CASCADE delete constraints
- **fix_student_api_urls.py** - Update student dashboard API URLs

### Utility Scripts
- **reset_admin_password.py** - Reset admin account password
- **test_reports_data.py** - Test reports and analytics data
- **drop_trigger.py** - Drop database triggers (legacy)

## 🚀 Usage

All scripts should be run from the project root directory:

```bash
# Activate virtual environment first
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run any script
python scripts/check_db.py
python scripts/reset_admin_password.py
```

## ⚠️ Important Notes

- Always backup database before running migration scripts
- Ensure `.env` file is configured with correct database credentials
- Some scripts require admin privileges
- Scripts are idempotent (safe to run multiple times)
