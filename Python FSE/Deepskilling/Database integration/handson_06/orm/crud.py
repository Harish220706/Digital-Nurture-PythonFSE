"""
Hands-On 6, Task 2 - CRUD Operations via SQLAlchemy ORM
"""

from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Department, Student, Course, Enrollment, Professor

# echo=True (Step 84) prints every SQL statement issued - essential for
# spotting N+1 query patterns.
DATABASE_URL = "postgresql+psycopg2://postgres:your_password_here@localhost:5432/college_db_orm"
engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine)


def seed_data(session):
    # Step 81: 3 departments, 5 students
    cs = Department(dept_name="Computer Science", hod_name="Dr. Ramesh Kumar", budget=850000.00)
    ec = Department(dept_name="Electronics", hod_name="Dr. Priya Nair", budget=620000.00)
    me = Department(dept_name="Mechanical", hod_name="Dr. Suresh Iyer", budget=540000.00)
    session.add_all([cs, ec, me])
    session.commit()

    students = [
        Student(first_name="Arjun", last_name="Mehta", email="arjun.mehta@college.edu",
                date_of_birth=date(2003, 4, 12), department_id=cs.department_id, enrollment_year=2022),
        Student(first_name="Priya", last_name="Suresh", email="priya.suresh@college.edu",
                date_of_birth=date(2003, 7, 25), department_id=cs.department_id, enrollment_year=2022),
        Student(first_name="Rohan", last_name="Verma", email="rohan.verma@college.edu",
                date_of_birth=date(2002, 11, 8), department_id=ec.department_id, enrollment_year=2021),
        Student(first_name="Sneha", last_name="Patel", email="sneha.patel@college.edu",
                date_of_birth=date(2004, 1, 30), department_id=me.department_id, enrollment_year=2023),
        Student(first_name="Vikram", last_name="Das", email="vikram.das@college.edu",
                date_of_birth=date(2003, 9, 14), department_id=cs.department_id, enrollment_year=2022),
    ]
    session.add_all(students)
    session.commit()

    # Step 82: 3 courses, 4 enrollments
    courses = [
        Course(course_name="Data Structures & Algorithms", course_code="CS101", credits=4, department_id=cs.department_id),
        Course(course_name="Database Management Systems", course_code="CS102", credits=3, department_id=cs.department_id),
        Course(course_name="Circuit Theory", course_code="EC101", credits=3, department_id=ec.department_id),
    ]
    session.add_all(courses)
    session.commit()

    enrollments = [
        Enrollment(student_id=students[0].student_id, course_id=courses[0].course_id,
                   enrollment_date=date(2022, 7, 1), grade="A"),
        Enrollment(student_id=students[1].student_id, course_id=courses[0].course_id,
                   enrollment_date=date(2022, 7, 1), grade="B"),
        Enrollment(student_id=students[0].student_id, course_id=courses[1].course_id,
                   enrollment_date=date(2022, 7, 1), grade="B"),
        Enrollment(student_id=students[2].student_id, course_id=courses[2].course_id,
                   enrollment_date=date(2021, 7, 1), grade="A"),
    ]
    session.add_all(enrollments)
    session.commit()

    return cs, students, courses, enrollments


def read_cs_students(session):
    # Step 83: students in 'Computer Science'
    return (
        session.query(Student)
        .join(Department)
        .filter(Department.dept_name == "Computer Science")
        .all()
    )


def read_enrollments_n_plus_1(session):
    # Step 84: THIS TRIGGERS THE N+1 PROBLEM.
    # session.query(Enrollment).all() issues 1 query. Then accessing
    # enrollment.student.first_name and enrollment.course.course_name for
    # EACH row triggers a separate lazy-load SELECT per relationship
    # access, per row - N extra queries. With echo=True you will see one
    # SELECT ... FROM enrollments, followed by repeated
    # SELECT ... FROM students WHERE student_id = ? and
    # SELECT ... FROM courses WHERE course_id = ? for every row.
    enrollments = session.query(Enrollment).all()
    for e in enrollments:
        print(f"{e.student.first_name} {e.student.last_name} -> {e.course.course_name}")
    return enrollments


def update_student_enrollment_year(session, email, new_year):
    # Step 85
    student = session.query(Student).filter(Student.email == email).first()
    if student:
        student.enrollment_year = new_year
        session.commit()
    return student


def delete_enrollment(session, enrollment_id):
    # Step 86
    enrollment = session.get(Enrollment, enrollment_id)
    if enrollment:
        session.delete(enrollment)
        session.commit()
        return True
    return False


if __name__ == "__main__":
    session = Session()
    try:
        seed_data(session)

        cs_students = read_cs_students(session)
        print("CS students:", [s.first_name for s in cs_students])

        print("\n--- N+1 demonstration (watch the SQL log above) ---")
        read_enrollments_n_plus_1(session)

        updated = update_student_enrollment_year(session, "arjun.mehta@college.edu", 2023)
        print("\nUpdated enrollment_year for:", updated.email if updated else "not found")

        first_enrollment = session.query(Enrollment).first()
        if first_enrollment:
            deleted = delete_enrollment(session, first_enrollment.enrollment_id)
            print("Deleted enrollment:", deleted)
    finally:
        session.close()
