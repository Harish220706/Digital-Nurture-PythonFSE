"""add is_active to students

Revision ID: 0002_add_is_active
Revises: 0001_initial_schema
Create Date: 2026-07-25 10:15:00

"""
from alembic import op
import sqlalchemy as sa

revision = "0002_add_is_active"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "students",
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("students", "is_active")
