from typing import Optional, List

from fastapi import FastAPI, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db, init_models
from models import Course
from schemas import CourseCreate, CourseResponse

app = FastAPI(title='Course Management API', version='1.0')


@app.on_event('startup')
async def on_startup():
    await init_models()


@app.get('/')
async def root():
    return {'message': 'API running'}


@app.post('/api/courses/', response_model=CourseResponse, status_code=201)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    """FastAPI validates the body against CourseCreate automatically (422 on failure)."""
    new_course = Course(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


@app.get('/api/courses/{course_id}', response_model=CourseResponse)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    return result.scalar_one()


@app.get('/api/courses/', response_model=List[CourseResponse])
async def list_courses(
    skip: int = 0,
    limit: int = 10,
    department_id: Optional[int] = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    """Pagination + optional filtering by department_id."""
    query = select(Course)
    if department_id is not None:
        query = query.where(Course.department_id == department_id)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()
