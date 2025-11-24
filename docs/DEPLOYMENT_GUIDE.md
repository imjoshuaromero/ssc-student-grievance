# 🚀 Deployment Guide - SSC Grievance System

## Free Deployment Options

### ✅ **Option 1: Render.com (RECOMMENDED)**

**Pros:**
- Free PostgreSQL database (90 days, renewable)
- Free web service with HTTPS
- Auto-deployment from GitHub
- No credit card required
- Easy setup

**Limitations:**
- Service sleeps after 15 min inactivity (30-60s cold start)
- 750 hours/month free tier

---

## 📋 Step-by-Step Deployment on Render

### 1️⃣ Prepare Your Repository

1. **Commit all files to GitHub:**
   ```powershell
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Files already created:**
   - ✅ `render.yaml` - Render configuration
   - ✅ `Procfile` - Production server command
   - ✅ `runtime.txt` - Python version
   - ✅ `requirements.txt` - Updated with gunicorn

### 2️⃣ Create Render Account

1. Go to https://render.com
2. Sign up with GitHub (recommended)
3. Authorize Render to access your repositories

### 3️⃣ Deploy Database

1. Click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name:** `ssc-grievance-db`
   - **Database:** `ssc_grievance_system`
   - **User:** `ssc_admin`
   - **Region:** Choose closest to your location
   - **Plan:** Free
3. Click **"Create Database"**
4. Wait 2-3 minutes for provisioning
5. **Copy the "Internal Database URL"** (you'll need this)

### 4️⃣ Setup Database Schema

1. In Render dashboard, go to your database
2. Click **"Connect"** → **"External Connection"**
3. Use any PostgreSQL client (DBeaver, pgAdmin, or online tool)
4. Run your schema file:
   ```sql
   -- Run db/schema.sql to create tables
   -- Then run db/seed_students.sql for initial data
   ```

**OR use Render Shell:**
1. In database dashboard, click **"Shell"**
2. Paste your SQL schema directly

### 5️⃣ Deploy Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `imjoshuaromero/oop-final-project`
3. Configure:
   - **Name:** `ssc-grievance-system`
   - **Region:** Same as database
   - **Branch:** `main`
   - **Root Directory:** (leave empty)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn backend.app:app`
   - **Plan:** Free

### 6️⃣ Configure Environment Variables

In the **Environment** section, add:

```bash
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-random-secret-key-here-change-this
JWT_SECRET_KEY=your-jwt-secret-key-here-change-this

# Database (use Internal Database URL from step 3)
DATABASE_URL=postgresql://ssc_admin:password@host/ssc_grievance_system

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=24-31688@g.batstate-u.edu.ph
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=24-31688@g.batstate-u.edu.ph

# Google OAuth (if using)
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=https://your-app-name.onrender.com/api/auth/google/callback
```

**Generate secure keys:**
```python
import secrets
print(secrets.token_urlsafe(32))  # Run twice for SECRET_KEY and JWT_SECRET_KEY
```

### 7️⃣ Deploy!

1. Click **"Create Web Service"**
2. Wait 3-5 minutes for deployment
3. Check logs for errors
4. Your app will be live at: `https://ssc-grievance-system.onrender.com`

### 8️⃣ Update Frontend URLs

Update API URLs in your frontend files to point to your Render URL:

**Files to update:**
- `frontend/templates/admin-dashboard.html`
- `frontend/templates/student-dashboard.html`
- `frontend/templates/register.html`
- `frontend/templates/login.html`
- `frontend/static/js/auth.js`

Change:
```javascript
const API_BASE_URL = 'http://localhost:5000';
```

To:
```javascript
const API_BASE_URL = 'https://ssc-grievance-system.onrender.com';
```

**OR** use environment-aware URL:
```javascript
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000' 
    : 'https://ssc-grievance-system.onrender.com';
```

---

## 🔧 Alternative Options

### Option 2: Railway.app

**Pros:**
- $5 free credit/month
- PostgreSQL included
- No sleep time

