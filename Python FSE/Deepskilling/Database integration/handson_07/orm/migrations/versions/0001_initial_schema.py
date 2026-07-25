"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-07-25 10:00:00

"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "departments",
        sa.Column("department_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("dept_name", sa.String(100), nullable=False),
        sa.Column("hod_name", sa.String(100)),
        sa.Column("budget", sa.DECIMAL(12, 2)),
    )

    op.create_table(
        "students",
        sa.Column("student_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("first_name", sa.String(50), nullable=False),
        sa.Column("last_name", sa.String(50), nullable=False),
        sa.Column("email", sa.String(100), nullable=False, unique=True),
        sa.Column("date_of_birth", sa.Date),
        sa.Column("department_id", sa.Integer, sa.ForeignKey("departments.department_id")),
        sa.Column("enrollment_year", sa.Integer),
    )

    op.create_table(
        "courses",
        sa.Column("course_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("course_name", sa.String(150), nullable=False),
        sa.Column("course_code", sa.String(20), unique=True),
        sa.Column("credits", sa.Integer),
        sa.Column("department_id", sa.Integer, sa.ForeignKey("departments.department_id")),
    )

    op.create_table(
        "enrollments",
        sa.Column("enrollment_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("student_id", sa.Integer, sa.ForeignKey("students.student_id")),
        sa.Column("course_id", sa.Integer, sa.ForeignKey("courses.course_id")),
        sa.Column("enrollment_date", sa.Date),
        sa.Column("grade", sa.CHAR(2)),
    )

    op.create_table(
        "professors",
        sa.Column("professor_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("prof_name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(100), unique=True),
        sa.Column("department_id", sa.Integer, sa.ForeignKey("departments.department_id")),
        sa.Column("salary", sa.DECIMAL(10, 2)),
    )


def downgrade() -> None:
    op.drop_table("professors")
    op.drop_table("enrollments")
    op.drop_table("courses")
    op.drop_table("students")
    op.drop_table("departments")
