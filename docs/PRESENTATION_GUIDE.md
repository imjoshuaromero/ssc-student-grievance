# SSC Student Grievance System — Presentation & Technical Guide

Last updated: 2025-12-16

Purpose: This document prepares you for your project presentation and defense. It contains a short walkthrough script, a detailed code map (which file does what and how modules connect), explanations of the routing/logic/email/auth systems, the purpose of important framework/library imports, and suggested Q&A topics.

---

## 1. Quick Walkthrough Script (2–3 minutes)

Use this short script to open the presentation and guide reviewers through the system.

"Good [morning/afternoon]. We are presenting the SSC Student Grievance Reporting and Tracking System — a web application built with Flask and PostgreSQL to enable students to file grievances and for administrators to manage them. The system includes user registration with email verification, Google SSO support, secure authentication using JWT, a robust backend with triggers (ticket generation, status history), and a responsive frontend for students and admins.

Demo flow: 1) register a student account and verify your email; 2) sign in and submit a new concern with optional attachments; 3) as an admin, view, assign, and resolve concerns; 4) view email notifications and the status history.

This system enforces data integrity via a normalized 3NF database, automates ticket numbering with a database trigger to avoid duplicates, and uses Flask-Mail for email notifications. I will now explain the architecture and key components of the codebase, followed by some technical Q&A points." 

(End of script.)

---

## 2. High-Level Architecture

- Backend: Flask application in `backend/` (Blueprints for routes, models for DB access, utils for helpers).
- Database: PostgreSQL (schema in `db/schema.sql`) with triggers and views.
- Frontend: Static templates and assets in `frontend/templates` and `frontend/static` (JS in `frontend/static/js`).
- Deployment: Designed for hosting on PythonAnywhere / Render / Heroku (supports `DATABASE_URL`).

Core connections:
- `backend/app.py` creates the Flask app, registers Blueprints, sets template/static folders to `frontend/`.
- Blueprints:
  - `backend/routes/auth_routes.py` ⇒ `/api/auth`
  - `backend/routes/concern_routes.py` ⇒ `/api/concerns`
  - `backend/routes/user_routes.py` ⇒ `/api/users`
- Models call `backend/config/database.py::Database.execute_query()` for all DB access.
- Emailing uses `backend/utils/email_service.py`, initialized in `backend/app.py` via `init_mail(app)`.

---

## 3. File Map & How Code Works (Detailed)

This section lists important files, responsibilities, and connections. Use file links relative to the repository root.

### 3.1 Entry point
- `backend/app.py`
  - Creates Flask `app` with `template_folder='../frontend/templates'` and `static_folder='../frontend/static'`.
  - Configures CORS using `flask_cors.CORS` for `/api/*` endpoints.
  - Calls `init_mail(app)` from `backend/utils/email_service.py` to initialize email support.
  - Registers Blueprints: `auth_bp`, `concern_bp`, `user_bp` with url_prefixes.
  - Exposes frontend routes that render templates (`/login`, `/register`, `/student-dashboard`, `/admin-dashboard`).

Why this matters: `create_app()` centralizes configuration and wiring so the WSGI entrypoint can import a single `app` for production.

### 3.2 Routing (APIs & Frontend)

#### Authentication routes — `backend/routes/auth_routes.py` (Blueprint: `auth_bp` → `/api/auth`)
Key endpoints (representative):
- `POST /api/auth/register` — Registers a new user (validates SR code, email, hashes password, saves user via `backend/models/user.py::User.create()`), inserts verification code, and sends verification email.
- `POST /api/auth/login` — Validates credentials, checks email verification (students), returns JWT token from `backend/utils/auth.py::generate_token()`.
- `GET /api/auth/google` & OAuth callbacks — Initiates Google SSO and exchanges code for token (calls `backend/utils/google_auth.py`).
- `POST /api/auth/verify` — Verifies email code or token (uses `backend/utils/email_verification.py`).

Connections:
- Uses `backend.config.database.Database` for direct DB updates (e.g., storing verification code).
- Uses `backend.utils.email_service` functions to send verification emails.
- Uses `backend.models.user.User` for user CRUD.

#### Concerns routes — `backend/routes/concern_routes.py` (Blueprint: `concern_bp` → `/api/concerns`)
Key endpoints (representative):
- `POST /api/concerns/` — Create a new concern (protected by `token_required`). Accepts JSON or multipart form for attachments. Calls `backend.models.concern.Concern.create()` to insert the record.
- `GET /api/concerns/` — List concerns (admin filterable, students see their own).
- `GET /api/concerns/<id>` — Get concern details (includes student name, category, assigned office info using JOINs in `Concern.find_by_id`).
- `PATCH /api/concerns/<id>/status` — Update status, which triggers `Concern.add_status_history()` and email notifications.
- `POST /api/concerns/<id>/comments` — Add comment; may send notification emails via `email_service`.

