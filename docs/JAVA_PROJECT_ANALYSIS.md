# SSC Student Welfare System - Complete Java Project Analysis

## Executive Summary
This is a **Student Grievance Management System** for the Student Supreme Council (SSC) that allows students to file concerns/complaints and administrators to manage them. The system uses a console-based UI with role-based access control.

---

## 1. KEY FEATURES & FUNCTIONALITIES

### Main System Features
1. **Student Registration System**
   - Register new students with SR-Code validation
   - Validates against campus registry (students.json)
   - Password hashing (SHA-256) for security
   - Email format validation

2. **Authentication System**
   - Student login (SR-Code + Password)
   - Admin login (Username + Password)
   - Password change functionality
   - Password reset by admin

3. **Grievance Management**
   - Students can file concerns/grievances
   - Admins can view all concerns
   - Admins can update concern status
   - Admins can delete concerns
   - Track concern status (Submitted → Under Review → In Progress → Resolved)

4. **Data Persistence**
   - JSON file-based storage
   - `students.json` - stores all registered students
   - `grievances.json` - stores all filed concerns
   - Auto-save on create/update/delete operations

---

## 2. DATA MODELS (Classes)

### 2.1 User (Abstract Parent Class)
**Purpose:** Base class for all system users

**Fields:**
- `username` (String, protected)
- `password` (String, protected) - stores hashed password
- `name` (String, protected)

**Methods:**
- `getUsername()` - returns username
- `getPassword()` - returns hashed password
- `getName()` - returns full name
- `setPassword(String)` - updates password
- `displayInfo()` - **ABSTRACT** - display user information
- `getRole()` - **ABSTRACT** - returns user role

**Design Pattern:** Template Method Pattern (abstract methods implemented by subclasses)

---

### 2.2 Student (extends User)
**Purpose:** Represents a student user

