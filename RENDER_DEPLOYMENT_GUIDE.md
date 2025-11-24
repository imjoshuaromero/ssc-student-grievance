# 🚀 Complete Render Deployment Guide

## Step 1: Prepare Your Code

### ✅ Already Done:
- ✅ `requirements.txt` - All dependencies listed
- ✅ `Procfile` - Gunicorn configuration
- ✅ `runtime.txt` - Python version specified
- ✅ `render.yaml` - Render configuration
- ✅ Database config supports `DATABASE_URL`
- ✅ App configured for production

### 📝 Quick Check:
```bash
git status
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

---

## Step 2: Create Render Account

1. **Go to:** https://render.com
2. **Click:** "Get Started for Free"
3. **Sign up with GitHub** (recommended)
4. **Authorize Render** to access your repositories

---

## Step 3: Create PostgreSQL Database

### 3.1 Create Database
1. Click **"New +"** (top right)
2. Select **"PostgreSQL"**

### 3.2 Configure Database
Fill in these details:
```
Name: ssc-grievance-db
Database: grievance_system
User: postgres
Region: Singapore (closest to Philippines)
PostgreSQL Version: 15
```

### 3.3 Select Plan
- Choose **"Free"** plan
- Free tier includes:
  - 1 GB storage
  - Shared CPU
  - Auto-suspend after 90 days inactivity

### 3.4 Create Database
- Click **"Create Database"**
- Wait 2-3 minutes for database to provision

### 3.5 Get Connection Details
After creation, you'll see:
```
Status: Available
Host: dpg-xxxxx.singapore-postgres.render.com
Port: 5432
Database: grievance_system
Username: postgres
Password: [auto-generated]
```

**⚠️ IMPORTANT:** Copy these values:
- **Internal Database URL** (starts with `postgresql://`)
- **External Database URL** (for local testing)

---

## Step 4: Setup Database Schema

### Option A: Using Render Shell (Recommended)
1. In your database dashboard, click **"Connect"** → **"External Connection"**
2. Copy the connection string
3. On your local machine, run:
```bash
# Install PostgreSQL client if not installed
winget install PostgreSQL.PostgreSQL

# Connect to database
psql "postgresql://postgres:YOUR_PASSWORD@dpg-xxxxx.singapore-postgres.render.com/grievance_system"

# Run your schema
\i db/schema.sql

# Verify tables
\dt

# Exit
\q
```

### Option B: Using DBeaver/pgAdmin
1. Download **DBeaver** or **pgAdmin**
2. Create new connection using External Database URL
3. Execute your `db/schema.sql` file
4. Verify tables are created

---

## Step 5: Deploy Web Service

### 5.1 Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Click **"Connect a repository"**
3. Find and select: **`imjoshuaromero/oop-final-project`**
4. Click **"Connect"**

### 5.2 Configure Service
Fill in these details:

```
Name: ssc-grievance-system
Region: Singapore
Branch: main
Runtime: Python 3
Build Command: chmod +x render-build.sh && ./render-build.sh
Start Command: gunicorn backend.app:app --bind 0.0.0.0:$PORT
```

### 5.3 Select Plan
- Choose **"Free"** plan
- Free tier includes:
  - 512 MB RAM
  - Shared CPU
  - 750 hours/month
  - Auto-suspend after 15 min inactivity

---

## Step 6: Configure Environment Variables

### 6.1 Add Environment Variables
In the **Environment** section, click **"Add Environment Variable"** and add these:

#### Required Variables:
```bash
# Database
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@dpg-xxxxx.singapore-postgres.render.com/grievance_system

# Security Keys (Generate strong random strings)
SECRET_KEY=your-super-secret-key-change-this-to-random-string
JWT_SECRET_KEY=your-jwt-secret-key-change-this-too

# Flask Environment
FLASK_ENV=production
PORT=10000

# Email Configuration (Gmail App Password)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
MAIL_ADMIN_EMAIL=ssc@batstateu.edu.ph

# Google OAuth (Optional - for Google login)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=https://ssc-grievance-system.onrender.com/api/auth/google/callback

# CORS (Your deployed URL)
CORS_ORIGINS=https://ssc-grievance-system.onrender.com
```

#### How to Get Gmail App Password:
1. Go to: https://myaccount.google.com/security
2. Enable **"2-Step Verification"**
3. Go to **"App passwords"**
4. Select app: **"Mail"**, device: **"Other"** (type "Render")
5. Click **"Generate"**
6. Copy the 16-character password

#### How to Generate Secret Keys:
```bash
# In Python terminal
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 6.2 Save Environment Variables
- Click **"Save Changes"**

---

## Step 7: Deploy Application

### 7.1 Create and Deploy
1. Click **"Create Web Service"**
2. Deployment will start automatically
3. Watch the build logs

### 7.2 Monitor Deployment
You'll see logs like:
```
==> Cloning from https://github.com/imjoshuaromero/oop-final-project...
==> Running build command: './render-build.sh'...
==> Installing dependencies...
==> Build completed successfully!
==> Starting service with 'gunicorn backend.app:app'...
==> Service is live 🎉
```

### 7.3 Check Deployment Status
- **Status:** Should show "Live" with green indicator
- **URL:** `https://ssc-grievance-system.onrender.com`

