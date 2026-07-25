"""
Hands-On 6, Task 1 - SQLAlchemy models mirroring the college_db schema.
Run: python models.py  (creates all tables in college_db_orm)
"""

from sqlalchemy import (
    create_engine, Column, Integer, String, Date, DECIMAL, ForeignKey, CHAR
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Step 76: engine - update credentials/host as needed
# For MySQL: "mysql+mysqlconnector://user:password@localhost/college_db_orm"
DATABASE_URL = "postgresql+psycopg2://postgres:your_password_here@localhost:5432/college_db_orm"
engine = create_engine(DATABASE_URL, echo=False)


class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_name = Column(String(100), nullable=False)
    hod_name = Column(String(100))
    budget = Column(DECIMAL(12, 2))

    students = relationship("Student", back_populates="department")
    courses = relationship("Course", back_populates="department")
    professors = relationship("Professor", back_populates="department")


class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    date_of_birth = Column(Date)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    enrollment_year = Column(Integer)

    # Step 78: many-to-one relationship to Department
    department = relationship("Department", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")


class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(150), nullable=False)
    course_code = Column(String(20), unique=True)
    credits = Column(Integer)
    department_id = Column(Integer, ForeignKey("departments.department_id"))

    department = relationship("Department", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")


class Enrollment(Base):
    __tablename__ = "enrollments"

    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.student_id"))
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    enrollment_date = Column(Date)
    grade = Column(CHAR(2))

    # Step 78: many-to-one relationships to both Student and Course
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")


class Professor(Base):
    __tablename__ = "professors"

    professor_id = Column(Integer, primary_key=True, autoincrement=True)
    prof_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    salary = Column(DECIMAL(10, 2))

    department = relationship("Department", back_populates="professors")


if __name__ == "__main__":
    # Step 79: create all tables in a fresh database
    Base.metadata.create_all(engine)
    print("All tables created in college_db_orm.")
