"""
Hands-On 6, Task 3 - Eager Loading to Fix N+1 (Steps 87-91)

COMPARISON SUMMARY (as required by Step 90):
----------------------------------------------
crud.py's read_enrollments_n_plus_1() with 4 enrollments issued:
  1 query for all enrollments
  + up to 4 queries for e.student (one per row, deduplicated by session
    identity map if the same student repeats)
  + up to 4 queries for e.course
  = up to 9 queries total for just 4 enrollment rows (13 in the original
    12-row sample dataset from Hands-On 2, matching the exercise's
    expected "13 queries" baseline).

This file's read_enrollments_eager() issues exactly 1 SQL query total
(a single statement with JOINs), regardless of how many enrollment rows
exist - confirmed by counting SQL log lines with echo=True.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload

from models import Enrollment

DATABASE_URL = "postgresql+psycopg2://postgres:your_password_here@localhost:5432/college_db_orm"
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)


def read_enrollments_eager(session):
    # Step 88: joinedload eliminates N+1 - one SQL statement with JOINs
    enrollments = (
        session.query(Enrollment)
        .options(
            joinedload(Enrollment.student),
            joinedload(Enrollment.course),
        )
        .all()
    )
    for e in enrollments:
        print(f"{e.student.first_name} {e.student.last_name} -> {e.course.course_name}")
    return enrollments


if __name__ == "__main__":
    session = Session()
    try:
        print("--- Eager-loaded query (watch the SQL log - should be 1 statement) ---")
        read_enrollments_eager(session)
    finally:
        session.close()


# Step 91 (Bonus) - Django ORM equivalent, for reference:
#
#   from myapp.models import Enrollment
#   enrollments = Enrollment.objects.select_related('student', 'course').all()
#   for e in enrollments:
#       print(f"{e.student.first_name} {e.student.last_name} -> {e.course.course_name}")
#
# select_related() performs a SQL JOIN and includes the related object's
# fields in the SELECT statement, achieving the same single-query result
# as SQLAlchemy's joinedload().
