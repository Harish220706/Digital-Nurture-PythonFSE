# Hands-On 3 — Django REST Views, URL Routing & Forms (DRF)

## What's inside
- `courses/serializers.py` — ModelSerializers for all 4 models
- `courses/views.py` — Task 1 `CourseListView`/`CourseDetailView` (APIView) kept for reference,
  plus Task 2 `CourseViewSet`/`StudentViewSet`/`EnrollmentViewSet` (ModelViewSet) — the
  recommended approach, including a custom `/courses/{id}/students/` action
- `courses/urls.py` — `DefaultRouter` auto-generates all CRUD routes

## How to run
```bash
pip install -r requirements.txt
cd coursemanager
python manage.py migrate
python manage.py runserver
```
Endpoints (all under `/api/`):
- `GET/POST /api/courses/`
- `GET/PUT/PATCH/DELETE /api/courses/{id}/`
- `GET /api/courses/{id}/students/`  (custom action)
- `GET/POST /api/students/`, `GET/POST /api/enrollments/`

Test with Postman/Thunder Client.