**Setup:**
1. Go to https://railway.app
2. Create account with GitHub
3. Click "New Project" → "Deploy from GitHub"
4. Add PostgreSQL from marketplace
5. Railway auto-detects Python and uses Procfile

### Option 3: Fly.io

**Pros:**
- Free PostgreSQL (3GB)
- No sleep time
- Global edge network

**Setup:**
```powershell
# Install Fly CLI
irm https://fly.io/install.ps1 | iex

# Login and launch
fly auth login
fly launch
fly postgres create
fly secrets set SECRET_KEY=xxx JWT_SECRET_KEY=xxx MAIL_PASSWORD=xxx
fly deploy
```

---

## 🧪 Post-Deployment Testing

1. **Test endpoints:**
   ```powershell
   curl https://your-app-name.onrender.com/api/health
   ```

2. **Create admin account:**
   - Register at `/register`
   - Manually update database to set `role='admin'`

3. **Test features:**
   - ✅ Registration + Email verification
   - ✅ Login
   - ✅ Create concern
   - ✅ Admin dashboard
   - ✅ File uploads
   - ✅ Email notifications

---

## 🐛 Troubleshooting

### Service won't start
- Check logs in Render dashboard
- Verify all environment variables set
- Ensure DATABASE_URL is correct

### Database connection error
- Verify DATABASE_URL format: `postgresql://user:pass@host:port/dbname`
- Use **Internal Database URL** (faster, free)
- Check database is running (green status)

### Email not sending
- Verify Gmail App Password (not regular password)
- Check "Less secure app access" disabled (use App Password)
- Test with: https://www.gmass.co/smtp-test

### 502 Bad Gateway
- Service is cold starting (wait 30-60s)
- Check if service is sleeping (free tier limitation)

### File uploads not working
- Render has ephemeral filesystem (files deleted on restart)
- **Solution:** Use Cloudinary or AWS S3 for file storage
- OR accept that uploads are temporary

---

## 💰 Cost Optimization

**Free tier limits:**
- Render: 750 hours/month web + 90-day PostgreSQL
- Railway: $5 credit/month (~140 hours)
- Fly.io: 3 VMs + 3GB PostgreSQL

**Tips:**
1. Use Render for database (renew every 90 days)
2. Use Railway/Fly.io for web service (no sleep)
3. Implement database backup scripts
4. Monitor usage in dashboards

---

## 🔐 Security Checklist

Before deploying:
- ✅ Change all default passwords
- ✅ Use strong SECRET_KEY and JWT_SECRET_KEY
- ✅ Set FLASK_ENV=production
- ✅ Remove DEBUG=True in production
- ✅ Use HTTPS only (Render provides free SSL)
- ✅ Validate all user inputs
- ✅ Enable CORS only for your domain
- ✅ Use environment variables for secrets (never commit .env)

---

## 📊 Monitoring

**Render Dashboard:**
- View logs in real-time
- Check service health
- Monitor resource usage

**Database Backups:**
```sql
-- Manual backup via Render dashboard
-- Or use pg_dump via Shell
pg_dump -Fc ssc_grievance_system > backup.dump
```

---

## 🎯 Custom Domain (Optional)

1. Buy domain (Namecheap, Google Domains)
2. In Render dashboard → Settings → Custom Domains
3. Add your domain: `grievance.yourdomain.com`
4. Update DNS records (CNAME to Render)
5. Wait for SSL certificate (automatic)

---

## 📞 Support

- **Render Docs:** https://render.com/docs
- **Community:** https://community.render.com
- **Discord:** https://discord.gg/render

---

## ✅ Quick Deploy Checklist

- [ ] Push code to GitHub
- [ ] Create Render account
- [ ] Deploy PostgreSQL database
- [ ] Run schema.sql on database
- [ ] Deploy web service
- [ ] Set environment variables
- [ ] Update frontend API URLs
- [ ] Test registration & login
- [ ] Test email verification
- [ ] Create admin user
- [ ] Test all features
- [ ] Setup database backup

**Your app will be live at:** `https://[your-service-name].onrender.com` 🎉
