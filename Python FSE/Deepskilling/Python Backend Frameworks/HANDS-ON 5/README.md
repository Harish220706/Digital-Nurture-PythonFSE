# Hands-On 5 — Flask with SQLAlchemy ORM & Database Integration

## What's inside
- `flask_coursemanager/courses/models.py` — SQLAlchemy models (Department, Course, Student,
  Enrollment) with relationships and `to_dict()` serializer methods
- `flask_coursemanager/courses/routes.py` — routes now query the real database via the ORM,
  using `get_or_404` and a JOIN-based `/students/` endpoint
- `flask_coursemanager/shell_inserts.py` — sample data inserts for `flask shell`

## How to run
```bash
pip install -r requirements.txt
cd flask_coursemanager
export FLASK_APP="app:create_app"      # Windows: set FLASK_APP=app:create_app
flask db init
flask db migrate -m "initial schema"
flask db upgrade
flask shell < shell_inserts.py
python app.py
```
Visit: http://127.0.0.1:5000/api/courses/
