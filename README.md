# Tailwebs Teacher Portal — Student Management System

A clean, responsive web application for teachers to manage student records, built with **Django**, **Tailwind CSS**, **Bootstrap**, and **JavaScript**.

---

## 🚀 Features

- Teacher authentication (login/logout)
- Student dashboard:
  - Add, edit, delete student records
  - Inline editing support
  - Profile initials with avatar-style UI
- Form validations (frontend & backend)
- Responsive layout using Tailwind CSS + Bootstrap 5
- Secure with CSRF protection and best practices
-  Seed script to auto-create superuser and demo data

---

## Tech Stack

| Layer        | Technology                        |
|--------------|------------------------------------|
| Backend      | Django                             |
| Frontend     | Tailwind CSS + Bootstrap 5 + JS    |
| Database     | SQLite (default)                   |
| Auth         | Django built-in authentication     |
| Dev Tools    | `django-environ`, custom management commands |

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/NexusProgrammingStudio/Tailwebs_TeacherPortal.git
cd Tailwebs_TeacherPortal
```

### 2. Create Virtual environment

```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
  pip install -r requirements.txt
```
### 4. Setup Environment Variables

- This project uses a .env file, but also includes a fallback mechanism.

```txt
    # .env
    SECRET_KEY=your-very-secret-key
    DEBUG=True
```
- ⚠️ If you don’t provide a .env, the system will use a fallback key (not suitable for production).

### 4. Migrations & Seed Data

#### We’ve added a custom management command to:

- Create a default superuser (admin / admin123)
- Add sample student records

```bash
  python manage.py migrate
  python manage.py seed_data
```

### 5. Run Application

```bash
  python manage.py runserver
```

- The app will be available at: http://localhost:8000