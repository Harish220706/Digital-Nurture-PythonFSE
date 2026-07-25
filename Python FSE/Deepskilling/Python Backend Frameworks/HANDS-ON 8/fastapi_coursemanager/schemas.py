from typing import Optional, List
from pydantic import BaseModel, ConfigDict, EmailStr


class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int
    department_id: int


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None


class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    department_id: int
    model_config = ConfigDict(from_attributes=True)


class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    department_id: Optional[int] = None
    enrollment_year: int


class StudentResponse(StudentCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentResponse(EnrollmentCreate):
    id: int
    grade: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class DepartmentResponse(BaseModel):
    id: int
    name: str
    head_of_dept: str
    courses: List[CourseResponse] = []
    model_config = ConfigDict(from_attributes=True)