Connections:
- File uploads handled using `werkzeug.utils.secure_filename` to sanitize filenames and saved to `uploads/`.
- Uses `token_required` and `admin_required` from `backend/utils/auth.py`.
- After creation or status change, functions from `email_service.py` are invoked (e.g., `send_concern_created_email`, `send_status_update_email`).

#### User routes — `backend/routes/user_routes.py` (Blueprint: `user_bp` → `/api/users`)
Key endpoints (representative):
- `GET /api/users/profile` — Returns the logged-in user's profile (`User.find_by_id`).
- `PUT /api/users/profile` — Update profile (`User.update_profile`).
- Admin-only endpoints: list students, create admin, reset passwords.

Connections:
- Uses models in `backend/models/user.py` for DB operations.

### 3.3 Models (DB access layer)

All models use `backend/config/database.py::Database.execute_query()` which:
- Uses `psycopg2` with `RealDictCursor` to return dict-like rows.
- Reads DB connection from environment variables (or `DATABASE_URL`).

Files:
- `backend/models/user.py` — CRUD for users (create, find_by_email, find_by_sr_code, find_by_id, get_all_students/admins, update_profile).
- `backend/models/concern.py` — Concern creation, queries, status history insertion (`add_status_history` is called after create).
- `backend/models/category.py` — Concern categories and office definitions (used by concern routes).

Why this design: Keeps SQL centralized in models so route handlers focus on validation and business logic.

### 3.4 Utilities (helpers)

- `backend/config/database.py` — DB connection manager and `execute_query()` with auto commit.
- `backend/config/config.py` — Loads configuration constants from env/config (Flask config, DB credentials, JWT secret/expiry, mail settings, upload folder).
- `backend/utils/auth.py` — Authentication helpers:
  - `hash_password` and `verify_password` (bcrypt)
  - `generate_token` and `decode_token` (JWT)
  - `token_required` and `admin_required` decorators that attach `request.user_id` and `request.user_role`.
- `backend/utils/email_service.py` — Flask-Mail wrapper with retry logic, templated HTML emails for events (concern created, status updated, resolved, comment notifications). Initialized by `init_mail(app)` in `app.py`.
- `backend/utils/email_verification.py` — Generates numeric verification codes and tokens, validation helpers, and functions to send verification emails (used in `auth_routes.register`).
- `backend/utils/google_auth.py` — Google OAuth helpers (generates auth URL, verifies token, exchanges code for user info), used by `auth_routes`.

### 3.5 Frontend (templates & static JS)

Files:
- `frontend/templates/*.html` — Jinja-style templates used by Flask `render_template()` calls. Serve the single-page UIs for login, register, student/admin dashboards, and verify-email page.
- `frontend/static/js/auth.js` — Handles login/register forms, Google Sign-In redirect flow, storing token in `localStorage` (or cookie), toggles UI, and shows alerts. Uses `API_BASE_URL = window.location.origin + '/api'` to call the backend.
- `frontend/static/css/styles.css` — Styling for pages.

How they connect:
- Frontend fetch calls send `Authorization: Bearer <token>` header for protected API calls.
- Frontend maps user actions to backend endpoints: e.g., `fetch('/api/auth/login')` and `fetch('/api/concerns')`.

---

## 4. Authentication Flow & Code Locations

1. Registration (`/api/auth/register`) — `backend/routes/auth_routes.py`:
   - Validates `sr_code`, email; hashes password via `backend/utils/auth.py::hash_password`; calls `User.create()` to insert.
   - Generates verification code using `backend/utils/email_verification.py::generate_verification_code()` and stores it in `users` via `Database.execute_query()`.
   - Sends verification email via `backend/utils/email_service.send_verification_code_email()`.

2. Login (`/api/auth/login`) — `backend/routes/auth_routes.py`:
   - Uses `User.find_by_email()` to get stored `password_hash`.
   - Verifies with `backend/utils/auth.verify_password()`.
   - If successful, issues JWT via `generate_token()`; token contains `user_id`, `role`, `exp`.

3. Protecting endpoints — `backend/utils/auth.token_required` decorator:
   - Checks `Authorization` header, decodes JWT with `Config.JWT_SECRET_KEY`, sets `request.user_id` and `request.user_role`.
   - `admin_required` wraps `token_required` and returns 403 if role not admin.

Why JWT: Stateless, scalable, server does not need session store. Token expiry is controlled via config.

---

## 5. Emailing System — How It Works & Where

