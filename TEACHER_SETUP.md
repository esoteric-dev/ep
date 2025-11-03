# Teacher Portal Setup Guide

## Overview

The Teacher Portal allows administrators and teachers to:
- Login with teacher credentials
- View analytics and statistics
- Create exams
- Upload question papers from Excel files
- Manage exams and questions

## Setup Instructions

### 1. Install Required Dependencies

Make sure you have pandas and openpyxl installed for Excel import:

```bash
pip install pandas openpyxl
```

### 2. Run Migrations

Create the teacher profile model in the database:

```bash
python manage.py makemigrations teacher
python manage.py migrate
```

### 3. Create Teacher Account

You can create a teacher account in two ways:

#### Option A: Using Django Admin (Recommended)

1. Create a Django superuser if you haven't already:
   ```bash
   python manage.py createsuperuser
   ```

2. Login to Django admin at `/admin/`

3. Create a User:
   - Go to "Users" section
   - Click "Add User"
   - Enter username and password
   - Save

4. Create Teacher Profile:
   - Go to "Teacher Profiles" section
   - Click "Add Teacher Profile"
   - Select the user you just created
   - Fill in required fields (first_name, last_name, email)
   - Optionally set `is_admin` to True for admin privileges
   - Save

#### Option B: Using Django Shell

```python
from django.contrib.auth.models import User
from teacher.models import TeacherProfile

# Create user
user = User.objects.create_user(
    username='teacher1',
    password='your_password_here',
    email='teacher@example.com'
)

# Create teacher profile
teacher = TeacherProfile.objects.create(
    user=user,
    first_name='John',
    last_name='Doe',
    email='teacher@example.com',
    department='Mathematics',
    is_admin=False
)
```

### 4. Access Teacher Portal

1. Navigate to `/teacher/login/` or click "Teacher Login" from the landing page
2. Login with your teacher credentials
3. You'll be redirected to the dashboard

## Features

### Dashboard (`/teacher/dashboard/`)
- View total exams, questions, students, and attempts
- See exam performance statistics
- View recent exams and attempts

### Create Exam (`/teacher/create-exam/`)
- Create new exams with:
  - Exam name
  - Description
  - Duration (minutes)
  - Total marks
  - Language

### Upload Question Paper (`/teacher/upload-paper/`)
- Select an exam
- Upload Excel file (.xlsx) with questions
- Supports MCQ, MSQ, and Numerical question types
- Shows detailed error messages if any issues occur
- See `EXAM_IMPORT_GUIDE.md` for Excel format details

### Manage Exams (`/teacher/manage-exams/`)
- View all exams
- See test papers count for each exam
- Quick links to upload papers or view exams

## Excel Import Format

The Excel file should follow this structure:

### Sheet: Exam_Info (Optional)
- Exam Name
- Description
- Duration (minutes)
- Total Marks
- Language

### Test Paper Sheets (One per paper)
Sheet names become paper codes (e.g., "PAPER001", "SET1")

**Required Columns:**
- Question Type (MCQ/MSQ/Numerical)
- Question Number
- Question Text

**For MCQ:**
- Option A, B, C, D
- Correct Option (A/B/C/D)

**For MSQ:**
- Option A, B, C, D
- Correct Options (e.g., "AB", "ABC", "ABCD")

**For Numerical:**
- Correct Answer (numeric value)

**Optional Columns:**
- Question Image (path)
- Marks (default: 1.0)
- Negative Marks (default: 0.0)
- Topic

## Error Handling

The upload system provides detailed error messages:
- Missing required columns
- Invalid question types
- Missing options for MCQ/MSQ
- Invalid correct answer formats
- Row-specific errors with line numbers

All errors are reported without stopping the import - valid questions are still created.

## Security Notes

- Only users with TeacherProfile can access teacher portal
- Login required for all teacher pages
- Teachers can manage all exams (consider adding per-teacher permissions if needed)

## Troubleshooting

### "Access denied. Teacher account required"
- Make sure the user has a TeacherProfile associated
- Check that you're logging in with the correct credentials

### "pandas library is required"
- Install pandas: `pip install pandas openpyxl`
- Restart the Django server

### Excel upload fails
- Check file format matches the template
- Verify all required columns are present
- Check error messages for specific row issues
- Ensure exam is selected before uploading

### Migration errors
- Make sure all migrations are up to date: `python manage.py migrate`
- Check that teacher app is in INSTALLED_APPS

