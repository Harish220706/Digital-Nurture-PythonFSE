-- =====================================================================
-- HANDS-ON 3: Advanced SQL — Subqueries, Views & Transactions
-- Written for PostgreSQL; MySQL equivalents noted where syntax differs.
-- =====================================================================

-- =====================================================================
-- Task 1: Subqueries (Steps 35-38)
-- =====================================================================

-- Step 35: students enrolled in more courses than the average per student
-- (non-correlated subquery calculates the average)
SELECT student_id, COUNT(*) AS course_count
FROM enrollments
GROUP BY student_id
HAVING COUNT(*) > (
    SELECT AVG(course_count) FROM (
        SELECT COUNT(*) AS course_count
        FROM enrollments
        GROUP BY student_id
    ) AS per_student_counts
);

-- Step 36: courses where ALL enrolled students received an 'A'
-- (using NOT EXISTS - no enrollment in this course has a non-'A' grade)
SELECT DISTINCT c.course_name
FROM courses c
WHERE NOT EXISTS (
    SELECT 1
    FROM enrollments e
    WHERE e.course_id = c.course_id
      AND (e.grade IS DISTINCT FROM 'A')   -- MySQL: e.grade <> 'A' OR e.grade IS NULL
)
AND EXISTS (
    SELECT 1 FROM enrollments e2 WHERE e2.course_id = c.course_id
);

-- Step 37: highest-paid professor in each department (correlated subquery)
SELECT p.prof_name, p.department_id, p.salary
FROM professors p
WHERE p.salary = (
    SELECT MAX(p2.salary)
    FROM professors p2
    WHERE p2.department_id = p.department_id
);

-- Step 38: derived table - per-department avg salary, filtered above 85,000
SELECT dept_avg.department_id, dept_avg.avg_salary
FROM (
    SELECT department_id, AVG(salary) AS avg_salary
    FROM professors
    GROUP BY department_id
) AS dept_avg
WHERE dept_avg.avg_salary > 85000;


-- =====================================================================
-- Task 2: Creating and Using Views (Steps 39-43)
-- =====================================================================

-- Step 39: student enrollment summary with GPA
CREATE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    s.first_name || ' ' || s.last_name AS full_name,   -- MySQL: CONCAT(...)
    d.dept_name,
    COUNT(e.enrollment_id) AS courses_enrolled,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
        END
    ), 2) AS gpa
FROM students s
JOIN departments d ON s.department_id = d.department_id
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name, d.dept_name;

-- Step 40: per-course stats view
CREATE VIEW vw_course_stats AS
SELECT
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id) AS total_enrollments,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
        END
    ), 2) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_name, c.course_code;

-- Step 41: students with GPA above 3.0
SELECT full_name, gpa
FROM vw_student_enrollment_summary
WHERE gpa > 3.0;

-- Step 42: attempt to UPDATE through a multi-table view
-- UPDATE vw_student_enrollment_summary SET gpa = 4.0 WHERE student_id = 1;
-- --> This fails (or is rejected/ignored depending on engine) because the
-- view aggregates data from multiple joined tables (students, departments,
-- enrollments) via GROUP BY and JOIN. The database cannot unambiguously
-- determine which single underlying row(s) in which single underlying
-- table an UPDATE against a computed/aggregated column like "gpa" should
-- modify. Multi-table, grouped, or aggregate views are inherently
-- non-updatable in standard SQL - only views that map cleanly to a single
-- base table's rows (no joins, no GROUP BY, no aggregates) can be updated
-- directly.

-- Step 43: drop and recreate as a single-table view WITH CHECK OPTION
DROP VIEW IF EXISTS vw_student_enrollment_summary;
DROP VIEW IF EXISTS vw_course_stats;

-- Single-table subset view: only students enrolled in 2022, updatable
CREATE VIEW vw_students_2022 AS
SELECT student_id, first_name, last_name, email, department_id, enrollment_year
FROM students
WHERE enrollment_year = 2022
WITH CHECK OPTION;
-- WITH CHECK OPTION means: any UPDATE/INSERT through this view that would
-- produce a row where enrollment_year <> 2022 is rejected, since that row
-- would then be invisible through the view's own WHERE clause.

