# Hands-On 2 — Django Models, ORM & Admin Interface

## What's inside
- `coursemanager/courses/models.py` — Department, Course, Student, Enrollment
- `coursemanager/courses/migrations/0001_initial.py` — initial migration
- `coursemanager/courses/admin.py` — admin registration with list_display/search_fields/list_filter
- `coursemanager/orm_queries.py` — Task 2 ORM query examples (filter, annotate, select_related, F())

## How to run
```bash
pip install -r requirements.txt
cd coursemanager
python manage.py migrate
python manage.py createsuperuser   # e.g. admin / admin@college.edu
python manage.py runserver
```
- Admin: http://127.0.0.1:8000/admin/
- Try ORM queries: `python manage.py shell < orm_queries.py`
- Confirm tables: `python manage.py dbshell` then `.tables` (sqlite)
