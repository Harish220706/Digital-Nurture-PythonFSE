"""
HANDS-ON 5 - Task 1, step 51: sample inserts.
Run with: flask shell < shell_inserts.py  (with FLASK_APP=app:create_app set as a factory)
or paste into `flask shell` interactively.
"""
from app import db
from courses.models import Department, Course

d1 = Department(name='Computer Science', head_of_dept='Dr. Rao', budget=500000)
d2 = Department(name='Electrical Engineering', head_of_dept='Dr. Iyer', budget=400000)
db.session.add_all([d1, d2])
db.session.commit()

c1 = Course(name='Data Structures', code='CS101', credits=4, department_id=d1.id)
c2 = Course(name='Operating Systems', code='CS102', credits=4, department_id=d1.id)
c3 = Course(name='Circuits', code='EE101', credits=3, department_id=d2.id)
db.session.add_all([c1, c2, c3])
db.session.commit()

print(Course.query.all())
