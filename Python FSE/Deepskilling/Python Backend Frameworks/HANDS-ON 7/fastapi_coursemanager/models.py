from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    head_of_dept = Column(String(100))
    budget = Column(Numeric(12, 2), default=0)

    courses = relationship('Course', back_populates='department')


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    credits = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))

    department = relationship('Department', back_populates='courses')


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
    enrollment_year = Column(Integer)


class Enrollment(Base):
    __tablename__ = 'enrollments'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    enrollment_date = Column(Date)
    grade = Column(String(2), nullable=True)

    student = relationship('Student')
    course = relationship('Course')

    __table_args__ = (UniqueConstraint('student_id', 'course_id', name='uq_student_course'),)