---

## Step 8: Create Admin Account

### 8.1 Connect to Database
```bash
psql "postgresql://postgres:YOUR_PASSWORD@dpg-xxxxx.singapore-postgres.render.com/grievance_system"
```

### 8.2 Create Admin User
```sql
-- Insert admin account
INSERT INTO users (
    sr_code, 
    email, 
    password_hash, 
    first_name, 
    last_name, 
    role,
    email_verified
) VALUES (
    '00-00000', 
    'admin@batstateu.edu.ph',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lOZBvD.YM0iq',  -- password: admin123
    'System',
    'Administrator',
    'admin',
    TRUE
);
```

**Admin Login Credentials:**
- Email: `admin@batstateu.edu.ph`
- Password: `admin123`
- ⚠️ **Change this password immediately after first login!**

---

## Step 9: Test Your Deployment

### 9.1 Health Check
Visit: `https://ssc-grievance-system.onrender.com/api/health`

Should return:
```json
{
  "status": "healthy",
  "message": "Grievance System API is running"
}
```

### 9.2 Test Frontend
1. Visit: `https://ssc-grievance-system.onrender.com/login`
2. Try logging in with admin credentials
3. Register a test student account
4. Submit a test concern

### 9.3 Test Features
- ✅ Login/Register
- ✅ Submit Concern
- ✅ Upload Files
- ✅ Admin Dashboard
- ✅ Export CSV/PDF
- ✅ Email Notifications
- ✅ Google Login (if configured)

---

## Step 10: Configure Custom Domain (Optional)

### 10.1 Add Custom Domain
1. In Render dashboard, go to **Settings**
2. Scroll to **Custom Domains**
3. Click **"Add Custom Domain"**
4. Enter your domain: `grievance.yourdomain.com`

### 10.2 Update DNS Records
Add these records to your domain provider:
```
Type: CNAME
Name: grievance
Value: ssc-grievance-system.onrender.com
TTL: 3600
```

### 10.3 Update Environment Variables
Update `GOOGLE_REDIRECT_URI` and `CORS_ORIGINS` to use your custom domain

---

## 🔧 Troubleshooting

### Issue: Service Won't Start
**Check:**
1. Build logs for errors
2. Start command is correct: `gunicorn backend.app:app`
3. All environment variables are set

### Issue: Database Connection Error
**Check:**
1. `DATABASE_URL` is correct
2. Database status is "Available"
3. Internal URL is used (not External)

### Issue: 502 Bad Gateway
**Fix:**
1. Check if app binds to `0.0.0.0:$PORT`
2. Verify gunicorn is running
3. Check application logs

### Issue: Import Errors
**Fix:**
1. Ensure all dependencies in `requirements.txt`
2. Check Python version matches `runtime.txt`
3. Rebuild service

### Issue: Email Not Sending
**Check:**
1. Gmail App Password is correct
2. `MAIL_USE_TLS=True` is set
3. Email provider allows SMTP

---

## 📊 Monitoring & Maintenance

### View Logs
1. Go to your service dashboard
2. Click **"Logs"** tab
3. Real-time logs appear here

### Check Metrics
- **CPU Usage**
- **Memory Usage**
- **Response Time**
- **Request Count**

### Auto-Deploy on Push
Render automatically deploys when you push to `main` branch:
```bash
git add .
git commit -m "Update feature"
git push origin main
# Deployment starts automatically
```

### Manual Deploy
1. Go to service dashboard
2. Click **"Manual Deploy"**
3. Select branch: `main`
4. Click **"Deploy"**

---

## 💰 Free Tier Limits

### Web Service:
- ✅ 750 hours/month (enough for 1 service)
- ✅ 512 MB RAM
- ✅ Shared CPU
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ 50 sec to wake up

### Database:
- ✅ 1 GB storage
- ✅ Shared CPU
- ⚠️ Expires after 90 days inactivity
- ⚠️ Connection limit: 97

### Keep Service Awake (Optional):
Use a free uptime monitor:
- **UptimeRobot**: https://uptimerobot.com
- Ping your app every 5 minutes
- Prevents sleep

---

## 🎉 You're Live!

Your app is now deployed at:
**https://ssc-grievance-system.onrender.com**

### Next Steps:
1. ✅ Test all features
2. ✅ Create admin account
3. ✅ Add test data
4. ✅ Invite users to test
5. ✅ Monitor logs
6. ✅ Update Google OAuth redirect URI
7. ✅ Share with your team!

---

## 📞 Need Help?

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **Flask Docs**: https://flask.palletsprojects.com
- **PostgreSQL Docs**: https://www.postgresql.org/docs

---

**Good luck with your deployment! 🚀**
