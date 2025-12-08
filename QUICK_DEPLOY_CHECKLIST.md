# 🚀 Quick Render Deployment Checklist

## Before You Start
- [ ] Code pushed to GitHub (`main` branch)
- [ ] Render account created (https://render.com)
- [ ] Gmail App Password ready (for email notifications)

## Step 1: Create Database (5 minutes)
1. **New +** → **PostgreSQL**
2. Name: `ssc-grievance-db`
3. Region: **Singapore**
4. Plan: **Free**
5. **Create Database**
6. ✅ Copy **Internal Database URL**

## Step 2: Run Database Schema (2 minutes)
```bash
# Connect to database
psql "YOUR_EXTERNAL_DATABASE_URL"

# Run schema
\i db/schema.sql

# Verify
\dt

# Exit
\q
```

## Step 3: Deploy Web Service (10 minutes)
1. **New +** → **Web Service**
2. Connect: `imjoshuaromero/oop-final-project`
3. Settings:
   - Name: `ssc-grievance-system`
   - Region: **Singapore**
   - Branch: `main`
   - Runtime: **Python 3**
   - Build: `chmod +x render-build.sh && ./render-build.sh`
   - Start: `gunicorn backend.app:app --bind 0.0.0.0:$PORT`
   - Plan: **Free**

## Step 4: Add Environment Variables (5 minutes)
Copy these to Render Environment section:

```bash
DATABASE_URL=postgresql://postgres:PASSWORD@dpg-xxx.singapore-postgres.render.com/grievance_system
SECRET_KEY=generate-random-32-char-string
JWT_SECRET_KEY=generate-random-32-char-string
FLASK_ENV=production
PORT=10000
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
GOOGLE_CLIENT_ID=your-google-oauth-id
GOOGLE_CLIENT_SECRET=your-google-oauth-secret
GOOGLE_REDIRECT_URI=https://ssc-grievance-system.onrender.com/api/auth/google/callback
CORS_ORIGINS=https://ssc-grievance-system.onrender.com
```

## Step 5: Create Admin Account (2 minutes)
```sql
-- Connect to database
psql "YOUR_EXTERNAL_DATABASE_URL"

-- Create admin
INSERT INTO users (sr_code, email, password_hash, first_name, last_name, role, email_verified)
VALUES ('00-00000', 'admin@batstateu.edu.ph', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lOZBvD.YM0iq', 'System', 'Administrator', 'admin', TRUE);

-- Exit
\q
```

**Admin Login:**
- Email: `admin@batstateu.edu.ph`
- Password: `admin123`

## Step 6: Test Deployment (2 minutes)
1. Visit: `https://ssc-grievance-system.onrender.com`
2. Login with admin credentials
3. Register test student
4. Submit test concern
5. Test export features

## ✅ Done!
Your app is live at: **https://ssc-grievance-system.onrender.com**

## Quick Commands

### Generate Secret Key
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Connect to Database
```bash
psql "postgresql://postgres:PASSWORD@dpg-xxx.singapore-postgres.render.com/grievance_system"
```

### View Render Logs
```bash
# In Render dashboard: Service → Logs tab
```

### Redeploy
```bash
git add .
git commit -m "Update"
git push origin main
# Auto-deploys
```

## Troubleshooting

### Service won't start?
- Check environment variables are set
- Verify `DATABASE_URL` is correct
- Check build logs for errors

### Database connection failed?
- Use **Internal Database URL** (not External)
- Verify database status is "Available"

### Email not sending?
- Use Gmail App Password (not regular password)
- Enable 2FA on Gmail first

## Free Tier Limits
- Web: 750 hours/month, sleeps after 15 min
- Database: 1 GB storage, 97 connections
- Both auto-suspend if inactive

## Keep Awake (Optional)
Use UptimeRobot to ping every 5 minutes:
- URL: `https://ssc-grievance-system.onrender.com/api/health`

---

**Total Time: ~25 minutes** ⚡
