# School MIS Backend

Modern Django REST Framework backend for School Management Information System with role-based access control, attendance tracking, grade management, and document uploads.

## 🚀 Features

- **JWT Authentication** with refresh tokens
- **Role-Based Access Control** (SuperAdmin, Admin, Teacher, Student)
- **User Management** with approval workflow for students
- **Academic Management** (Classes, Subjects, Semesters)
- **Student & Teacher Profiles**
- **Grade Management** with report cards
- **Attendance Tracking** for students and teachers
- **Document Upload & Management**
- **Granular Permission System** for admins
- **Automatic Cleanup** of pending accounts (configurable)
- **API Documentation** (Swagger/ReDoc)

## 📋 Requirements

- Python 3.8+
- Django 4.2+
- Redis (for Celery)

## 🛠️ Installation

1. **Create virtual environment:**
```bash
cd backend_new
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Create `.env` file:**
```bash
cp .env.example .env
```

Edit `.env` and set your configuration (or use defaults for development).

4. **Run migrations:**
```bash
python manage.py migrate
```

5. **Seed initial data (creates superadmin and semesters):**
```bash
python manage.py seed_data
```

This creates:
- Super Admin: `username: superadmin`, `password: Admin@123`
- Semesters 1-8

6. **Run development server:**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, access:
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **Schema**: http://localhost:8000/api/schema/

## 🔑 User Roles

### 1. Super Admin
- Full system access
- Can create and manage admins
- Can assign permissions to admins
- Can configure system settings

### 2. Admin
- Customizable permissions assigned by SuperAdmin
- Can manage resources based on granted permissions
- Cannot see other admins or super admins

### 3. Teacher
- Can view assigned classes and students
- Can enter/update grades for their subjects
- Can mark attendance
- Can view their own attendance records

### 4. Student
- Self-registration (requires approval)
- View own profile and grades
- View own attendance records
- View exam results

## 🔐 Authentication

### Register Student
```http
POST /api/auth/auth/register/student/
Content-Type: application/json

{
  "username": "student1",
  "password": "password123",
  "password_confirm": "password123",
  "name": "احمد رحیمی",
  "father_name": "محمد",
  "gender": "male",
  "phone_number": "+93700123456"
}
```

### Login
```http
POST /api/auth/auth/login/
Content-Type: application/json

{
  "username": "superadmin",
  "password": "Admin@123"
}
```

Response:
```json
{
  "refresh": "refresh_token_here",
  "access": "access_token_here",
  "user": { ... }
}
```

### Use Token
```http
GET /api/students/
Authorization: Bearer <access_token>
```

## 📁 Project Structure

```
backend_new/
├── config/                 # Django settings and configuration
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py
├── apps/
│   ├── core/              # Shared utilities and base classes
│   ├── accounts/          # User authentication and management
│   ├── permissions/       # Permission checking utilities
│   ├── students/          # Student management
│   ├── teachers/          # Teacher management
│   ├── academics/         # Classes, subjects, semesters
│   ├── grades/            # Grade management
│   ├── attendance/        # Attendance tracking
│   └── documents/         # Document uploads
├── media/                 # Uploaded files
├── staticfiles/           # Static files
├── requirements.txt
└── manage.py
```

## 🔄 Celery (Background Tasks)

The system uses Celery for background tasks like automatic cleanup of expired pending accounts.

### Start Redis
```bash
redis-server
```

### Start Celery Worker
```bash
celery -A config worker -l info
```

### Start Celery Beat (for scheduled tasks)
```bash
celery -A config beat -l info
```

## 🎯 API Endpoints

### Authentication
- `POST /api/auth/auth/register/student/` - Student self-registration
- `POST /api/auth/auth/login/` - Login
- `POST /api/auth/auth/logout/` - Logout
- `GET /api/auth/auth/me/` - Get current user
- `PUT /api/auth/auth/update_profile/` - Update profile
- `POST /api/auth/auth/change_password/` - Change password

### Users (Admin/SuperAdmin)
- `GET /api/auth/users/` - List users
- `POST /api/auth/users/` - Create user
- `GET /api/auth/users/{id}/` - Get user details
- `PUT /api/auth/users/{id}/` - Update user
- `DELETE /api/auth/users/{id}/` - Delete user
- `GET /api/auth/users/pending-students/` - List pending students
- `POST /api/auth/users/{id}/approve-reject/` - Approve/reject user

### Students
- `GET /api/students/` - List students
- `POST /api/students/` - Create student
- `GET /api/students/{id}/` - Get student details
- `GET /api/students/me/` - Get current student profile
- `GET /api/students/{id}/grades/` - Get student grades
- `GET /api/students/{id}/attendance/` - Get student attendance

### Teachers
- `GET /api/teachers/` - List teachers
- `POST /api/teachers/` - Create teacher
- `GET /api/teachers/{id}/` - Get teacher details
- `GET /api/teachers/me/` - Get current teacher profile
- `GET /api/teachers/{id}/students/` - Get teacher's students

### Academics
- `GET /api/academics/semesters/` - List semesters
- `GET /api/academics/classes/` - List classes
- `GET /api/academics/subjects/` - List subjects
- `POST /api/academics/classes/` - Create class
- `POST /api/academics/subjects/` - Create subject

### Grades
- `GET /api/grades/` - List grades
- `POST /api/grades/` - Create grade
- `GET /api/grades/student/{id}/` - Get grades for student
- `GET /api/grades/report-card/{id}/` - Get student report card
- `POST /api/grades/bulk-create/` - Bulk create grades

### Attendance
- `GET /api/attendance/students/` - List student attendance
- `POST /api/attendance/students/` - Mark student attendance
- `GET /api/attendance/teachers/` - List teacher attendance
- `POST /api/attendance/teachers/` - Mark teacher attendance
- `POST /api/attendance/students/bulk-mark/` - Bulk mark attendance

### Documents
- `GET /api/documents/` - List documents
- `POST /api/documents/` - Upload document
- `GET /api/documents/student/{id}/` - Get documents for student
- `POST /api/documents/{id}/verify/` - Verify document

### Permissions
- `GET /api/permissions/check/my_permissions/` - Get current user permissions
- `POST /api/permissions/check/check_permission/` - Check specific permission

## ⚙️ Configuration

Edit `.env` file:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
CELERY_BROKER_URL=redis://localhost:6379/0
PENDING_ACCOUNT_EXPIRY_MONTHS=6
```

## 🧪 Testing

```bash
python manage.py test
```

## 📝 Admin Panel

Access Django admin at: http://localhost:8000/admin/
- Username: `superadmin`
- Password: `Admin@123`

## 🔒 Security Notes

- Change default super admin password in production
- Use strong SECRET_KEY in production
- Set DEBUG=False in production
- Configure proper ALLOWED_HOSTS
- Use HTTPS in production
- Regularly update dependencies

## 📄 License

MIT License
