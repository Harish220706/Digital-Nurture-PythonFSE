# Hands-On 7 — Migrations & Versioning with Alembic

This folder already contains the finished migration files
(`migrations/versions/0001_initial_schema.py`,
`0002_add_is_active.py`, `0003_add_course_schedules.py`) so you can see
exactly what `--autogenerate` would produce. To actually reproduce this
from scratch yourself (which is what the exercise is really testing),
follow the commands below in order.

## Setup

```bash
cd handson_07/orm
pip install alembic sqlalchemy psycopg2-binary
```

Update the connection string in **both** `alembic.ini` and `migrations/env.py`
(via `models.py`) to match your local PostgreSQL credentials before running
anything.

## Task 1 — Baseline migration (steps 92–97)

```bash
# 92: initialise Alembic (only needed if starting from an empty folder —
#     this repo already has migrations/ set up for you)
alembic init migrations

# 93 & 94: point alembic.ini and migrations/env.py at your DB + models
#     (already done in this folder — see alembic.ini and env.py)

# 95: generate the first migration from the models
alembic revision --autogenerate -m "initial schema"

# 96: inspect migrations/versions/0001_initial_schema.py — confirm it has
#     upgrade() and downgrade() functions (it does, see the file)

# 97: apply it
alembic upgrade head
```

Verify: `alembic current` should print the `0001_initial_schema` revision
hash, and the `alembic_version` table should now exist in `college_db_orm`
alongside all 5 original tables.

## Task 2 — Incremental migrations (steps 98–103)

```bash
# 98: add is_active to the Student model — already done in models.py

# 99: generate the migration
alembic revision --autogenerate -m "add is_active to students"

# 100: inspect 0002_add_is_active.py — confirm upgrade() adds the column
#      and downgrade() drops it (it does, see the file)

# 101: apply it
alembic upgrade head

# 102: add CourseSchedule model — already done in models.py — then:
alembic revision --autogenerate -m "add course_schedules table"
alembic upgrade head

# 103: view the full chain
alembic history --verbose
```

Expected `alembic history` output (3 revisions, oldest to newest):
```
0001_initial_schema -> 0002_add_is_active -> 0003_add_course_schedules (head)
```

## Task 3 — Rollback and recovery (steps 104–108)

```bash
# 104: note the current head
alembic current

# 105: step back one revision
alembic downgrade -1
# Verify: the is_active column should now be gone from students.

# 106: roll all the way back to nothing
alembic downgrade base
# Verify: all 5 original tables (and course_schedules, is_active) are gone.

# 107: re-apply everything
alembic upgrade head
# Verify: alembic current matches the 0003_add_course_schedules hash again,
# and all tables/columns are back.
```

### Bonus — Django migrations equivalent (step 108)

If you were using Django instead of SQLAlchemy/Alembic, the equivalent
workflow would be:

```bash
python manage.py makemigrations      # generates a migration file, like `alembic revision --autogenerate`
python manage.py migrate              # applies pending migrations, like `alembic upgrade head`

# Roll back to a specific earlier migration:
python manage.py migrate <app_name> <previous_migration_number>
```

Django numbers its migrations sequentially per-app (e.g. `0001_initial`,
`0002_add_is_active_to_student`) and tracks applied state in its own
`django_migrations` table — conceptually identical to Alembic's
`alembic_version` table, just scoped per-app instead of per-project.
