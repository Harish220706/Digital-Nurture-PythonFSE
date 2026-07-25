"""
HANDS-ON 9 - Authentication & Security: JWT, OAuth2 concepts, CORS, OWASP awareness.
"""
from typing import Optional

from fastapi import FastAPI, Depends, Query, status, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException, RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from database import get_db, init_models
from models import Course, User
from schemas import CourseCreate, CourseUpdate, CourseResponse
from crud import get_course_or_404
from errors import http_exception_handler, validation_exception_handler
from deps import get_current_user
from auth_routes import router as auth_router

app = FastAPI(title='Course Management API', version='1.0')
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# CORS: allow the frontend dev server. CORS is enforced by the BROWSER, not the
# server - it does not protect server-to-server calls, only browser JS from other origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth_router)


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
    """Public - no auth required for reads."""
    query = select(Course)
    if search:
        like = f'%{search}%'
        query = query.where(or_(Course.name.ilike(like), Course.code.ilike(like)))

    total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar_one()
    offset = (page - 1) * page_size
    result = await db.execute(query.offset(offset).limit(page_size))
    courses = result.scalars().all()

    next_url = f'/api/v1/courses/?page={page + 1}&page_size={page_size}' if offset + page_size < total else None
    prev_url = f'/api/v1/courses/?page={page - 1}&page_size={page_size}' if page > 1 else None
    return {
        'count': total, 'next': next_url, 'previous': prev_url,
        'results': [CourseResponse.model_validate(c).model_dump() for c in courses],
    }


@app.post('/api/v1/courses/', response_model=CourseResponse, status_code=status.HTTP_201_CREATED, tags=['Courses'])
async def create_course(
    course: CourseCreate,
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),  # protected - 401 if no/invalid token
):
    new_course = Course(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    response.headers['Location'] = f'/api/v1/courses/{new_course.id}/'
    return new_course


@app.get('/api/v1/courses/{course_id}/', response_model=CourseResponse, tags=['Courses'])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    return await get_course_or_404(db, course_id)


@app.patch('/api/v1/courses/{course_id}/', response_model=CourseResponse, tags=['Courses'])
async def partial_update_course(
    course_id: int, payload: CourseUpdate, db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    course = await get_course_or_404(db, course_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    await db.commit()
    await db.refresh(course)
    return course


@app.delete('/api/v1/courses/{course_id}/', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def delete_course(
    course_id: int, db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),  # protected - 401 if no/invalid token
):
    course = await get_course_or_404(db, course_id)
    await db.delete(course)
    await db.commit()
