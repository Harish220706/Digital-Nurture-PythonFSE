# Hands-On 1 — Web Framework Foundations & Django Project Setup

## What's inside
- `coursemanager/` — Django project scaffold (project = `coursemanager`, app = `courses`)
- `coursemanager/notes.py` — Task 1 answers (request-response cycle, middleware, WSGI vs ASGI, MVC→MVT)
- `courses/views.py` — `hello_view` function-based view
- `courses/urls.py` — maps `/api/hello/`

## How to run
```bash
pip install -r requirements.txt
cd coursemanager
python manage.py migrate
python manage.py runserver
```
Visit: http://127.0.0.1:8000/api/hello/ → should show "Course Management API is running"
