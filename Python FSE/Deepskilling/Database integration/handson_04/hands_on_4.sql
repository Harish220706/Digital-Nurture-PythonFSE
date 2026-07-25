-- =====================================================================
-- HANDS-ON 4: Query Optimisation — Indexes, EXPLAIN & the N+1 Problem
-- =====================================================================

-- =====================================================================
-- Task 1: Baseline Performance — No Indexes (Steps 48-50)
-- =====================================================================

EXPLAIN
SELECT s.first_name, s.last_name, c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

-- Sample baseline output (PostgreSQL, small sample dataset), recorded here
-- as required by Step 48 - your exact numbers will vary by machine/data
-- volume, but the SHAPE of the plan is what matters:
--
--  Hash Join  (cost=1.11..2.35 rows=4 width=72)
--    Hash Cond: (e.course_id = c.course_id)
--    ->  Hash Join  (cost=1.09..2.28 rows=4 width=13)
--          Hash Cond: (e.student_id = s.student_id)
--          ->  Seq Scan on enrollments e  (cost=0.00..1.10 rows=10 width=8)
--          ->  Hash  (cost=1.06..1.06 rows=6 width=13)
--                ->  Seq Scan on students s  (cost=0.00..1.06 rows=6 width=13)
--                      Filter: (enrollment_year = 2022)
--    ->  Hash  (cost=1.05..1.05 rows=5 width=67)
--          ->  Seq Scan on courses c  (cost=0.00..1.05 rows=5 width=67)
--
-- Step 49: the plan shows a Seq Scan on students with a Filter on
-- enrollment_year - this is exactly the table scan we'll target with an
-- index. enrollments and courses are also Seq Scanned (unavoidable at
-- this size without a WHERE on those tables specifically).
--
-- Step 50: estimated cost of the students Seq Scan above is
-- cost=0.00..1.06 (startup..total, in arbitrary planner cost units) for
-- an estimated 6 rows. On a small sample table this is already cheap -
-- the value of the upcoming index becomes apparent as this table grows
-- to thousands/millions of rows, where a full Seq Scan cost grows
-- linearly but an Index Scan cost grows roughly logarithmically.


-- =====================================================================
-- Task 2: Add Indexes and Compare Plans (Steps 51-55)
-- =====================================================================

-- Step 51: B-Tree index on students.enrollment_year
CREATE INDEX idx_students_enrollment_year ON students (enrollment_year);

-- Step 52: composite UNIQUE index - also prevents duplicate enrollments
CREATE UNIQUE INDEX idx_enrollments_student_course
    ON enrollments (student_id, course_id);

-- Step 53: index on courses.course_code
CREATE INDEX idx_courses_course_code ON courses (course_code);

-- Step 54: re-run EXPLAIN and compare
EXPLAIN
SELECT s.first_name, s.last_name, c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;
--
-- Expected change: the Seq Scan on students with Filter: (enrollment_year
-- = 2022) is replaced by an Index Scan (or Bitmap Index Scan) using
-- idx_students_enrollment_year, e.g.:
--   ->  Index Scan using idx_students_enrollment_year on students s
--         Index Cond: (enrollment_year = 2022)
-- On very small tables, PostgreSQL's planner may still choose a Seq Scan
-- even with the index present, because a Seq Scan on a handful of rows
-- can be cheaper than the overhead of an index lookup - this is expected
-- and normal; the benefit becomes decisive as row counts grow into the
-- thousands+.

-- Step 55: partial index for unevaluated enrollments
CREATE INDEX idx_enrollments_ungraded
    ON enrollments (student_id)
    WHERE grade IS NULL;

-- This index only covers rows where grade IS NULL, so it stays small and
-- fast specifically for queries like:
-- SELECT * FROM enrollments WHERE student_id = 4 AND grade IS NULL;
