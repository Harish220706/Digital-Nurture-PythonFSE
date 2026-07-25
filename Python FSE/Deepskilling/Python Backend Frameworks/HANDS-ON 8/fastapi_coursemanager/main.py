"""
HANDS-ON 8 - RESTful API Design Best Practices.
Refactor of the FastAPI course API (Hands-On 6/7) to follow REST
conventions: /api/v1/ versioning, offset pagination envelope,
search filtering, Location header on POST, and standardised errors.
"""
from datetime import date
from typing import Optional, List

from fastapi import FastAPI, Depends, Query, status, Response, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from database import get_db, init_models
from models import Course, Student, Enrollment
from schemas import CourseCreate, CourseUpdate, CourseResponse, StudentResponse
from crud import get_course_or_404
from errors import http_exception_handler, validation_exception_handler

# Versioning note (step 82): URL versioning (/api/v1/...) is used here because it
# is simple, visible, and easy to test directly in a browser. The alternative is
# HEADER versioning, e.g. `Accept: application/vnd.api+json;version=1` - this keeps
# URLs clean/stable long-term but is harder to explore without a tool like Postman.

app = FastAPI(title='Course Management API', version='1.0')
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.on_event('startup')
async def on_startup():
    await init_models()


@app.get('/api/v1/courses/', tags=['Courses'])
async def list_courses(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Offset pagination + case-insensitive search over name/code (DRF-style envelope)."""
    query = select(Course)
    if search:
        like = f'%{search}%'
        query = query.where(or_(Course.name.ilike(like), Course.code.ilike(like)))

    count_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = count_result.scalar_one()

    offset = (page - 1) * page_size
    result = await db.execute(query.offset(offset).limit(page_size))
    courses = result.scalars().all()

    base_url = '/api/v1/courses/'
    next_url = f'{base_url}?page={page + 1}&page_size={page_size}' if offset + page_size < total else None
    prev_url = f'{base_url}?page={page - 1}&page_size={page_size}' if page > 1 else None

    return {
        'count': total,
        'next': next_url,
        'previous': prev_url,
        'results': [CourseResponse.model_validate(c).model_dump() for c in courses],
    }


@app.post('/api/v1/courses/', response_model=CourseResponse, status_code=status.HTTP_201_CREATED, tags=['Courses'])
async def create_course(course: CourseCreate, response: Response, db: AsyncSession = Depends(get_db)):
    new_course = Course(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    response.headers['Location'] = f'/api/v1/courses/{new_course.id}/'
    return new_course


@app.get('/api/v1/courses/{course_id}/', response_model=CourseResponse, tags=['Courses'])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    return await get_course_or_404(db, course_id)


@app.put('/api/v1/courses/{course_id}/', response_model=CourseResponse, tags=['Courses'])
async def replace_course(course_id: int, payload: CourseCreate, db: AsyncSession = Depends(get_db)):
    """PUT = full replace, all fields required."""
    course = await get_course_or_404(db, course_id)
    for field, value in payload.model_dump().items():
        setattr(course, field, value)
    await db.commit()
    await db.refresh(course)
    return course


@app.patch('/api/v1/courses/{course_id}/', response_model=CourseResponse, tags=['Courses'])
async def partial_update_course(course_id: int, payload: CourseUpdate, db: AsyncSession = Depends(get_db)):
    """PATCH = partial update, only supplied fields change."""
    course = await get_course_or_404(db, course_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    await db.commit()
    await db.refresh(course)
    return course


@app.delete('/api/v1/courses/{course_id}/', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await get_course_or_404(db, course_id)
    await db.delete(course)
    await db.commit()
