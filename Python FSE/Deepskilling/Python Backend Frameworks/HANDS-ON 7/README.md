# Hands-On 7 — FastAPI: Dependency Injection, CRUD & OpenAPI Docs

## What's inside
- `fastapi_coursemanager/crud.py` — `get_course_or_404` / `get_student_or_404` helpers using `HTTPException`
- `fastapi_coursemanager/main.py` — full CRUD for Courses (incl. PATCH-style partial `PUT` via
  `exclude_unset`), Students, and Enrollments; `DELETE` returns 204; `POST` returns 201;
  a `BackgroundTasks` confirmation "email" on enrollment; OpenAPI tags/summary/description

## How to run
```bash
pip install -r requirements.txt
cd fastapi_coursemanager
uvicorn main:app --reload
```
- Swagger UI (grouped by tag): http://127.0.0.1:8000/docs
- `POST /api/enrollments/` returns 201 immediately; check the terminal for the
  "Sending confirmation to ..." print that appears right after the response.
