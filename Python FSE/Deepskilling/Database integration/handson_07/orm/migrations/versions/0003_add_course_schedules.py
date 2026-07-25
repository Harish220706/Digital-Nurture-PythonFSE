"""add course_schedules table

Revision ID: 0003_add_course_schedules
Revises: 0002_add_is_active
Create Date: 2026-07-25 10:30:00

"""
from alembic import op
import sqlalchemy as sa

revision = "0003_add_course_schedules"
down_revision = "0002_add_is_active"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "course_schedules",
        sa.Column("schedule_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("course_id", sa.Integer, sa.ForeignKey("courses.course_id")),
        sa.Column("day_of_week", sa.String(10)),
        sa.Column("start_time", sa.Time),
        sa.Column("end_time", sa.Time),
    )


def downgrade() -> None:
    op.drop_table("course_schedules")