-- Recreate the two summary views for continued use in later hands-on exercises
CREATE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    s.first_name || ' ' || s.last_name AS full_name,
    d.dept_name,
    COUNT(e.enrollment_id) AS courses_enrolled,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4 WHEN 'B' THEN 3 WHEN 'C' THEN 2
            WHEN 'D' THEN 1 WHEN 'F' THEN 0
        END
    ), 2) AS gpa
FROM students s
JOIN departments d ON s.department_id = d.department_id
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name, d.dept_name;

CREATE VIEW vw_course_stats AS
SELECT
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id) AS total_enrollments,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4 WHEN 'B' THEN 3 WHEN 'C' THEN 2
            WHEN 'D' THEN 1 WHEN 'F' THEN 0
        END
    ), 2) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_name, c.course_code;


-- =====================================================================
-- Task 3: Stored Procedures / Functions and Transactions (Steps 44-47)
-- =====================================================================

-- Step 44 (PostgreSQL): fn_enroll_student
CREATE OR REPLACE FUNCTION fn_enroll_student(
    p_student_id INT,
    p_course_id INT,
    p_enrollment_date DATE
) RETURNS VOID AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM enrollments
        WHERE student_id = p_student_id AND course_id = p_course_id
    ) THEN
        RAISE EXCEPTION 'Student % is already enrolled in course %', p_student_id, p_course_id;
    END IF;

    INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
    VALUES (p_student_id, p_course_id, p_enrollment_date, NULL);
END;
$$ LANGUAGE plpgsql;

-- MySQL equivalent (Step 44):
-- DELIMITER $$
-- CREATE PROCEDURE sp_enroll_student(
--     IN p_student_id INT, IN p_course_id INT, IN p_enrollment_date DATE
-- )
-- BEGIN
--     IF EXISTS (SELECT 1 FROM enrollments WHERE student_id = p_student_id AND course_id = p_course_id) THEN
--         SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Student already enrolled in this course';
--     ELSE
--         INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
--         VALUES (p_student_id, p_course_id, p_enrollment_date, NULL);
--     END IF;
-- END$$
-- DELIMITER ;

-- Step 45: department_transfer_log table + sp_transfer_student
CREATE TABLE IF NOT EXISTS department_transfer_log (
    log_id          SERIAL PRIMARY KEY,
    student_id      INT NOT NULL,
    old_department  INT,
    new_department  INT,
    transferred_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION fn_transfer_student(
    p_student_id INT,
    p_new_department_id INT
) RETURNS VOID AS $$
DECLARE
    v_old_department INT;
BEGIN
    SELECT department_id INTO v_old_department FROM students WHERE student_id = p_student_id;

    UPDATE students SET department_id = p_new_department_id WHERE student_id = p_student_id;

    INSERT INTO department_transfer_log (student_id, old_department, new_department)
    VALUES (p_student_id, v_old_department, p_new_department_id);
    -- If either statement above fails (e.g. invalid FK on new_department_id),
    -- PostgreSQL functions run inside the calling transaction, so the whole
    -- transaction rolls back automatically on error - no explicit ROLLBACK
    -- needed inside the function itself.
END;
$$ LANGUAGE plpgsql;

-- Step 46: test the transaction with a deliberately invalid department id
BEGIN;
    SELECT fn_transfer_student(1, 9999);  -- 9999 does not exist in departments -> FK violation
    -- Expect an error here; the UPDATE to students is rolled back along with it.
ROLLBACK;

-- Verify student 1's department_id is unchanged:
SELECT student_id, department_id FROM students WHERE student_id = 1;

-- Step 47: SAVEPOINT demonstration
BEGIN;
    INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
    VALUES (2, 2, CURRENT_DATE, NULL);

    SAVEPOINT after_first_insert;

    -- Deliberately fail: invalid course_id (violates FK)
    INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
    VALUES (2, 9999, CURRENT_DATE, NULL);

    ROLLBACK TO SAVEPOINT after_first_insert;
COMMIT;

-- Verify: the first insert (student 2, course 2) should be present;
-- the failed second insert should not be.
SELECT * FROM enrollments WHERE student_id = 2 AND course_id IN (2, 9999);