**Additional Fields:**
- `srCode` (String, private) - Student Registration Code (format: ##-#####)
- `email` (String, private) - Student email address

**Constructor:**
```java
Student(String srCode, String name, String email, String password)
```

**Methods:**
- `getSrCode()` - returns SR-Code
- `getEmail()` - returns email
- `displayInfo()` - displays all student information
- `getRole()` - returns "Student"

**Business Rules:**
- SR-Code serves as username
- SR-Code must follow format: `##-#####` (e.g., 24-31688)
- SR-Code must exist in campus registry for registration
- Password is hashed using SHA-256

---

### 2.3 Admin (extends User)
**Purpose:** Represents an administrator user

**Constructor:**
- Default constructor: creates default admin (username: "admin", password: "admin")
- Custom constructor: creates custom admin with parameters

**Methods:**
- `displayInfo()` - displays admin information
- `getRole()` - returns "Administrator"
- `viewAllConcerns(ArrayList<Grievance>)` - displays all grievances
- `updateConcern(ArrayList<Grievance>)` - updates grievance status and feedback
- `deleteConcern(ArrayList<Grievance>)` - deletes a grievance by ID

**Business Rules:**
- Default admin credentials: username="admin", password="admin" (plain text)
- Admin passwords are NOT hashed (only student passwords are)

---

### 2.4 Grievance
**Purpose:** Represents a student concern/complaint

**Fields:**
- `grievanceId` (int, private) - auto-incremented ID
- `studentSr` (String, private) - SR-Code of student who filed
- `title` (String, private) - concern title
- `category` (String, private) - concern category
- `description` (String, private) - detailed description
- `status` (String, private) - current status
- `feedback` (String, private) - officer feedback

**Static Field:**
- `nextId` (int, static) - auto-increment counter

**Constructor:**
```java
Grievance(String studentSr, String title, String category, String description)
```

**Default Values:**
- `status` = "Submitted"
- `feedback` = "None"
- `grievanceId` = auto-incremented

**Methods:**
- Getters for all fields
- `setStatus(String)` - updates status
- `setFeedback(String)` - updates feedback
- `display()` - prints all grievance information

**Valid Status Values:**
- "Submitted" (default)
- "Under Review"
- "In Progress"
- "Resolved"

**Grievance Categories:**
1. Academic / Akademiko
2. Administrative Decisions / Desisyong Administratibo
3. Service and Facilities / Serbisyo at Pasilidad
4. Harrassment / Panghaharas
5. Others

---

### 2.5 AppData
**Purpose:** Container class for application data

**Fields:**
- `students` (ArrayList<Student>)
- `grievances` (ArrayList<Grievance>)

**Methods:**
- `getStudents()` - returns student list
- `getGrievances()` - returns grievance list

---

## 3. SERVICE METHODS

### 3.1 AuthService (Authentication & User Management)
**Purpose:** Handles all authentication logic

#### Student Authentication Methods:
- **`authenticateStudent(students, srCode, password)`**
  - Hashes input password with SHA-256
  - Compares against stored hash
  - Returns Student object if valid, null otherwise

- **`findStudentBySrCode(students, srCode)`**
  - Searches student list by SR-Code
  - Returns Student if found, null otherwise

- **`isDuplicateStudent(students, srCode)`**
  - Checks if SR-Code already registered
  - Returns boolean

- **`isValidSrCodeFormat(srCode)`**
  - Validates SR-Code format using regex: `\d{2}-\d{5}`
  - Returns boolean

#### Admin Authentication Methods:
- **`authenticateAdmin(username, password)`**
  - Compares plain text credentials
  - Default: username="admin", password="admin"
  - Returns boolean

#### Password Operations:
- **`changePassword(student, currentPassword, newPassword, confirmPassword)`**
  - Validates current password
  - Checks if new passwords match
  - Checks if new password is not empty
  - Updates password with hashed value
  - Returns boolean (success/failure)

- **`resetStudentPassword(students, srCode)`**
  - Resets password to SR-Code (hashed)
  - Admin-only operation
  - Auto-saves to file

**Constants:**
- `DEFAULT_ADMIN_USERNAME` = "admin"
- `DEFAULT_ADMIN_PASSWORD` = "admin"
- `SR_CODE_PATTERN` = "\\d{2}-\\d{5}"

---

### 3.2 StudentService (Student Operations)
**Purpose:** Handles student-specific operations

#### Registration:
- **`registerStudent(students)`**
  - Prompts for student information
  - Validates SR-Code format
  - Checks for duplicates
  - Validates against campus registry
  - Validates email format
  - Hashes password
  - Creates and saves new Student
  - Shows loading animation

**Registration Validation Rules:**
1. SR-Code must match format `##-#####`
2. SR-Code must not be already registered
3. SR-Code must exist in campus registry (students.json)
4. Email must be valid format

#### Validation:
- **`validateRegisteredStudents(students)`**
  - Validates all registered students
  - Checks SR-Code against registry
  - Checks email format
  - Generates validation report:
    - Total registered
    - Fully valid count
    - Invalid SR-Code count
    - Invalid email count
    - Registry size

#### Grievance Operations:
- **`fileConcern(student, grievances)`**
  - Displays 5 category options
  - Prompts for title and description
  - Creates new Grievance with status="Submitted"
  - Auto-saves to file
  - Shows success message

- **`viewMyConcerns(student, grievances)`**
  - Filters grievances by student's SR-Code
  - Displays all matching grievances
  - Shows "No concerns found" if empty

**Helper Method:**
- `getCategoryName(int)` - converts category number to name

---

## 4. MENU OPTIONS & USER FLOWS

### 4.1 Main Menu (MenuHandler)
**Entry Point:** `runMainMenu(students, grievances)`

**Options:**
1. Student Login
2. Register Student
3. Admin Login
4. Exit

---

### 4.2 Student Login Flow
**Process:**
1. Prompt for SR-Code
2. Prompt for Password
3. Show loading spinner
4. Authenticate using `AuthService.authenticateStudent()`
5. If successful → Student Dashboard
6. If failed → Show error message

---

### 4.3 Student Dashboard Menu
**Available after successful student login**

**Options:**
1. **File a Concern**
   - Select category (1-5)
   - Enter title
   - Enter description
   - Submit (auto-saved)

2. **View My Concerns**
   - Display all concerns filed by logged-in student
   - Shows: ID, Title, Category, Description, Status, Feedback

3. **Change Password**
   - Enter current password
   - Enter new password
   - Confirm new password
   - Validate and update

4. **Logout**
   - Return to main menu

---

### 4.4 Admin Login Flow
**Process:**
1. Prompt for Admin Username
2. Prompt for Password
3. Show loading spinner
4. Authenticate using `AuthService.authenticateAdmin()`
5. If successful → Admin Dashboard
6. If failed → Show error message

---

### 4.5 Admin Dashboard Menu
**Available after successful admin login**

**Options:**
1. **View All Concerns**
   - Display all submitted grievances
   - Shows all fields for each grievance

2. **Update Concerns**
   - Prompt for Grievance ID
   - Enter new status
   - Enter feedback from officer
   - Auto-save changes

3. **Delete Concern**
   - Prompt for Grievance ID
   - Confirm deletion (yes/no)
   - Remove from list and auto-save

4. **Validate Registered Students**
   - Run validation on all students
   - Show validation report

5. **Reload SR Registry**
   - Reload campus registry from students.json
   - Show total entries loaded

6. **Reset Student Password**
   - Prompt for SR-Code
   - Reset password to SR-Code (hashed)
   - Auto-save

7. **Logout**
   - Return to main menu

---

## 5. VALIDATION RULES

### 5.1 StudentValidator
**Purpose:** Validates student data against campus registry and email format

#### Registry Management:
- **`loadFromFile()`**
  - Reads students.json file
  - Extracts all SR-Codes using regex
  - Stores in HashSet for O(1) lookup
  - Format: parses JSON objects with "sr" field

- **`reloadRegistry()`**
  - Clears and reloads registry
  - Can be called at runtime

- **`registrySize()`**
  - Returns count of valid SR-Codes in registry

#### Validation Methods:
- **`isCampusStudent(srCode)`**
  - Checks if SR-Code exists in campus registry
  - Returns boolean

- **`isValidEmail(email)`**
  - Validates email format using regex
  - Pattern: `^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}$`
  - Returns boolean

**Data Structure:**
- `VALID_SR_CODES` (HashSet<String>, static) - in-memory registry

**Email Validation Rules:**
- Must contain @ symbol
- Must have domain and TLD
- Alphanumeric characters, dots, hyphens, underscores allowed
- TLD must be 2-6 characters

---

### 5.2 PasswordUtils
**Purpose:** Password hashing utilities

#### Hashing:
- **`hash(input)`**
  - Uses SHA-256 algorithm
  - Returns hex string representation
  - Returns null if input is null
  - Handles exceptions gracefully

**Implementation:**
```java
MessageDigest md = MessageDigest.getInstance("SHA-256");
byte[] hash = md.digest(input.getBytes(StandardCharsets.UTF_8));
// Convert bytes to hex string
```

**Security Notes:**
- SHA-256 is one-way hashing (cannot be reversed)
- Same input always produces same hash
- Student passwords are hashed
- Admin passwords are NOT hashed (security flaw)

---

## 6. DATA PERSISTENCE (DataManager)

### 6.1 File Structure

**Files:**
- `students.json` - stores all registered students
- `grievances.json` - stores all filed grievances

**JSON Format - Students:**
```json
[
  {
    "sr": "24-31688",
    "name": "John Doe",
    "email": "john@example.com",
    "passwordHash": "9e16d6a28ac1f7396192162e2daf7360c8d4fc2a..."
  }
]
```

**JSON Format - Grievances:**
```json
[
  {
    "id": 1,
    "studentSR": "24-31688",
    "title": "Concern Title",
    "category": "Academic / Akademiko",
    "description": "Description here",
    "status": "Submitted",
    "feedback": "None"
  }
]
```

---

### 6.2 DataManager Methods

#### Application Data Loading:
- **`loadApplicationData()`**
  - Loads both students and grievances
  - Reloads campus registry
  - Returns AppData object
  - Called at application startup

#### Student Operations:
- **`loadStudents()`**
  - Reads students.json file
  - Parses JSON using regex (no external library)
  - Creates Student objects
  - Skips duplicates
  - Returns ArrayList<Student>

- **`saveStudents(students)`**
  - Writes students.json file
  - Overwrites entire file (no append)
  - Formats as JSON array
  - Escapes special characters

#### Grievance Operations:
- **`loadGrievances()`**
  - Reads grievances.json file
  - Parses JSON using regex
  - Creates Grievance objects
  - Returns ArrayList<Grievance>

- **`saveGrievances(grievances)`**
  - Writes grievances.json file
  - Overwrites entire file
  - Formats as JSON array
  - Escapes special characters

#### JSON Helpers:
- **`parseStudentFromJson(jsonText)`**
  - Extracts fields from JSON string
  - Validates SR-Code format
  - Returns Student or null

- **`parseGrievanceFromJson(jsonText)`**
  - Extracts fields from JSON string
  - Returns Grievance or null

- **`buildStudentJson(student)`**
  - Converts Student to JSON string

- **`buildGrievanceJson(grievance)`**
  - Converts Grievance to JSON string

- **`extractJsonField(jsonText, field)`**
  - Uses regex to extract field value
  - Pattern: `"field"\s*:\s*"(.*?)"`

- **`escapeJson(s)`**
  - Escapes backslashes, quotes, newlines
  - Prevents JSON injection

---

### 6.3 Data Persistence Patterns

**When Data is Saved:**
1. Student registration → auto-saves students
2. Password change → auto-saves students
3. Password reset → auto-saves students
4. File concern → auto-saves grievances
5. Update concern → auto-saves grievances
6. Delete concern → auto-saves grievances

**Load Strategy:**
- Load all data at startup
- Keep in memory during runtime
- Save immediately after changes

**File I/O:**
- No external JSON library used
- Custom regex-based parsing
- Synchronous file operations
- No file locking mechanism

---

## 7. UI/UX COMPONENTS

### 7.1 Utility Class (UI Helpers)
**Purpose:** Provides UI utilities and input handling

#### Screen Management:
- **`clearScreen()`** - clears console (OS-dependent)
- **`getConsoleWidth()`** - detects terminal width (defaults to 80)
- **`printCentered(text)`** - centers text horizontally
- **`printCenteredInline(text)`** - centers without newline

#### UI Elements:
- **`printTitle(title)`** - displays boxed title with box-drawing characters
- **`printMenu(options)`** - displays vertical menu centered
- **`waitForEnter(prompt)`** - waits for user to press Enter

#### Input Methods:
- **`promptCenteredString(prompt)`** - reads string input
- **`promptCenteredInt(prompt)`** - reads integer (returns 0 on error)
- **`promptCenteredPassword(prompt)`** - reads password with asterisk masking

#### Loading Animations:
- **`loadingScreen()`** - shows loading spinner
- **`spinner(message, duration)`** - animated spinner
- **`overlaySpinner(message, duration)`** - in-place spinner (no vertical growth)
- **`loadingBar(message, duration, steps)`** - progress bar

**Special Features:**
- Password masking using separate thread
- Box-drawing characters for borders (╔╗╚╝═║)
- Auto-adjusts to terminal width
- OS-detection for screen clearing

---

### 7.2 UIHelper Class (User Messages)
**Purpose:** Standardized user feedback messages

#### Message Methods:
- **`showInvalidChoice(min, max)`** - invalid menu selection
- **`showError(message)`** - error message with prompt
- **`showSuccess(message)`** - success message with prompt
- **`showLoginSuccess(name)`** - welcome message after login
- **`exitProgram()`** - goodbye message with spinner

**Message Format:**
- All messages are centered
- Includes blank lines for spacing
- Includes "Press Enter to continue..." prompt
- Uses checkmark (✓) for success messages

---

## 8. SPECIAL BUSINESS LOGIC

### 8.1 SR-Code Registry System
**Purpose:** Validates student registration against campus database

**How it Works:**
1. Campus maintains a list of valid SR-Codes in students.json
2. System loads this registry at startup
3. During registration, SR-Code is checked against registry
4. Only students with valid SR-Codes can register
5. Admin can reload registry at runtime

**Benefits:**
- Prevents unauthorized registrations
- Maintains data integrity
- Easy to update (just modify JSON file)

---

### 8.2 Auto-Increment Grievance IDs
**Implementation:**
```java
private static int nextId = 1;
public Grievance(...) {
    this.grievanceId = nextId++;
}
```

**Problem:** IDs reset when program restarts
**Solution Needed:** Load max ID from file on startup

---

### 8.3 Password Security
**Current Implementation:**
- Student passwords: SHA-256 hashed
- Admin passwords: Plain text
- Password reset: resets to SR-Code

**Security Issues:**
1. Admin password is plain text
2. SHA-256 without salt is vulnerable to rainbow tables
3. No password strength requirements
4. No rate limiting on login attempts

---

### 8.4 Data Validation Flow
**Registration Process:**
1. Check SR-Code format (regex)
2. Check for duplicates (in-memory list)
3. Check campus registry (file-based)
4. Validate email format (regex)
5. Hash password (SHA-256)
6. Create student object
7. Save to file

---

## 9. ARCHITECTURE PATTERNS

### 9.1 Design Patterns Used

**1. Template Method Pattern**
- User class with abstract methods
- Student and Admin implement specific behavior

**2. Service Layer Pattern**
- AuthService, StudentService
- Separates business logic from UI

**3. Data Transfer Object (DTO)**
- AppData class carries related data

**4. Helper/Utility Pattern**
- Utility, UIHelper, PasswordUtils
- Static methods for common operations

**5. Menu-Driven Architecture**
- MenuHandler manages navigation
- Centralized menu logic

---

### 9.2 Code Organization

```
Main.java                     # Entry point
├── DataManager              # Data persistence
├── MenuHandler              # Navigation
    ├── AuthService          # Authentication
    ├── StudentService       # Student operations
    └── Admin                # Admin operations
Models:
├── User (abstract)
├── Student
├── Admin
└── Grievance
Utilities:
├── Utility                  # UI helpers
├── UIHelper                 # Messages
├── PasswordUtils            # Hashing
└── StudentValidator         # Validation
```

---

## 10. PYTHON FLASK REPLICATION GUIDE

### 10.1 Required Python Dependencies
```
Flask
Flask-CORS
psycopg2-binary  # If using PostgreSQL
python-dotenv
bcrypt           # For password hashing (better than SHA-256)
PyJWT            # For JWT authentication
Werkzeug         # For file handling
```

### 10.2 Model Mapping (Java → Python)

**User (Abstract) → SQLAlchemy Base Model**
```python
class User(db.Model):
    __abstract__ = True
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))  # hashed
    name = db.Column(db.String(100))
```

**Student → Student Model**
```python
class Student(User):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    sr_code = db.Column(db.String(10), unique=True)  # ##-#####
    email = db.Column(db.String(100))
    role = 'student'
```

**Admin → Admin Model**
```python
class Admin(User):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    role = 'admin'
```

**Grievance → Concern Model**
```python
class Concern(db.Model):
    __tablename__ = 'concerns'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_sr = db.Column(db.String(10), db.ForeignKey('students.sr_code'))
    title = db.Column(db.String(200))
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='Submitted')
    feedback = db.Column(db.Text, default='None')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

---

### 10.3 API Endpoints Mapping

**Authentication Endpoints:**
- `POST /api/auth/register` → StudentService.registerStudent()
- `POST /api/auth/login` → AuthService.authenticateStudent()
- `POST /api/auth/admin/login` → AuthService.authenticateAdmin()
- `POST /api/auth/change-password` → AuthService.changePassword()
- `POST /api/auth/reset-password` → AuthService.resetStudentPassword()

**Student Endpoints:**
- `POST /api/concerns` → StudentService.fileConcern()
- `GET /api/concerns/my` → StudentService.viewMyConcerns()
- `GET /api/students/validate` → StudentService.validateRegisteredStudents()

**Admin Endpoints:**
- `GET /api/admin/concerns` → Admin.viewAllConcerns()
- `PUT /api/admin/concerns/:id` → Admin.updateConcern()
- `DELETE /api/admin/concerns/:id` → Admin.deleteConcern()
- `POST /api/admin/registry/reload` → StudentValidator.reloadRegistry()

---

### 10.4 Validation Rules Implementation

**SR-Code Validation:**
```python
import re
SR_CODE_PATTERN = r'^\d{2}-\d{5}$'
def validate_sr_code(sr_code):
    return bool(re.match(SR_CODE_PATTERN, sr_code))
```

**Email Validation:**
```python
EMAIL_PATTERN = r'^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}$'
def validate_email(email):
    return bool(re.match(EMAIL_PATTERN, email))
```

**Password Hashing (use bcrypt instead of SHA-256):**
```python
import bcrypt
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
```

---

### 10.5 Grievance Categories (Constants)
```python
CATEGORIES = [
    "Academic / Akademiko",
    "Administrative Decisions / Desisyong Administratibo",
    "Service and Facilities / Serbisyo at Pasilidad",
    "Harrassment / Panghaharas",
    "Others"
]

STATUS_OPTIONS = [
    "Submitted",
    "Under Review",
    "In Progress",
    "Resolved"
]
```

---

### 10.6 Key Differences (Java vs Flask)

| Feature | Java Implementation | Flask Implementation |
|---------|-------------------|---------------------|
| Data Storage | JSON files | PostgreSQL database |
| Password Hashing | SHA-256 | bcrypt (more secure) |
| Authentication | Session-based (in-memory) | JWT tokens |
| API | Console menu-driven | RESTful API |
| Validation | Manual regex | Flask-WTF validators |
| Error Handling | Try-catch blocks | Flask error handlers |
| Concurrency | Single-threaded | Multi-threaded (WSGI) |

---

### 10.7 Additional Features to Add (Improvements)

**Security Enhancements:**
1. JWT-based authentication
2. Password strength validation
3. Rate limiting on login attempts
4. CSRF protection
5. Input sanitization

**Features:**
1. Timestamps for concerns (created_at, updated_at)
2. File attachments for concerns
3. Email notifications
4. Concern assignment to officers
5. Concern history/audit log
6. Search and filter concerns
7. Pagination for large datasets
8. User profile management

**Admin Features:**
1. User management (suspend/activate accounts)
2. Reports and analytics
3. Export data (CSV, PDF)
4. Bulk operations
5. Activity logs

---

## 11. SUMMARY OF ALL FUNCTIONALITIES

### Student Capabilities:
✓ Register with SR-Code validation  
✓ Login with SR-Code and password  
✓ File concerns/grievances (5 categories)  
✓ View own submitted concerns  
✓ Check concern status and feedback  
✓ Change password  

### Admin Capabilities:
✓ Login with admin credentials  
✓ View all submitted concerns  
✓ Update concern status (Submitted/Under Review/In Progress/Resolved)  
✓ Add feedback to concerns  
✓ Delete concerns  
✓ Validate registered students  
✓ Reload SR-Code registry  
✓ Reset student passwords  

### System Features:
✓ SR-Code registry validation  
✓ Email format validation  
✓ Password hashing (SHA-256)  
✓ Auto-increment grievance IDs  
✓ JSON-based data persistence  
✓ Console-based UI with animations  
✓ Centered text and box-drawing characters  
✓ Loading spinners and progress bars  
✓ Role-based access control  

---

## 12. FILE-BY-FILE BREAKDOWN

1. **Main.java** - Entry point, loads data and starts menu
2. **User.java** - Abstract base class for users
3. **Student.java** - Student model with SR-Code
4. **Admin.java** - Admin model with management methods
5. **Grievance.java** - Concern/complaint model
6. **AppData.java** - Data container
7. **AuthService.java** - Authentication logic
8. **StudentService.java** - Student operations
9. **MenuHandler.java** - Navigation and menu system
10. **DataManager.java** - File I/O operations
11. **StudentValidator.java** - Registry and email validation
12. **PasswordUtils.java** - SHA-256 hashing
13. **Utility.java** - UI helpers and input methods
14. **UIHelper.java** - User messages

---

## CONCLUSION

This is a well-structured console application with:
- Clear separation of concerns
- Service layer architecture
- Data validation
- File-based persistence
- Role-based access control

**Ready for Flask Migration:** All business logic, validation rules, and data structures are clearly defined and can be replicated in your Flask backend.

**Next Steps:**
1. Create SQLAlchemy models matching the data structures
2. Implement RESTful API endpoints
3. Add JWT authentication
4. Migrate validation logic
5. Create database schema
6. Test all endpoints
7. Build frontend to consume API