Files:
- `backend/utils/email_service.py` — Main email functions, initialized with `init_mail(app)` in `backend/app.py`.
- `backend/utils/email_verification.py` — Verification code and email templates for registration.
- `backend/routes` — Calls to email functions appear in `auth_routes.py` (verification) and `concern_routes.py` (send emails on create/status updates/comments).

Key behavior in `email_service.py`:
- `mail = Mail()` configured via Flask app config keys: `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER`.
- `send_email(...)` implements retries and a `SKIP_EMAIL_SEND` environment flag to bypass sending in local dev.
- Templated HTML emails for `send_concern_created_email`, `send_status_update_email`, and other notifications.

Testing emails locally:
- Use `SKIP_EMAIL_SEND=True` to simulate sends.
- Or run a local SMTP debug server and set `MAIL_SERVER=localhost`.

---

## 6. Important Imports & Their Purpose

Below are the main frameworks/libraries used and where/how they are used in the project.

- `flask` (`Flask`, `render_template`, `request`, `jsonify`)
  - Purpose: Core web framework to handle HTTP requests, templating, and responses.
  - Files: `backend/app.py`, route files (`backend/routes/*.py`), templates rendering.

- `flask_cors.CORS`
  - Purpose: Enables Cross-Origin Resource Sharing for `/api/*` so frontend JS can call API endpoints (in development set to `*`).
  - File: `backend/app.py`.

- `flask_mail.Mail`, `flask_mail.Message`
  - Purpose: Sending emails via SMTP (verification, notifications).
  - File: `backend/utils/email_service.py`.

- `psycopg2`, `psycopg2.extras.RealDictCursor`
  - Purpose: PostgreSQL driver for Python. `RealDictCursor` returns rows as dicts for easier access.
  - File: `backend/config/database.py` (connection and `execute_query`).

- `bcrypt`
  - Purpose: Securely hashing passwords (salted). Used to store and verify user passwords.
  - File: `backend/utils/auth.py`.

- `jwt` (PyJWT)
  - Purpose: Encode and decode JWT tokens for stateless authentication.
  - File: `backend/utils/auth.py`.

- `werkzeug.utils.secure_filename`
  - Purpose: Sanitize uploaded file names to prevent path traversal or invalid characters.
  - File: `backend/routes/concern_routes.py`.

- `datetime`, `time` and `timedelta`
  - Purpose: Timestamps for created_at, updated_at, verification expirations, token expirations.
  - Files: models, routes, utils.

- `os` and `dotenv` (`load_dotenv` in WSGI) / environment variables
  - Purpose: Manage configuration (DB credentials, mail, secrets) outside code.
  - Files: `backend/config/config.py`, `backend/config/database.py`, `backend/app.py` (WSGI uses `load_dotenv`).

- `re` (regex)
  - Purpose: Input validation (e.g., SR-Code and email validation in `auth_routes.py`).

- `functools.wraps`
  - Purpose: Used in decorators (`token_required`, `admin_required`) to preserve function metadata.

- `flask_cors` and `Flask` config
  - Purpose: Set allowed origins and headers for API calls.

- `requests` / OAuth libraries (`google-auth`, `google-auth-oauthlib`) — used in `backend/utils/google_auth.py`.
  - Purpose: Interact with Google OAuth endpoints, exchange authorization codes, and validate Google tokens.

Note: For any library you mention during Q&A, be ready to explain why it was chosen (e.g., bcrypt for secure hashing, psycopg2 because the DB is PostgreSQL, Flask-Mail provides a simple interface to SMTP, JWT for stateless sessions).

---

## 7. Database & Trigger Notes (Important Defense Points)

- The DB schema is in `db/schema.sql` and is normalized to 3NF. Tables: `users`, `concerns`, `concern_categories`, `offices`, `concern_status_history`, `comments`, `notifications`, `attachments`.
- Ticket generation originally used `COUNT()` and caused duplicates; replaced with a robust `MAX()`-based approach using `SUBSTRING` to extract sequence numbers per year. See migration script `scripts/fix_ticket_trigger.py`.
- Triggers implemented:
  - `generate_ticket_number()` — auto-generate `ticket_number` in format `GRV-YYYY-XXXXX`.
  - `update_updated_at_column()` — update `updated_at` timestamp on update.
  - `log_status_change()` — insert rows into `concern_status_history` automatically when status changes.

Why it matters: The trigger approach guarantees consistent ticket numbering at the DB level and keeps business-critical logic close to the data.

---

## 8. Common Presentation Q&A Topics & Suggested Answers

Q: How do you secure user passwords?
- A: We use `bcrypt` to hash passwords with a strong salt (`bcrypt.gensalt()`), never storing plaintext. Password verification uses `bcrypt.checkpw()`.

Q: Why JWT instead of server-side sessions?
- A: JWTs are stateless and scale well with multiple nodes; tokens contain `user_id`, `role`, and expiration. For higher security, we can implement refresh tokens and token revocation lists.

