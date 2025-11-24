# Database Normalization Documentation
## Student Grievance Reporting and Tracking System

---

## Table of Contents
1. [Unnormalized Form (UNF)](#unnormalized-form-unf)
2. [First Normal Form (1NF)](#first-normal-form-1nf)
3. [Second Normal Form (2NF)](#second-normal-form-2nf)
4. [Third Normal Form (3NF)](#third-normal-form-3nf)

---

## Unnormalized Form (UNF)

### Initial Data Structure (Before Normalization)

In the unnormalized form, all data would be stored in a single table with repeating groups and multi-valued attributes.

```
STUDENT_GRIEVANCE_SYSTEM
├─ SR_Code
├─ Student_Email
├─ Student_Password
├─ Student_First_Name
├─ Student_Last_Name
├─ Student_Middle_Name
├─ Student_Program
├─ Student_Year_Level
├─ Concern_Ticket_Number
├─ Concern_Title
├─ Concern_Description
├─ Concern_Location
├─ Concern_Incident_Date
├─ Concern_Category_Name
├─ Concern_Category_Description
├─ Concern_Status
├─ Concern_Priority
├─ Concern_Created_At
├─ Office_Name
├─ Office_Email
├─ Office_Contact_Number
├─ Admin_SR_Code
├─ Admin_Name
├─ Admin_Email
├─ Status_History (Multiple Values: [status1, date1, admin1], [status2, date2, admin2], ...)
├─ Comments (Multiple Values: [comment1, date1, user1], [comment2, date2, user2], ...)
├─ Attachments (Multiple Values: [file1, date1], [file2, date2], ...)
├─ Notifications (Multiple Values: [notif1, date1, read1], [notif2, date2, read2], ...)
└─ Resolution_Notes
```

### Example UNF Data (Single Row):

| SR_Code | Student_Name | Concern_Title | Category | Status_History | Comments | Attachments |
|---------|--------------|---------------|----------|----------------|----------|-------------|
| 21-12345 | Juan Dela Cruz | Broken AC | Services & Facilities | [pending, 2025-11-01], [in-review, 2025-11-02], [resolved, 2025-11-05] | [Need repair ASAP, 2025-11-01, Student], [Assigned to facilities, 2025-11-02, Admin] | [photo1.jpg, 2025-11-01], [report.pdf, 2025-11-02] |

**Problems with UNF:**
- ❌ Repeating groups (Status_History, Comments, Attachments)
- ❌ Multi-valued attributes in single cells
- ❌ Data redundancy (student info repeated for each concern)
- ❌ Update anomalies
- ❌ Difficult to query and maintain
- ❌ No data integrity

---

## First Normal Form (1NF)

### Rules for 1NF:
1. ✅ Eliminate repeating groups
2. ✅ Create separate rows for each set of related data
3. ✅ Identify primary key
4. ✅ Each cell contains only atomic (single) values

### 1NF Tables:

#### Table: STUDENT_CONCERNS_1NF

```sql
STUDENT_CONCERNS_1NF (
    Record_ID,                    -- Primary Key
    SR_Code,
    Student_Email,
    Student_Password,
    Student_First_Name,
    Student_Last_Name,
    Student_Middle_Name,
    Student_Program,
    Student_Year_Level,
    Concern_Ticket_Number,
    Concern_Title,
    Concern_Description,
    Concern_Location,
    Concern_Incident_Date,
    Concern_Category_Name,
    Concern_Category_Description,
    Concern_Status,
    Concern_Priority,
    Concern_Created_At,
    Office_Name,
    Office_Email,
    Office_Contact_Number,
    Admin_SR_Code,
    Admin_First_Name,
    Admin_Last_Name,
    Admin_Email,
    Status_Change_Old,
    Status_Change_New,
    Status_Change_Date,
    Status_Change_By,
    Comment_Text,
    Comment_Date,
    Comment_By,
    Attachment_Name,
    Attachment_Path,
    Attachment_Date,
    Notification_Title,
    Notification_Message,
    Notification_Date,
    Notification_Read,
    Resolution_Notes
)
```

### Example 1NF Data:

| Record_ID | SR_Code | Student_Name | Concern_Title | Category | Status_Old | Status_New | Comment_Text | Attachment |
|-----------|---------|--------------|---------------|----------|------------|------------|--------------|------------|
| 1 | 21-12345 | Juan | Broken AC | Facilities | NULL | pending | Need repair | photo1.jpg |
| 2 | 21-12345 | Juan | Broken AC | Facilities | NULL | pending | Need repair | report.pdf |
| 3 | 21-12345 | Juan | Broken AC | Facilities | pending | in-review | Assigned | photo1.jpg |
| 4 | 21-12345 | Juan | Broken AC | Facilities | pending | in-review | Assigned | report.pdf |
| 5 | 21-12345 | Juan | Broken AC | Facilities | in-review | resolved | Fixed | photo1.jpg |

**Improvements:**
- ✅ No multi-valued attributes
- ✅ Each cell contains atomic values
- ✅ Has primary key (Record_ID)

**Remaining Problems:**
- ❌ Massive data redundancy (student info repeated)
- ❌ Update anomalies (changing student email requires multiple updates)
- ❌ Insertion anomalies (can't add student without concern)
- ❌ Deletion anomalies (deleting concern deletes student info)
- ❌ Partial dependencies (student info depends only on SR_Code, not full key)

---

## Second Normal Form (2NF)

### Rules for 2NF:
1. ✅ Must be in 1NF
2. ✅ Remove partial dependencies
3. ✅ All non-key attributes must depend on the entire primary key

### 2NF Tables:

#### Table 1: USERS_2NF
```sql
USERS_2NF (
    User_ID,                      -- Primary Key
    SR_Code,
    Email,
    Password_Hash,
    First_Name,
    Last_Name,
    Middle_Name,
    Program,
    Year_Level,
    Role
)
```

#### Table 2: CONCERNS_2NF
```sql
CONCERNS_2NF (
    Concern_ID,                   -- Primary Key
    Student_User_ID,              -- Foreign Key → USERS_2NF
    Admin_User_ID,                -- Foreign Key → USERS_2NF
    Ticket_Number,
    Title,
    Description,
    Location,
    Incident_Date,
    Category_Name,
    Category_Description,
    Office_Name,
    Office_Email,
    Office_Contact_Number,
    Status,
    Priority,
    Created_At,
    Resolution_Notes
)
```

#### Table 3: STATUS_HISTORY_2NF
```sql
STATUS_HISTORY_2NF (
    History_ID,                   -- Primary Key
    Concern_ID,                   -- Foreign Key → CONCERNS_2NF
    Changed_By_User_ID,           -- Foreign Key → USERS_2NF
    Old_Status,
    New_Status,
    Changed_At,
    Remarks
)
```

#### Table 4: COMMENTS_2NF
```sql
COMMENTS_2NF (
    Comment_ID,                   -- Primary Key
    Concern_ID,                   -- Foreign Key → CONCERNS_2NF
    User_ID,                      -- Foreign Key → USERS_2NF
    Comment_Text,
    Is_Internal,
    Created_At
)
```

#### Table 5: ATTACHMENTS_2NF
```sql
ATTACHMENTS_2NF (
    Attachment_ID,                -- Primary Key
    Concern_ID,                   -- Foreign Key → CONCERNS_2NF
    Uploaded_By_User_ID,          -- Foreign Key → USERS_2NF
    File_Name,
    File_Path,
    File_Type,
    File_Size,
    Created_At
)
```

#### Table 6: NOTIFICATIONS_2NF
```sql
NOTIFICATIONS_2NF (
    Notification_ID,              -- Primary Key
    User_ID,                      -- Foreign Key → USERS_2NF
    Concern_ID,                   -- Foreign Key → CONCERNS_2NF
    Notification_Type,
    Title,
    Message,
    Is_Read,
    Read_At,
    Created_At
)
```

### Example 2NF Data:

**USERS_2NF:**
| User_ID | SR_Code | Email | First_Name | Last_Name | Role |
|---------|---------|-------|------------|-----------|------|
| 1 | 21-12345 | juan@g.batstate-u.edu.ph | Juan | Dela Cruz | student |
| 2 | 00-00000 | admin@ssc.batstateu.edu.ph | Admin | User | admin |

**CONCERNS_2NF:**
| Concern_ID | Student_User_ID | Ticket_Number | Title | Category_Name | Office_Name | Status |
|------------|-----------------|---------------|-------|---------------|-------------|--------|
| 1 | 1 | GRV-2025-00001 | Broken AC | Services & Facilities | Facility Management | resolved |

**STATUS_HISTORY_2NF:**
| History_ID | Concern_ID | Old_Status | New_Status | Changed_At | Changed_By_User_ID |
|------------|------------|------------|------------|------------|-------------------|
| 1 | 1 | NULL | pending | 2025-11-01 | 1 |
| 2 | 1 | pending | in-review | 2025-11-02 | 2 |
| 3 | 1 | in-review | resolved | 2025-11-05 | 2 |

**Improvements:**
- ✅ No partial dependencies
- ✅ Significantly reduced redundancy
- ✅ Each table focuses on a specific entity
- ✅ Easier to update user information

**Remaining Problems:**
- ❌ Transitive dependencies still exist
  - Category_Description depends on Category_Name (not primary key)
  - Office_Email depends on Office_Name (not primary key)
- ❌ Update anomalies (changing category description requires updating multiple concerns)

---

## Third Normal Form (3NF)

### Rules for 3NF:
1. ✅ Must be in 2NF
2. ✅ Remove transitive dependencies
3. ✅ All non-key attributes must depend ONLY on the primary key

### 3NF Tables (Final Normalized Schema):

#### Table 1: users
```sql
users (
    user_id SERIAL PRIMARY KEY,
    sr_code VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    program VARCHAR(100),
    year_level INTEGER,
    role VARCHAR(20) NOT NULL DEFAULT 'student',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### Table 2: concern_categories
```sql
concern_categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### Table 3: offices
```sql
offices (
    office_id SERIAL PRIMARY KEY,
    office_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    contact_email VARCHAR(255),
    contact_number VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### Table 4: concerns
```sql
concerns (
    concern_id SERIAL PRIMARY KEY,
    ticket_number VARCHAR(50) UNIQUE NOT NULL,
    student_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    assigned_office_id INTEGER,
    assigned_admin_id INTEGER,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(255),
    incident_date DATE,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    priority VARCHAR(20) DEFAULT 'normal',
    is_anonymous BOOLEAN DEFAULT FALSE,
    resolution_notes TEXT,
    resolved_at TIMESTAMP,
    resolved_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (student_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES concern_categories(category_id),
    FOREIGN KEY (assigned_office_id) REFERENCES offices(office_id),
    FOREIGN KEY (assigned_admin_id) REFERENCES users(user_id),
    FOREIGN KEY (resolved_by) REFERENCES users(user_id)
)
```

#### Table 5: concern_status_history
```sql
concern_status_history (
    history_id SERIAL PRIMARY KEY,
    concern_id INTEGER NOT NULL,
    old_status VARCHAR(50),
    new_status VARCHAR(50) NOT NULL,
    changed_by INTEGER NOT NULL,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (concern_id) REFERENCES concerns(concern_id),
    FOREIGN KEY (changed_by) REFERENCES users(user_id)
)
```

#### Table 6: comments
```sql
comments (
    comment_id SERIAL PRIMARY KEY,
    concern_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    comment_text TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (concern_id) REFERENCES concerns(concern_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
```

#### Table 7: notifications
```sql
notifications (
    notification_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    concern_id INTEGER,
    notification_type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (concern_id) REFERENCES concerns(concern_id)
)
```

#### Table 8: attachments
```sql
attachments (
    attachment_id SERIAL PRIMARY KEY,
    concern_id INTEGER NOT NULL,
    uploaded_by INTEGER NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(50),
    file_size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (concern_id) REFERENCES concerns(concern_id),
    FOREIGN KEY (uploaded_by) REFERENCES users(user_id)
)
```

### Example 3NF Data:

**users:**
| user_id | sr_code | email | first_name | last_name | role |
|---------|---------|-------|------------|-----------|------|
| 1 | 21-12345 | juan@g.batstate-u.edu.ph | Juan | Dela Cruz | student |
| 2 | 00-00000 | admin@ssc.batstateu.edu.ph | Admin | User | admin |

**concern_categories:**
| category_id | category_name | description |
|-------------|---------------|-------------|
| 1 | Academic | Concerns related to classes, grades |
| 2 | Services & Facilities | Problems with campus facilities |

**offices:**
| office_id | office_name | contact_email |
|-----------|-------------|---------------|
| 1 | SSC | ssc@batstateu.edu.ph |
| 2 | Facility Management | facilities@batstateu.edu.ph |

**concerns:**
| concern_id | ticket_number | student_id | category_id | assigned_office_id | title | status |
|------------|---------------|------------|-------------|-------------------|-------|--------|
| 1 | GRV-2025-00001 | 1 | 2 | 2 | Broken AC | resolved |

**concern_status_history:**
| history_id | concern_id | old_status | new_status | changed_by | created_at |
|------------|------------|------------|------------|------------|------------|
| 1 | 1 | NULL | pending | 1 | 2025-11-01 10:00:00 |
| 2 | 1 | pending | in-review | 2 | 2025-11-02 14:30:00 |
| 3 | 1 | in-review | resolved | 2 | 2025-11-05 16:00:00 |

---

## Comparison Summary

| Aspect | UNF | 1NF | 2NF | 3NF |
|--------|-----|-----|-----|-----|
| **Repeating Groups** | ❌ Has repeating groups | ✅ Eliminated | ✅ Eliminated | ✅ Eliminated |
| **Atomic Values** | ❌ Multi-valued cells | ✅ Atomic values | ✅ Atomic values | ✅ Atomic values |
| **Primary Key** | ❌ No clear key | ✅ Has primary key | ✅ Has primary key | ✅ Has primary key |
| **Partial Dependencies** | ❌ Many dependencies | ❌ Exists | ✅ Removed | ✅ Removed |
| **Transitive Dependencies** | ❌ Many dependencies | ❌ Exists | ❌ Exists | ✅ Removed |
| **Data Redundancy** | ❌ Extreme redundancy | ❌ High redundancy | ⚠️ Some redundancy | ✅ Minimal redundancy |
| **Update Anomalies** | ❌ Severe | ❌ High | ⚠️ Some | ✅ None |
| **Number of Tables** | 1 | 1 | 6 | 8 |
| **Data Integrity** | ❌ Poor | ⚠️ Fair | ✅ Good | ✅ Excellent |

---

## Benefits of 3NF Implementation

### ✅ **Advantages:**
1. **Data Integrity** - Referential integrity through foreign keys
2. **No Redundancy** - Each piece of data stored once
3. **Easy Updates** - Change data in one place
4. **Scalability** - Easy to add new features
5. **Consistency** - No update/delete/insert anomalies
6. **Flexibility** - Easy to query and maintain
7. **Performance** - Efficient indexing and querying
8. **Transparency** - Supports SDG 16 through audit trails

### ⚠️ **Trade-offs:**
- More complex queries (need JOINs)
- Slightly more initial setup
- **BUT** these are worth it for data integrity and maintainability!

---

## Conclusion

The Student Grievance Reporting System database has been designed following proper normalization principles:

- **UNF → 1NF**: Eliminated repeating groups and multi-valued attributes
- **1NF → 2NF**: Removed partial dependencies by separating entities
- **2NF → 3NF**: Removed transitive dependencies by creating lookup tables

The final **3NF schema** ensures:
- ✅ Data integrity
- ✅ Minimal redundancy
- ✅ Efficient maintenance
- ✅ Scalability for future features
- ✅ Support for SDG 16 (transparency and accountability)

This normalized structure provides a solid foundation for the grievance reporting system, ensuring reliable and efficient data management for BatState-U TNEU Lipa's Supreme Student Council.
