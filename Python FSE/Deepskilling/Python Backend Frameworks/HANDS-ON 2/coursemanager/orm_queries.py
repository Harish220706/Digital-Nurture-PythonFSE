"""
HANDS-ON 2 - Task 2: Django ORM Queries
Run these inside `python manage.py shell` (paste line by line), or
`python manage.py shell < orm_queries.py`.
"""
from courses.models import Department, Course, Student, Enrollment
from django.db.models import Count, F

# Step 16: create sample data
cs = Department.objects.create(name='Computer Science', head_of_dept='Dr. Rao', budget=500000)
ee = Department.objects.create(name='Electrical Engineering', head_of_dept='Dr. Iyer', budget=400000)

c1 = Course.objects.create(name='Data Structures', code='CS101', credits=4, department=cs)
c2 = Course.objects.create(name='Operating Systems', code='CS102', credits=4, department=cs)
c3 = Course.objects.create(name='Circuits', code='EE101', credits=3, department=ee)
c4 = Course.objects.create(name='Signals', code='EE102', credits=3, department=ee)

Student.objects.create(first_name='Asha', last_name='Rao', email='asha@college.edu', department=cs, enrollment_year=2024)
Student.objects.create(first_name='Ravi', last_name='Kumar', email='ravi@college.edu', department=cs, enrollment_year=2024)
Student.objects.create(first_name='Priya', last_name='Nair', email='priya@college.edu', department=ee, enrollment_year=2023)
Student.objects.create(first_name='Karthik', last_name='S', email='karthik@college.edu', department=ee, enrollment_year=2023)
Student.objects.create(first_name='Divya', last_name='M', email='divya@college.edu', department=cs, enrollment_year=2025)

# Step 17: filter across a ForeignKey using __
cs_courses = Course.objects.filter(department__name='Computer Science')
print(list(cs_courses))

# Step 18: annotate + count per department
dept_counts = Department.objects.annotate(course_count=Count('courses'))
for d in dept_counts:
    print(d.name, d.course_count)

# Step 19: select_related to avoid N+1 queries
students_with_dept = Student.objects.select_related('department').all()
for s in students_with_dept:
    print(s, '-', s.department)

# Step 20: bulk update using F() - calculation happens in the DB
Department.objects.update(budget=F('budget') * 1.1)
