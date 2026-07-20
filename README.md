# Student Feedback System

A Django-based feedback management portal where students submit feedback securely, and staff review, respond to, and report on it.

## Features

- **Student registration & login** — accounts are backed by Django's auth system, extended with a `StudentProfile` (roll number, department, year).
- **Feedback submission** — students submit categorized feedback with a 1–5 rating, and can optionally submit anonymously.
- **Student dashboard** — students see their own submission history and its status.
- **Admin dashboard** — staff accounts see every submission, with search and filtering by status/category, and can respond and change status.
- **Reports** — aggregate charts (via Chart.js) on volume by category, average rating by category, status breakdown, and rating distribution.
- **Responsive design** — built with Bootstrap 5, works on mobile, tablet, and desktop.

## Tech stack

Django · Python · SQLite · Bootstrap 5 (+ Chart.js for reports)

## Project structure

```
student_feedback_system/
├── manage.py
├── requirements.txt
├── feedback_system/        # project settings, URLs, WSGI/ASGI
└── feedback/                # the app: models, views, forms, templates
    ├── models.py             # StudentProfile, Category, Feedback
    ├── views.py
    ├── forms.py
    ├── admin.py
    ├── urls.py
    ├── migrations/
    ├── management/commands/seed_demo_data.py
    ├── templates/feedback/
    └── static/feedback/
```

## Getting started

1. **Create a virtual environment and install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

3. **(Optional) Seed demo data** — creates a superuser (`admin` / `ChangeMe123!`), 8 demo student accounts (`student1`…`student8` / `ChangeMe123!`), 5 categories, and 25 sample feedback entries:

   ```bash
   python manage.py seed_demo_data
   ```

   Or create your own superuser instead:

   ```bash
   python manage.py createsuperuser
   ```

4. **Run the development server**

   ```bash
   python manage.py runserver
   ```

5. Visit `http://127.0.0.1:8000/`:
   - Log in as a **student** to submit feedback and track its status.
   - Log in as a **staff/superuser** account to reach the admin dashboard (`/admin-dashboard/`) and reports (`/reports/`), plus the built-in Django admin at `/admin/`.

## Security notes for production

Before deploying, be sure to:

- Set `DJANGO_SECRET_KEY` to a fresh, random value via an environment variable.
- Set `DJANGO_DEBUG=False`.
- Set `DJANGO_ALLOWED_HOSTS` to your real domain(s).
- Enable `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, and `SECURE_SSL_REDIRECT` once served over HTTPS.
- Switch from SQLite to a production database (e.g. PostgreSQL) for anything beyond a demo.
- Change the seeded demo passwords, or don't run `seed_demo_data` in production at all.

## Key design decisions

- **Django's built-in auth** is reused rather than hand-rolled, for battle-tested password hashing, session handling, and CSRF protection.
- **Anonymity is opt-in per submission** (`is_anonymous`) rather than account-wide, so students can choose per feedback item whether staff see their identity — the underlying `student` FK is still recorded so a student can still see their own submission history.
- **Staff vs. student routing** is centralized in a single `redirect_after_login` view so the same login page works for both roles.
- **Reports use Chart.js**, fed by a small JSON payload computed server-side with Django's aggregation (`Avg`, `Count`), keeping the client-side code lightweight.
