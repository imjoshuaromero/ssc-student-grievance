# 📚 SSC STUDENT GRIEVANCE SYSTEM - DATABASE DOCUMENTATION

**Batangas State University - The National Engineering University**  
**TNEU Lipa Campus**  
**Supreme Student Council (SSC)**  

---

## TABLE OF CONTENTS

1. [Introduction](#1-introduction)
2. [Entity Relationship Diagram](#2-entity-relationship-diagram)
3. [Normalization Process](#3-normalization-process)
4. [Data Dictionary](#4-data-dictionary)
5. [Sample Records & SQL Scripts](#5-sample-records--sql-scripts)
6. [SQL Queries and Results](#6-sql-queries-and-results)
7. [SQL Schema & Version Control](#7-sql-schema--version-control)
8. [Screenshots](#8-screenshots)
9. [Conclusion](#9-conclusion)
10. [References](#10-references)

---

## 1. INTRODUCTION

### 1.1 Overview of the System

The **SSC Student Grievance Reporting and Tracking System** is a comprehensive web-based platform designed to streamline the process of reporting, tracking, and resolving student concerns at Batangas State University - TNEU Lipa Campus. The system serves as a centralized hub where students can submit grievances related to academic matters, administrative decisions, campus facilities, harassment incidents, and other concerns that affect their educational experience.

The platform bridges the communication gap between students and the Supreme Student Council (SSC), ensuring that every concern is properly documented, assigned to the appropriate office, tracked through resolution, and concluded with proper feedback. By implementing a transparent ticket-based system, students can monitor the progress of their concerns in real-time, while administrators can efficiently manage and prioritize multiple grievances simultaneously. This digital transformation of the grievance handling process promotes accountability, transparency, and efficient resolution of student concerns, ultimately contributing to a better campus environment.

### 1.2 Purpose of Database

The database serves as the backbone of the grievance system, providing:

- **Centralized Data Storage**: All student information, concerns, communications, and resolutions are stored in a single, organized repository
- **Data Integrity**: Ensures that all relationships between students, concerns, categories, offices, and administrators are maintained accurately through foreign key constraints
- **Audit Trail**: Complete tracking of all status changes, comments, and actions taken on each concern for full transparency
- **Efficient Retrieval**: Optimized indexing allows quick access to specific concerns, user information, and historical data
- **Scalability**: Designed to handle growing numbers of users and concerns without performance degradation
- **Security**: Implements proper authentication and authorization mechanisms to protect sensitive student information
- **Reporting Capabilities**: Supports complex queries for generating statistics and insights about concern trends and resolution efficiency

### 1.3 Database Type and Tools Used

The system is built using modern, industry-standard technologies:

**Database Management System:**
- **PostgreSQL 14+**: A powerful, open-source relational database system known for its reliability, robustness, and advanced features including:
  - ACID compliance for data integrity
  - Advanced SQL features (CTEs, window functions, JSON support)
  - Triggers and stored procedures for automated processes
  - Full-text search capabilities
  - Excellent performance and scalability

**Backend Framework:**
- **Flask 3.0.0**: A lightweight Python web framework that provides:
  - RESTful API development
  - Session management
  - Template rendering
  - Easy integration with PostgreSQL via psycopg2

**Additional Tools:**
- **psycopg2-binary**: PostgreSQL adapter for Python
- **bcrypt**: Secure password hashing
- **PyJWT**: JSON Web Token authentication
- **Flask-Mail**: Email notification system
- **Pillow**: Image processing for file uploads
- **Google Auth**: OAuth 2.0 authentication

### 1.4 Objectives of the Project

The SSC Student Grievance System aims to achieve the following objectives:

**Primary Objectives:**

1. **Streamline Grievance Reporting**
   - Provide an accessible platform for students to report concerns 24/7
   - Implement a user-friendly interface that simplifies the submission process
   - Support file attachments for evidence documentation
   - Enable anonymous reporting when needed for sensitive issues

2. **Ensure Accountability and Transparency**
   - Generate unique ticket numbers for every concern (e.g., GRV-2025-00001)
   - Maintain complete status history with timestamps and responsible parties
   - Provide real-time updates to students on their concern progress
   - Create an audit trail for all actions taken on each concern

3. **Improve Resolution Efficiency**
   - Automatically assign concerns to appropriate offices based on category
   - Enable administrators to prioritize concerns (low, normal, high, urgent)
   - Track average resolution times and identify bottlenecks
   - Facilitate communication through built-in commenting system

4. **Enhance Communication**
   - Automated email notifications for status changes
   - In-app notification system for real-time updates
   - Comment threads between students and administrators
   - Email alerts for concern assignments and resolutions

5. **Support Data-Driven Decision Making**
   - Generate comprehensive reports on concern trends
   - Analyze resolution rates and times by category and office
   - Identify recurring issues for proactive solutions
   - Provide insights for improving campus services

**Secondary Objectives:**

6. **Promote Digital Governance**
   - Reduce paper-based processes and manual tracking
   - Create a centralized database of all student concerns
   - Enable remote access for students and administrators
   - Support multiple concurrent users

7. **Ensure Data Security and Privacy**
   - Implement secure authentication (JWT tokens, bcrypt password hashing)
   - Protect sensitive student information
   - Support Google OAuth for secure single sign-on
   - Implement role-based access control (students vs admins)

8. **Contribute to SDG 16**
   - Support **Peace, Justice, and Strong Institutions** through:
     - Transparent and accountable governance processes
     - Equal access to justice for all students
     - Effective and responsible decision-making
     - Inclusive and participatory governance

9. **Scalability and Maintainability**
   - Design for future growth in users and concerns
   - Use modular architecture for easy feature additions
   - Implement proper database normalization (3NF)
   - Maintain comprehensive documentation

10. **User Satisfaction**
    - Provide intuitive interfaces for both students and administrators
    - Ensure fast response times and system availability
    - Gather feedback for continuous improvement
    - Measure and improve user experience metrics

---

## 2. ENTITY RELATIONSHIP DIAGRAM

### 2.1 Entities

The SSC Student Grievance System uses the following entities to organize and store data:

#### **User Entity**
Stores all user accounts in the system, including both students and administrators.
- **Primary Purpose**: Authentication, authorization, and user identification
- **User Types**: Students (file concerns) and Admins (manage concerns)

#### **Concern Entity**
Represents individual grievances or concerns submitted by students.
- **Primary Purpose**: Track all reported issues from submission to resolution
- **Features**: Unique ticket numbers, status tracking, priority levels

#### **Concern Category Entity**
Defines the types or categories of concerns that can be reported.
- **Primary Purpose**: Classify concerns for proper routing and analysis
- **Examples**: Academic, Administrative Decisions, Services & Facilities, Harassment, Others

#### **Office Entity**
Represents university offices/departments responsible for handling concerns.
- **Primary Purpose**: Assign concerns to appropriate departments
- **Examples**: SSC, Registrar, OSAS, Facility Management, Academic Affairs

#### **Concern Status History Entity**
Logs every status change made to a concern.
- **Primary Purpose**: Complete audit trail of concern lifecycle
- **Tracks**: Old status, new status, who made the change, when it was made

#### **Comment Entity**
Stores all communications between students and administrators.
- **Primary Purpose**: Enable dialogue and updates on concerns
- **Types**: Public comments (visible to student) and internal notes (admin only)

#### **Notification Entity**
Manages in-app notifications for users.
- **Primary Purpose**: Alert users about important events
- **Types**: Concern created, status changed, comment added, concern assigned, resolved

#### **Attachment Entity**
Stores metadata for files uploaded with concerns.
- **Primary Purpose**: Document evidence and supporting materials
- **Supported Types**: Images (PNG, JPG), Documents (PDF, DOC), etc.

### 2.2 Attributes

#### **users** Entity Attributes:

| Attribute | Data Type | Description | Constraints |
|-----------|-----------|-------------|-------------|
| `user_id` | INTEGER | Unique identifier for each user | PRIMARY KEY, AUTO INCREMENT |
| `sr_code` | VARCHAR(20) | Student/Staff Registration code (e.g., "21-12345") | UNIQUE, NOT NULL |
| `email` | VARCHAR(255) | User's email address | UNIQUE, NOT NULL |
| `password_hash` | VARCHAR(255) | Encrypted password using bcrypt | NOT NULL |
| `first_name` | VARCHAR(100) | User's first name | NOT NULL |
| `last_name` | VARCHAR(100) | User's last name | NOT NULL |
| `middle_name` | VARCHAR(100) | User's middle name | NULLABLE |
| `program` | VARCHAR(100) | Academic program (e.g., "BSCS", "BSIT") | NULLABLE |
| `year_level` | INTEGER | Year level (1, 2, 3, or 4) | CHECK (1-4) |
| `role` | VARCHAR(20) | User role: 'student' or 'admin' | NOT NULL, DEFAULT 'student' |
| `google_id` | VARCHAR(255) | Google OAuth identifier | UNIQUE, NULLABLE |
| `email_verified` | BOOLEAN | Email verification status | DEFAULT FALSE |
| `verification_code` | VARCHAR(6) | 6-digit email verification code | NULLABLE |
| `verification_code_expires` | TIMESTAMP | Expiration time for verification code | NULLABLE |
| `verification_token` | VARCHAR(255) | Email verification token | NULLABLE |
| `is_active` | BOOLEAN | Account status | DEFAULT TRUE |
| `created_at` | TIMESTAMP | Account creation timestamp | DEFAULT CURRENT_TIMESTAMP |
| `updated_at` | TIMESTAMP | Last update timestamp | AUTO-UPDATE |

#### **concerns** Entity Attributes:

| Attribute | Data Type | Description | Constraints |
|-----------|-----------|-------------|-------------|
| `concern_id` | INTEGER | Unique identifier for each concern | PRIMARY KEY, AUTO INCREMENT |
| `ticket_number` | VARCHAR(50) | Unique ticket (e.g., "GRV-2025-00001") | UNIQUE, NOT NULL, AUTO-GENERATED |
| `student_id` | INTEGER | Reference to user who filed concern | FOREIGN KEY → users(user_id) |
| `category_id` | INTEGER | Reference to concern category | FOREIGN KEY → concern_categories |
| `assigned_office_id` | INTEGER | Office handling the concern | FOREIGN KEY → offices |
| `assigned_admin_id` | INTEGER | Admin assigned to concern | FOREIGN KEY → users(user_id) |
| `title` | VARCHAR(255) | Brief title of the concern | NOT NULL |
| `description` | TEXT | Detailed description of the concern | NOT NULL |
| `location` | VARCHAR(255) | Where the incident occurred | NULLABLE |
| `incident_date` | DATE | When the incident happened | NULLABLE |
| `status` | VARCHAR(50) | Current status | CHECK ('pending', 'in-review', 'in-progress', 'resolved', 'closed', 'rejected') |
| `priority` | VARCHAR(20) | Priority level | CHECK ('low', 'normal', 'high', 'urgent') |
| `is_anonymous` | BOOLEAN | Anonymous submission flag | DEFAULT FALSE |
| `other_category` | VARCHAR(100) | Custom category if "Others" selected | NULLABLE |
| `resolution_notes` | TEXT | Final resolution details | NULLABLE |
| `resolved_at` | TIMESTAMP | Resolution timestamp | NULLABLE |
| `resolved_by` | INTEGER | Admin who resolved | FOREIGN KEY → users |
| `created_at` | TIMESTAMP | Submission timestamp | DEFAULT CURRENT_TIMESTAMP |
| `updated_at` | TIMESTAMP | Last update timestamp | AUTO-UPDATE |

#### **concern_categories** Entity Attributes:

| Attribute | Data Type | Description | Constraints |
|-----------|-----------|-------------|-------------|
| `category_id` | INTEGER | Unique identifier | PRIMARY KEY, AUTO INCREMENT |
| `category_name` | VARCHAR(100) | Category name | UNIQUE, NOT NULL |
| `description` | TEXT | Category description | NULLABLE |
| `is_active` | BOOLEAN | Active status | DEFAULT TRUE |
| `created_at` | TIMESTAMP | Creation timestamp | DEFAULT CURRENT_TIMESTAMP |

#### **offices** Entity Attributes:

| Attribute | Data Type | Description | Constraints |
|-----------|-----------|-------------|-------------|
| `office_id` | INTEGER | Unique identifier | PRIMARY KEY, AUTO INCREMENT |
| `office_name` | VARCHAR(100) | Office name | UNIQUE, NOT NULL |
| `description` | TEXT | Office description | NULLABLE |
| `contact_email` | VARCHAR(255) | Office email | NULLABLE |
| `contact_number` | VARCHAR(20) | Office phone | NULLABLE |
| `is_active` | BOOLEAN | Active status | DEFAULT TRUE |
| `created_at` | TIMESTAMP | Creation timestamp | DEFAULT CURRENT_TIMESTAMP |

#### **concern_status_history** Entity Attributes:

| Attribute | Data Type | Description | Constraints |
|-----------|-----------|-------------|-------------|
| `history_id` | INTEGER | Unique identifier | PRIMARY KEY, AUTO INCREMENT |
| `concern_id` | INTEGER | Reference to concern | FOREIGN KEY → concerns(concern_id) |
| `old_status` | VARCHAR(50) | Previous status | NULLABLE (NULL for initial creation) |
| `new_status` | VARCHAR(50) | New status | NOT NULL |
| `changed_by` | INTEGER | User who made the change | FOREIGN KEY → users(user_id) |
| `remarks` | TEXT | Notes about the change | NULLABLE |
| `created_at` | TIMESTAMP | Change timestamp | DEFAULT CURRENT_TIMESTAMP |

#### **comments** Entity Attributes:

| Attribute | Data Type | Description | Constraints |
|-----------|-----------|-------------|-------------|
| `comment_id` | INTEGER | Unique identifier | PRIMARY KEY, AUTO INCREMENT |
| `concern_id` | INTEGER | Reference to concern | FOREIGN KEY → concerns |
| `user_id` | INTEGER | User who commented | FOREIGN KEY → users |
| `comment_text` | TEXT | Comment content | NOT NULL |
| `is_internal` | BOOLEAN | Internal admin note flag | DEFAULT FALSE |
| `created_at` | TIMESTAMP | Comment timestamp | DEFAULT CURRENT_TIMESTAMP |
| `updated_at` | TIMESTAMP | Last update timestamp | AUTO-UPDATE |

#### **notifications** Entity Attributes:

| Attribute | Data Type | Description | Constraints |
|-----------|-----------|-------------|-------------|
| `notification_id` | INTEGER | Unique identifier | PRIMARY KEY, AUTO INCREMENT |
| `user_id` | INTEGER | Recipient user | FOREIGN KEY → users |
| `concern_id` | INTEGER | Related concern | FOREIGN KEY → concerns (NULLABLE) |
| `notification_type` | VARCHAR(50) | Type of notification | CHECK (concern_created, status_changed, comment_added, concern_assigned, concern_resolved) |
| `title` | VARCHAR(255) | Notification title | NOT NULL |
| `message` | TEXT | Notification message | NOT NULL |
| `is_read` | BOOLEAN | Read status | DEFAULT FALSE |
| `read_at` | TIMESTAMP | When notification was read | NULLABLE |
| `created_at` | TIMESTAMP | Creation timestamp | DEFAULT CURRENT_TIMESTAMP |

#### **attachments** Entity Attributes:

| Attribute | Data Type | Description | Constraints |
|-----------|-----------|-------------|-------------|
| `attachment_id` | INTEGER | Unique identifier | PRIMARY KEY, AUTO INCREMENT |
| `concern_id` | INTEGER | Related concern | FOREIGN KEY → concerns |
| `uploaded_by` | INTEGER | User who uploaded | FOREIGN KEY → users |
| `file_name` | VARCHAR(255) | Original filename | NOT NULL |
| `file_path` | VARCHAR(500) | Server file path | NOT NULL |
| `file_type` | VARCHAR(50) | MIME type | NULLABLE |
| `file_size` | INTEGER | File size in bytes | NULLABLE |
| `created_at` | TIMESTAMP | Upload timestamp | DEFAULT CURRENT_TIMESTAMP |

### 2.3 Primary Keys and Foreign Keys

#### Primary Keys:

| Table | Primary Key | Description |
|-------|-------------|-------------|
| users | `user_id` | Uniquely identifies each user |
| concerns | `concern_id` | Uniquely identifies each concern |
| concern_categories | `category_id` | Uniquely identifies each category |
| offices | `office_id` | Uniquely identifies each office |
| concern_status_history | `history_id` | Uniquely identifies each status change |
| comments | `comment_id` | Uniquely identifies each comment |
| notifications | `notification_id` | Uniquely identifies each notification |
| attachments | `attachment_id` | Uniquely identifies each attachment |

#### Foreign Keys:

| Table | Foreign Key | References | Relationship |
|-------|-------------|------------|--------------|
| concerns | `student_id` | users(user_id) | Many concerns → One student |
| concerns | `category_id` | concern_categories(category_id) | Many concerns → One category |
| concerns | `assigned_office_id` | offices(office_id) | Many concerns → One office |
| concerns | `assigned_admin_id` | users(user_id) | Many concerns → One admin |
| concerns | `resolved_by` | users(user_id) | Many concerns → One admin |
| concern_status_history | `concern_id` | concerns(concern_id) | Many history → One concern |
| concern_status_history | `changed_by` | users(user_id) | Many changes → One user |
| comments | `concern_id` | concerns(concern_id) | Many comments → One concern |
| comments | `user_id` | users(user_id) | Many comments → One user |
| notifications | `user_id` | users(user_id) | Many notifications → One user |
| notifications | `concern_id` | concerns(concern_id) | Many notifications → One concern |
| attachments | `concern_id` | concerns(concern_id) | Many attachments → One concern |
| attachments | `uploaded_by` | users(user_id) | Many attachments → One user |

### 2.4 Relationships

#### Relationship Types:

**1. users ↔ concerns (as student)**
- **Type**: One-to-Many (1:M)
- **Description**: A student user can submit multiple concerns, but each concern is filed by only one student
- **Implementation**: `concerns.student_id` → `users.user_id`

**2. users ↔ concerns (as admin)**
- **Type**: One-to-Many (1:M)
- **Description**: An admin can be assigned to multiple concerns, but each concern can have only one assigned admin
- **Implementation**: `concerns.assigned_admin_id` → `users.user_id`

**3. concern_categories ↔ concerns**
- **Type**: One-to-Many (1:M)
- **Description**: A category can contain multiple concerns, but each concern belongs to only one category
- **Implementation**: `concerns.category_id` → `concern_categories.category_id`

**4. offices ↔ concerns**
- **Type**: One-to-Many (1:M)
- **Description**: An office can handle multiple concerns, but each concern is assigned to only one office
- **Implementation**: `concerns.assigned_office_id` → `offices.office_id`

**5. concerns ↔ concern_status_history**
- **Type**: One-to-Many (1:M)
- **Description**: Each concern has multiple status changes tracked over time
- **Implementation**: `concern_status_history.concern_id` → `concerns.concern_id`

**6. concerns ↔ comments**
- **Type**: One-to-Many (1:M)
- **Description**: Each concern can have multiple comments for discussion
- **Implementation**: `comments.concern_id` → `concerns.concern_id`

**7. users ↔ comments**
- **Type**: One-to-Many (1:M)
- **Description**: A user can write multiple comments across different concerns
- **Implementation**: `comments.user_id` → `users.user_id`

**8. concerns ↔ notifications**
- **Type**: One-to-Many (1:M)
- **Description**: Each concern can generate multiple notifications
- **Implementation**: `notifications.concern_id` → `concerns.concern_id`

**9. users ↔ notifications**
- **Type**: One-to-Many (1:M)
- **Description**: A user can receive multiple notifications
- **Implementation**: `notifications.user_id` → `users.user_id`

**10. concerns ↔ attachments**
- **Type**: One-to-Many (1:M)
- **Description**: Each concern can have multiple file attachments
- **Implementation**: `attachments.concern_id` → `concerns.concern_id`

### 2.5 Entity Relationship Diagram (ERD)

```
┌─────────────────────────┐
│        users            │
├─────────────────────────┤
│ PK user_id              │
│    sr_code (UNIQUE)     │
│    email (UNIQUE)       │
│    password_hash        │
│    first_name           │
│    last_name            │
│    middle_name          │
│    program              │
│    year_level           │
│    role                 │
│    google_id            │
│    email_verified       │
│    verification_code    │
│    is_active            │
│    created_at           │
│    updated_at           │
└───────────┬─────────────┘
            │
            │ 1:M (student_id)
            │
            ▼
┌─────────────────────────┐        ┌─────────────────────────┐
│ concern_categories      │        │       offices           │
├─────────────────────────┤        ├─────────────────────────┤
│ PK category_id          │        │ PK office_id            │
│    category_name        │        │    office_name          │
│    description          │        │    description          │
│    is_active            │        │    contact_email        │
│    created_at           │        │    contact_number       │
└───────────┬─────────────┘        │    is_active            │
            │                      │    created_at           │
            │ 1:M                  └───────────┬─────────────┘
            │                                  │
            │                                  │ 1:M
            ▼                                  ▼
┌──────────────────────────────────────────────────────┐
│                   concerns                           │
├──────────────────────────────────────────────────────┤
│ PK concern_id                                        │
│    ticket_number (UNIQUE, AUTO-GENERATED)            │
│ FK student_id → users(user_id)                       │
│ FK category_id → concern_categories(category_id)     │
│ FK assigned_office_id → offices(office_id)           │
│ FK assigned_admin_id → users(user_id)                │
│    title                                             │
│    description                                       │
│    location                                          │
│    incident_date                                     │
│    status                                            │
│    priority                                          │
│    is_anonymous                                      │
│    other_category                                    │
│    resolution_notes                                  │
│    resolved_at                                       │
│ FK resolved_by → users(user_id)                      │
│    created_at                                        │
│    updated_at                                        │
└───────────┬────────────┬────────────┬────────────────┘
            │            │            │
     1:M    │            │ 1:M        │ 1:M
            │            │            │
            ▼            ▼            ▼
┌───────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│concern_status_    │ │   comments      │ │  attachments    │
│   history         │ │                 │ │                 │
├───────────────────┤ ├─────────────────┤ ├─────────────────┤
│PK history_id      │ │PK comment_id    │ │PK attachment_id │
│FK concern_id      │ │FK concern_id    │ │FK concern_id    │
│FK changed_by      │ │FK user_id       │ │FK uploaded_by   │
│   old_status      │ │   comment_text  │ │   file_name     │
│   new_status      │ │   is_internal   │ │   file_path     │
│   remarks         │ │   created_at    │ │   file_type     │
│   created_at      │ │   updated_at    │ │   file_size     │
└───────────────────┘ └─────────────────┘ │   created_at    │
                                          └─────────────────┘
            ┌──────────────────┐
            │ notifications    │
            ├──────────────────┤
            │PK notification_id│
            │FK user_id        │
            │FK concern_id     │
            │ notification_type│
            │ title            │
            │ message          │
            │ is_read          │
            │ read_at          │
            │ created_at       │
            └──────────────────┘
```

**Relationship Legend:**
- `PK` = Primary Key
- `FK` = Foreign Key
- `1:M` = One-to-Many Relationship
- `UNIQUE` = Unique Constraint
- Arrows indicate the direction of relationships

---

## 3. NORMALIZATION PROCESS

### 3.1 Unnormalized Form (UNF)

**Initial Structure:** All data in a single table with repeating groups and multi-valued attributes.

**Example UNF Table:**

```
STUDENT_GRIEVANCE_SYSTEM
├─ SR_Code: "21-12345"
├─ Student_Email: "juan@g.batstate-u.edu.ph"
├─ Student_Name: "Juan Dela Cruz"
├─ Student_Program: "BSCS"
├─ Student_Year: 3
├─ Concern_Ticket: "GRV-2025-00001"
├─ Concern_Title: "Broken Air Conditioning in Room 301"
├─ Concern_Description: "The AC has been broken for 2 weeks..."
├─ Concern_Category: "Services & Facilities"
├─ Category_Description: "Problems with campus facilities..."
├─ Office_Assigned: "Facility Management"
├─ Office_Email: "facilities@batstateu.edu.ph"
├─ Office_Phone: "043-XXX-XXXX"
├─ Admin_Assigned: "Maria Santos"
├─ Admin_Email: "admin@ssc.batstateu.edu.ph"
├─ Status_History: [
│     {status: "pending", date: "2025-11-01 10:00", by: "System"},
│     {status: "in-review", date: "2025-11-02 14:30", by: "Admin Maria"},
│     {status: "in-progress", date: "2025-11-03 09:00", by: "Admin Maria"},
│     {status: "resolved", date: "2025-11-05 16:00", by: "Admin Maria"}
│  ]
├─ Comments: [
│     {user: "Juan", date: "2025-11-01", text: "Need urgent repair"},
│     {user: "Admin Maria", date: "2025-11-02", text: "Assigned to facilities"},
│     {user: "Admin Maria", date: "2025-11-05", text: "AC has been repaired"}
│  ]
├─ Attachments: [
│     {file: "broken_ac_photo.jpg", date: "2025-11-01"},
│     {file: "room_301_report.pdf", date: "2025-11-01"}
│  ]
└─ Notifications: [
      {type: "created", date: "2025-11-01", read: true},
      {type: "status_changed", date: "2025-11-02", read: true},
      {type: "resolved", date: "2025-11-05", read: false}
   ]
```

**Problems with UNF:**
- ❌ **Repeating Groups**: Status_History, Comments, Attachments, Notifications contain multiple values
- ❌ **Data Redundancy**: Student information repeated for every concern
- ❌ **Update Anomalies**: Changing student email requires updating multiple rows
- ❌ **Insertion Anomalies**: Cannot add a student without a concern
- ❌ **Deletion Anomalies**: Deleting a concern deletes all student information
- ❌ **Difficult Queries**: Cannot efficiently search or filter data
- ❌ **No Data Integrity**: No constraints or relationships

### 3.2 First Normal Form (1NF)

**Rules Applied:**
1. ✅ Eliminate repeating groups
2. ✅ Create separate rows for each set of related data
3. ✅ Each cell contains only atomic (single) values
4. ✅ Identify primary key

**1NF Table Structure:**

```sql
STUDENT_CONCERNS_1NF (
    record_id INT PRIMARY KEY,
    sr_code VARCHAR(20),
    student_email VARCHAR(255),
    student_name VARCHAR(100),
    student_program VARCHAR(100),
    student_year INTEGER,
    concern_ticket VARCHAR(50),
    concern_title VARCHAR(255),
    concern_description TEXT,
    category_name VARCHAR(100),
    category_description TEXT,
    office_name VARCHAR(100),
    office_email VARCHAR(255),
    office_phone VARCHAR(20),
    admin_name VARCHAR(100),
    admin_email VARCHAR(255),
    status_old VARCHAR(50),
    status_new VARCHAR(50),
    status_date TIMESTAMP,
    status_changed_by VARCHAR(100),
    comment_text TEXT,
    comment_date TIMESTAMP,
    comment_by VARCHAR(100),
    attachment_filename VARCHAR(255),
    attachment_path VARCHAR(500),
    attachment_date TIMESTAMP,
    notification_type VARCHAR(50),
    notification_date TIMESTAMP,
    notification_read BOOLEAN
)
```

**Example 1NF Data (Flattened):**

| record_id | sr_code | student_name | concern_ticket | category | status_old | status_new | comment_text | attachment |
|-----------|---------|--------------|----------------|----------|------------|------------|--------------|------------|
| 1 | 21-12345 | Juan Dela Cruz | GRV-2025-00001 | Facilities | NULL | pending | Need urgent repair | broken_ac.jpg |
| 2 | 21-12345 | Juan Dela Cruz | GRV-2025-00001 | Facilities | NULL | pending | Need urgent repair | report.pdf |
| 3 | 21-12345 | Juan Dela Cruz | GRV-2025-00001 | Facilities | pending | in-review | Assigned to facilities | broken_ac.jpg |
| 4 | 21-12345 | Juan Dela Cruz | GRV-2025-00001 | Facilities | pending | in-review | Assigned to facilities | report.pdf |
| 5 | 21-12345 | Juan Dela Cruz | GRV-2025-00001 | Facilities | in-review | in-progress | Working on it | broken_ac.jpg |

**Improvements:**
- ✅ No multi-valued attributes
- ✅ Each cell contains atomic values
- ✅ Has primary key (record_id)

**Remaining Problems:**
- ❌ **Massive Data Redundancy**: Student info repeated in every row
- ❌ **Partial Dependencies**: Student info depends only on sr_code, not entire primary key
- ❌ **Update Anomalies**: Changing student email requires multiple updates
- ❌ **Storage Inefficiency**: Same data stored hundreds of times

### 3.3 Second Normal Form (2NF)

**Rules Applied:**
1. ✅ Must be in 1NF
2. ✅ Remove partial dependencies
3. ✅ All non-key attributes must depend on the entire primary key

**2NF Tables:**

#### Table: users_2nf
```sql
users_2nf (
    user_id INT PRIMARY KEY,
    sr_code VARCHAR(20) UNIQUE,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    program VARCHAR(100),
    year_level INTEGER,
    role VARCHAR(20)
)
```

#### Table: concerns_2nf
```sql
concerns_2nf (
    concern_id INT PRIMARY KEY,
    student_user_id INT,  -- FK to users_2nf
    admin_user_id INT,    -- FK to users_2nf
    ticket_number VARCHAR(50) UNIQUE,
    title VARCHAR(255),
    description TEXT,
    category_name VARCHAR(100),
    category_description TEXT,
    office_name VARCHAR(100),
    office_email VARCHAR(255),
    status VARCHAR(50),
    priority VARCHAR(20),
    created_at TIMESTAMP,
    FOREIGN KEY (student_user_id) REFERENCES users_2nf(user_id),
    FOREIGN KEY (admin_user_id) REFERENCES users_2nf(user_id)
)
```

#### Table: status_history_2nf
```sql
status_history_2nf (
    history_id INT PRIMARY KEY,
    concern_id INT,
    changed_by_user_id INT,
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    remarks TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (concern_id) REFERENCES concerns_2nf(concern_id),
    FOREIGN KEY (changed_by_user_id) REFERENCES users_2nf(user_id)
)
```

#### Table: comments_2nf
```sql
comments_2nf (
    comment_id INT PRIMARY KEY,
    concern_id INT,
    user_id INT,
    comment_text TEXT,
    is_internal BOOLEAN,
    created_at TIMESTAMP,
    FOREIGN KEY (concern_id) REFERENCES concerns_2nf(concern_id),
    FOREIGN KEY (user_id) REFERENCES users_2nf(user_id)
)
```

#### Table: attachments_2nf
```sql
attachments_2nf (
    attachment_id INT PRIMARY KEY,
    concern_id INT,
    uploaded_by_user_id INT,
    file_name VARCHAR(255),
    file_path VARCHAR(500),
    created_at TIMESTAMP,
    FOREIGN KEY (concern_id) REFERENCES concerns_2nf(concern_id),
    FOREIGN KEY (uploaded_by_user_id) REFERENCES users_2nf(user_id)
)
```

#### Table: notifications_2nf
```sql
notifications_2nf (
    notification_id INT PRIMARY KEY,
    user_id INT,
    concern_id INT,
    notification_type VARCHAR(50),
    message TEXT,
    is_read BOOLEAN,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users_2nf(user_id),
    FOREIGN KEY (concern_id) REFERENCES concerns_2nf(concern_id)
)
```

**Example 2NF Data:**

**users_2nf:**
| user_id | sr_code | email | first_name | last_name | program | role |
|---------|---------|-------|------------|-----------|---------|------|
| 1 | 21-12345 | juan@g.batstate-u.edu.ph | Juan | Dela Cruz | BSCS | student |
| 2 | 00-00000 | admin@ssc.batstateu.edu.ph | Maria | Santos | N/A | admin |

**concerns_2nf:**
| concern_id | student_user_id | ticket_number | title | category_name | office_name | status |
|------------|-----------------|---------------|-------|---------------|-------------|--------|
| 1 | 1 | GRV-2025-00001 | Broken AC in Room 301 | Services & Facilities | Facility Management | resolved |

**status_history_2nf:**
| history_id | concern_id | old_status | new_status | changed_by_user_id | created_at |
|------------|------------|------------|------------|-------------------|------------|
| 1 | 1 | NULL | pending | 1 | 2025-11-01 10:00 |
| 2 | 1 | pending | in-review | 2 | 2025-11-02 14:30 |
| 3 | 1 | in-review | in-progress | 2 | 2025-11-03 09:00 |
| 4 | 1 | in-progress | resolved | 2 | 2025-11-05 16:00 |

**Improvements:**
- ✅ No partial dependencies
- ✅ Significantly reduced data redundancy
- ✅ Each table focuses on specific entities
- ✅ Foreign keys maintain relationships

**Remaining Problems:**
- ❌ **Transitive Dependencies** still exist:
  - `category_description` depends on `category_name` (not primary key)
  - `office_email` depends on `office_name` (not primary key)
- ❌ **Update Anomalies**: Changing category description requires updating all concerns in that category

### 3.4 Third Normal Form (3NF)

**Rules Applied:**
1. ✅ Must be in 2NF
2. ✅ Remove transitive dependencies
3. ✅ All non-key attributes must depend ONLY on the primary key

**3NF Tables (Final Normalized Schema):**

#### Table: users
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
    year_level INTEGER CHECK (year_level BETWEEN 1 AND 4),
    role VARCHAR(20) NOT NULL DEFAULT 'student',
    google_id VARCHAR(255) UNIQUE,
    email_verified BOOLEAN DEFAULT FALSE,
    verification_code VARCHAR(6),
    verification_code_expires TIMESTAMP,
    verification_token VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### Table: concern_categories
```sql
concern_categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### Table: offices
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

#### Table: concerns
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
    other_category VARCHAR(100),
    resolution_notes TEXT,
    resolved_at TIMESTAMP,
    resolved_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES concern_categories(category_id),
    FOREIGN KEY (assigned_office_id) REFERENCES offices(office_id),
    FOREIGN KEY (assigned_admin_id) REFERENCES users(user_id),
    FOREIGN KEY (resolved_by) REFERENCES users(user_id)
)
```

#### Table: concern_status_history
```sql
concern_status_history (
    history_id SERIAL PRIMARY KEY,
    concern_id INTEGER NOT NULL,
    old_status VARCHAR(50),
    new_status VARCHAR(50) NOT NULL,
    changed_by INTEGER NOT NULL,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (concern_id) REFERENCES concerns(concern_id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users(user_id)
)
```

#### Table: comments
```sql
comments (
    comment_id SERIAL PRIMARY KEY,
    concern_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    comment_text TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (concern_id) REFERENCES concerns(concern_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
)
```

#### Table: notifications
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
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (concern_id) REFERENCES concerns(concern_id) ON DELETE CASCADE
)
```

#### Table: attachments
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
    
    FOREIGN KEY (concern_id) REFERENCES concerns(concern_id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(user_id)
)
```

**Example 3NF Data:**

**users:**
| user_id | sr_code | email | first_name | last_name | program | year_level | role |
|---------|---------|-------|------------|-----------|---------|------------|------|
| 1 | 21-12345 | juan@g.batstate-u.edu.ph | Juan | Dela Cruz | BSCS | 3 | student |
| 2 | 00-00000 | admin@ssc.batstateu.edu.ph | Maria | Santos | NULL | NULL | admin |

**concern_categories:**
| category_id | category_name | description |
|-------------|---------------|-------------|
| 1 | Academic | Concerns related to classes, grades, curriculum, and academic matters |
| 2 | Administrative Decisions | Issues with administrative policies, decisions, and procedures |
| 3 | Services & Facilities | Problems with campus facilities, services, and infrastructure |
| 4 | Harassment | Harassment, discrimination, or bullying reports |
| 5 | Others | Other concerns not covered by the above categories |

**offices:**
| office_id | office_name | description | contact_email |
|-----------|-------------|-------------|---------------|
| 1 | SSC | Supreme Student Council | ssc@batstateu.edu.ph |
| 2 | Registrar | Office of the Registrar | registrar@batstateu.edu.ph |
| 3 | OSAS | Office of Student Affairs and Services | osas@batstateu.edu.ph |
| 4 | Facility Management | Campus Facility Management | facilities@batstateu.edu.ph |
| 5 | Academic Affairs | Office of Academic Affairs | academics@batstateu.edu.ph |

**concerns:**
| concern_id | ticket_number | student_id | category_id | assigned_office_id | assigned_admin_id | title | description | status | priority | created_at |
|------------|---------------|------------|-------------|-------------------|-------------------|-------|-------------|--------|----------|------------|
| 1 | GRV-2025-00001 | 1 | 3 | 4 | 2 | Broken AC in Room 301 | The air conditioning unit in Room 301 has been broken for 2 weeks... | resolved | high | 2025-11-01 10:00:00 |

**concern_status_history:**
| history_id | concern_id | old_status | new_status | changed_by | remarks | created_at |
|------------|------------|------------|------------|------------|---------|------------|
| 1 | 1 | NULL | pending | 1 | Concern created | 2025-11-01 10:00:00 |
| 2 | 1 | pending | in-review | 2 | Reviewing the issue | 2025-11-02 14:30:00 |
| 3 | 1 | in-review | in-progress | 2 | Assigned to facilities team | 2025-11-03 09:00:00 |
| 4 | 1 | in-progress | resolved | 2 | AC unit has been repaired | 2025-11-05 16:00:00 |

**comments:**
| comment_id | concern_id | user_id | comment_text | is_internal | created_at |
|------------|------------|---------|--------------|-------------|------------|
| 1 | 1 | 1 | Need urgent repair as it affects classes | FALSE | 2025-11-01 10:05:00 |
| 2 | 1 | 2 | Assigned to facility management | FALSE | 2025-11-02 14:35:00 |
| 3 | 1 | 2 | Checking budget allocation | TRUE | 2025-11-02 15:00:00 |
| 4 | 1 | 2 | AC has been repaired and tested | FALSE | 2025-11-05 16:05:00 |

**attachments:**
| attachment_id | concern_id | uploaded_by | file_name | file_path | file_type | file_size | created_at |
|---------------|------------|-------------|-----------|-----------|-----------|-----------|------------|
| 1 | 1 | 1 | broken_ac_photo.jpg | uploads/broken_ac_photo.jpg | image/jpeg | 245678 | 2025-11-01 10:02:00 |
| 2 | 1 | 1 | room_301_report.pdf | uploads/room_301_report.pdf | application/pdf | 123456 | 2025-11-01 10:03:00 |

**notifications:**
| notification_id | user_id | concern_id | notification_type | title | message | is_read | created_at |
|-----------------|---------|------------|-------------------|-------|---------|---------|------------|
| 1 | 1 | 1 | concern_created | Concern Received | Your concern GRV-2025-00001 has been received... | TRUE | 2025-11-01 10:00:01 |
| 2 | 1 | 1 | status_changed | Status Updated | Your concern GRV-2025-00001 status has been updated to in-review | TRUE | 2025-11-02 14:30:01 |
| 3 | 1 | 1 | concern_resolved | Concern Resolved | Your concern GRV-2025-00001 has been resolved | FALSE | 2025-11-05 16:00:01 |

### 3.5 Normalization Summary

| Aspect | UNF | 1NF | 2NF | 3NF (Final) |
|--------|-----|-----|-----|-------------|
| **Repeating Groups** | ❌ Many | ✅ None | ✅ None | ✅ None |
| **Atomic Values** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **Primary Key** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **Partial Dependencies** | ❌ Many | ❌ Many | ✅ None | ✅ None |
| **Transitive Dependencies** | ❌ Many | ❌ Many | ❌ Exist | ✅ None |
| **Data Redundancy** | ❌ Extreme | ❌ Very High | ⚠️ Moderate | ✅ Minimal |
| **Update Anomalies** | ❌ Severe | ❌ Severe | ⚠️ Some | ✅ None |
| **Insertion Anomalies** | ❌ Yes | ❌ Yes | ⚠️ Few | ✅ None |
| **Deletion Anomalies** | ❌ Yes | ❌ Yes | ⚠️ Few | ✅ None |
| **Number of Tables** | 1 | 1 | 6 | 8 |
| **Data Integrity** | ❌ Poor | ⚠️ Fair | ✅ Good | ✅ Excellent |
| **Query Performance** | ❌ Poor | ❌ Poor | ✅ Good | ✅ Excellent |
| **Maintainability** | ❌ Difficult | ❌ Difficult | ✅ Good | ✅ Excellent |
| **Scalability** | ❌ Poor | ❌ Poor | ✅ Good | ✅ Excellent |

### 3.6 Benefits of 3NF Implementation

**✅ Advantages:**

1. **Data Integrity**
   - Referential integrity through foreign keys
   - Constraints prevent invalid data
   - CASCADE options maintain consistency

2. **No Redundancy**
   - Each piece of data stored exactly once
   - Reduces storage requirements
   - Eliminates inconsistent data

3. **Easy Updates**
   - Change data in only one place
   - No update anomalies
   - Atomic transactions

4. **Flexible Queries**
   - Easy to filter and search
   - Efficient JOIN operations
   - Supports complex analytics

5. **Scalability**
   - Easy to add new features
   - Can handle growing data
   - Performance remains consistent

6. **Transparency**
   - Complete audit trails
   - Status history tracking
   - Supports SDG 16 principles

**⚠️ Trade-offs:**

- **More Complex Queries**: Requires JOINs across multiple tables
- **Initial Setup**: Takes longer to design properly
- **Learning Curve**: Developers need to understand relationships

**BUT** these trade-offs are worth it for:
- Long-term maintainability
- Data integrity
- Professional database design
- Scalability

### 3.7 Denormalization Considerations

**When Denormalization Might Be Considered:**

For read-heavy operations, we created **materialized views** instead of denormalizing:

```sql
-- View: Active concerns summary (for dashboard)
CREATE VIEW vw_active_concerns AS
SELECT 
    c.concern_id,
    c.ticket_number,
    c.title,
    c.status,
    c.priority,
    c.created_at,
    u.first_name || ' ' || u.last_name AS student_name,
    u.sr_code,
    cat.category_name,
    o.office_name
FROM concerns c
JOIN users u ON c.student_id = u.user_id
JOIN concern_categories cat ON c.category_id = cat.category_id
LEFT JOIN offices o ON c.assigned_office_id = o.office_id
WHERE c.status NOT IN ('closed', 'resolved')
ORDER BY 
    CASE c.priority
        WHEN 'urgent' THEN 1
        WHEN 'high' THEN 2
        WHEN 'normal' THEN 3
        WHEN 'low' THEN 4
    END,
    c.created_at DESC;
```

This approach:
- ✅ Maintains 3NF structure
- ✅ Improves read performance
- ✅ Keeps data integrity
- ✅ Easy to refresh

---

*Continue to [Section 4: Data Dictionary](#4-data-dictionary)*
