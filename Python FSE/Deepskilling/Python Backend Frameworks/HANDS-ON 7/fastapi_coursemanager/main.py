from datetime import date
from typing import Optional, List

from fastapi import FastAPI, Depends, Query, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db, init_models
from models import Course, Student, Enrollment
from schemas import (
    CourseCreate, CourseUpdate, CourseResponse,
    StudentCreate, StudentResponse,
    EnrollmentCreate, EnrollmentResponse,
)
from crud import get_course_or_404, get_student_or_404

app = FastAPI(
    title='Course Management API',
    description='Backend API for the Digital Nurture 5.0 Course Management scenario.',
    version='1.0',
    contact={'name': 'Digital Nurture 5.0 POC', 'email': 'poc@example.edu'},
)


@app.on_event('startup')
async def on_startup():
    await init_models()


@app.get('/', tags=['Health'])
async def root():
    return {'message': 'API running'}


# ---------------- Courses ----------------

@app.get('/api/courses/', response_model=List[CourseResponse], tags=['Courses'])
async def list_courses(
    skip: int = 0,
    limit: int = 10,
    department_id: Optional[int] = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Course)
    if department_id is not None:
        query = query.where(Course.department_id == department_id)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@app.post(
    '/api/courses/',
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Courses'],
    summary='Create a new course',
    response_description='The created course',
)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    new_course = Course(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


@app.get('/api/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    return await get_course_or_404(db, course_id)


@app.put('/api/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def update_course(course_id: int, payload: CourseUpdate, db: AsyncSession = Depends(get_db)):
    course = await get_course_or_404(db, course_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    await db.commit()
    await db.refresh(course)
    return course


@app.delete('/api/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await get_course_or_404(db, course_id)
    await db.delete(course)
    await db.commit()


@app.get('/api/courses/{course_id}/students/', response_model=List[StudentResponse], tags=['Courses'])
async def students_in_course(course_id: int, db: AsyncSession = Depends(get_db)):
    await get_course_or_404(db, course_id)
    result = await db.execute(
        select(Student).join(Enrollment, Enrollment.student_id == Student.id)
        .where(Enrollment.course_id == course_id)
    )
    return result.scalars().all()


# ---------------- Students ----------------

@app.get('/api/students/', response_model=List[StudentResponse], tags=['Students'])
async def list_students(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student))
    return result.scalars().all()


@app.post('/api/students/', response_model=StudentResponse, status_code=201, tags=['Students'])
async def create_student(student: StudentCreate, db: AsyncSession = Depends(get_db)):
    new_student = Student(**student.model_dump())
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return new_student


# ---------------- Enrollments ----------------

def send_confirmation_email(student_email: str):
    """Simulated background task - runs AFTER the response is sent."""
    print(f'Sending confirmation to {student_email}')


@app.post('/api/enrollments/', response_model=EnrollmentResponse, status_code=201, tags=['Enrollments'])
async def create_enrollment(
    enrollment: EnrollmentCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    student = await get_student_or_404(db, enrollment.student_id)
    await get_course_or_404(db, enrollment.course_id)

    new_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        enrollment_date=date.today(),
    )
    db.add(new_enrollment)
    await db.commit()
    await db.refresh(new_enrollment)

    background_tasks.add_task(send_confirmation_email, student.email)
    return new_enrollment