Q: How do you prevent duplicate ticket numbers under concurrency?
- A: Ticket numbers are generated by a DB trigger using `MAX()` on existing ticket sequence for the year. This avoids COUNT() race conditions. For even higher concurrency or performance, sequence tables or a dedicated sequence generator could be used.

Q: How do you handle file uploads security?
- A: Filenames are sanitized with `secure_filename`. Uploads are stored in a dedicated `uploads/` directory with permissions set. Allowed file types and max size checks are enforced server-side.

Q: How are email failures handled?
- A: `send_email()` implements retries and a `SKIP_EMAIL_SEND` flag for development. Network errors log a simulated send; production should use a reliable SMTP provider and monitor logs.

Q: How is role-based access enforced?
- A: `token_required` decorator decodes the JWT and sets `request.user_role`. `admin_required` checks for `admin` role and returns 403 otherwise. Sensitive endpoints are protected with these decorators.

Q: How do you migrate database changes?
- A: SQL migration scripts live in `/db` and automated scripts exist under `/scripts`. Backups should be made with `pg_dump` before applying migrations.

Q: What are your scaling considerations?
- A: Move to managed DB, use connection pooling, add caching, offload static files to CDN, and implement pagination for large lists.

---

## 9. Debugging & Development Quick Commands

Activate venv (Windows PowerShell):

```powershell
& "venv\Scripts\Activate.ps1"
```

Run app locally:

```powershell
$env:FLASK_ENV = 'development'
python backend/app.py
# or
flask run --host=0.0.0.0 --port=5000
```

Run DB schema (Postgres):

```bash
psql -h <host> -U <user> -d <db> -f db/schema.sql
```

Seed sample data:

```bash
psql -h <host> -U <user> -d <db> -f db/seed_students.sql
```

Test email send in console (after activating venv):

```python
# python REPL
from backend.utils.email_service import send_email
send_email('your@example.com','Test','Hello')
```

---

## 10. Demo Checklist (what to show during the presentation)

- Show `README.md` and mention tech stack.
- Open `backend/app.py` and briefly point to where Blueprints are registered.
- Show `auth_routes.py` registration flow and `email_verification.py` generation.
- Show `concern_routes.py` create concern flow and `Concern.create()` in `models/concern.py`.
- Show `db/schema.sql` (explain ticket trigger and status history table).
- Run a demo: register → verify email → login → submit concern (with file) → log in as admin → change status → show email (if not possible, check server logs that simulate email send).
- Show logs (`backend/config/database.py` connection errors and `email_service.py` send logs) if anything fails.

---

## 11. Extra Notes & Tips for Defense

- Bring up the design trade-offs (why triggers for ticket generation vs application-level generation).
- Be prepared to explain data normalization and show UNF→1NF→2NF→3NF (we have `db/normalization_documentation.md`).
- Show the security measures (bcrypt, JWT, permission checks, file sanitization).
- Mention extensibility: adding surveys, multi-attachment storage (S3), or analytics dashboards.
- If asked about testing: describe manual tests (seed data scripts) and recommend unit tests for routes and models.
- If asked about concurrency: note DB-level constraints to maintain integrity and propose sequences or advisory locks for heavier loads.

---

## 12. Where to Read Code (Quick Links)

- `backend/app.py` — app factory, blueprint registration, frontend routes
- `backend/routes/auth_routes.py` — registration, login, verification, Google SSO
- `backend/routes/concern_routes.py` — create/list/update concerns, file uploads
- `backend/routes/user_routes.py` — profile and admin user endpoints
- `backend/models/user.py` — user SQL and helper methods
- `backend/models/concern.py` — concern SQL and status history logging
- `backend/config/database.py` — DB connection manager (psycopg2)
- `backend/config/config.py` — environment-driven configuration constants
- `backend/utils/auth.py` — bcrypt + JWT + decorators
- `backend/utils/email_service.py` — Flask-Mail templates and send logic
- `backend/utils/email_verification.py` — verification code generation
- `frontend/templates/` — HTML templates
- `frontend/static/js/auth.js` — frontend auth and API calls
- `db/schema.sql` — full DB schema, triggers, indexes
- `db/seed_students.sql`, `db/generate_sample_concerns.py` — sample data

---

## 13. Next Steps (if time allows)

- Add a short suite of unit tests for `auth_routes` and `concern_routes`.
- Add Postman collection or API documentation (Swagger) for endpoints.
- Create a short video demo and include screenshots inside `docs/`.

---

Good luck with your presentation and defense — tell the panel you focused on secure authentication, data integrity, and clear separation of concerns. If you want, I can also generate a short slide outline or a Postman collection next.
