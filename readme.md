<!-- build command : pip install -r requirements.txt

run command : gunicorn fitness_tracker.wsgi:application --bind 0.0.0.0:8000

run migration for first time and if something changes python manage.py migrate -->

# Fitness Tracker Backend

This is the backend for the **Fitness Tracker** application, built with **Django** and **Django REST Framework**.  
It provides APIs to manage workouts, meals, and step tracking for users.

---

## Features

- User authentication (register, login, logout)
- CRUD APIs for:
  - Workouts
  - Meals
  - Step counts
- JWT/Token-based authentication
- CORS support for frontend integration
- PostgreSQL database support

---

## Prerequisites

- Python 3.13+
- PostgreSQL (or any compatible DB)
- Virtual environment (recommended)

---

## Setup & Installation

1. **Clone the repository**

```bash
git clone https://github.com/prabash19/cicd1FitnessTrackerBackend.git
cd cicd1FitnessTrackerBackend
```

# 2.Create and activate a virtual environment

python -m venv venv

# Windows

venv\Scripts\activate

# macOS/Linux

source venv/bin/activate

# 3. Install dependencies

pip install -r requirements.txt

### Database Setup

# run migrations (first-time setup):

python manage.py migrate

# If models or database change in the future:

python manage.py migrate

# Running the Application

Development (optional)

python manage.py runserver

# Production (Render or Linux server)

gunicorn fitness_tracker.wsgi:application --bind 0.0.0.0:8000
