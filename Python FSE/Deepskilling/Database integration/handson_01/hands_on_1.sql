-- =====================================================================
-- HANDS-ON 1: Schema Design & Core SQL — DDL and Normalisation
-- Target: PostgreSQL (MySQL equivalents noted in comments where they differ)
-- =====================================================================

-- Task 1, Step 1: create the database
-- Run this line separately (most clients don't allow CREATE DATABASE
-- inside the same transaction/script as other DDL):
CREATE DATABASE college_db;

-- Then connect to college_db before running everything below.
-- \c college_db   (psql)   |   USE college_db;  (MySQL)

-- ---------------------------------------------------------------------
-- Task 1, Steps 2-4: CREATE TABLE statements with constraints
-- Order matters: departments first, since other tables reference it.
-- ---------------------------------------------------------------------

CREATE TABLE departments (
    department_id   SERIAL PRIMARY KEY,          -- MySQL: INT AUTO_INCREMENT PRIMARY KEY
    dept_name       VARCHAR(100) NOT NULL,
    hod_name        VARCHAR(100),
    budget          DECIMAL(12,2)
);

CREATE TABLE students (
    student_id       SERIAL PRIMARY KEY,          -- MySQL: INT AUTO_INCREMENT PRIMARY KEY
    first_name       VARCHAR(50) NOT NULL,
    last_name        VARCHAR(50) NOT NULL,
    email            VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth    DATE,
    department_id    INT,
    enrollment_year  INT,
    CONSTRAINT fk_students_department
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE courses (
    course_id       SERIAL PRIMARY KEY,           -- MySQL: INT AUTO_INCREMENT PRIMARY KEY
    course_name     VARCHAR(150) NOT NULL,
    course_code     VARCHAR(20) UNIQUE,
    credits         INT,
    department_id   INT,
    CONSTRAINT fk_courses_department
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE enrollments (
    enrollment_id    SERIAL PRIMARY KEY,          -- MySQL: INT AUTO_INCREMENT PRIMARY KEY
    student_id       INT,
    course_id        INT,
    enrollment_date  DATE,
    grade            CHAR(2),
    CONSTRAINT fk_enrollments_student
        FOREIGN KEY (student_id) REFERENCES students(student_id),
    CONSTRAINT fk_enrollments_course
        FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE professors (
    professor_id    SERIAL PRIMARY KEY,           -- MySQL: INT AUTO_INCREMENT PRIMARY KEY
    prof_name       VARCHAR(100) NOT NULL,
    email           VARCHAR(100) UNIQUE,
    department_id   INT,
    salary          DECIMAL(10,2),
    CONSTRAINT fk_professors_department
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Verify: \d students   (psql)   |   DESCRIBE students;  (MySQL)


-- =====================================================================
-- Task 2: Normalisation Analysis (Steps 6-9)
-- =====================================================================

-- 1NF ANALYSIS:
-- Every column in every table above holds a single atomic value (e.g.,
-- first_name holds one name, grade holds one letter). A HYPOTHETICAL
-- 1NF VIOLATION would be storing multiple phone numbers in one column,
-- e.g. phone_numbers = '9876543210, 8765432109' — this is non-atomic
-- and would need to be split into a separate student_phone_numbers table
-- (one row per number) to satisfy 1NF.

-- 2NF ANALYSIS (enrollments table):
-- enrollments has a composite candidate key of (student_id, course_id).
-- Its non-key columns are enrollment_date and grade. Both depend on the
-- FULL composite key (a specific student's grade IN a specific course),
-- not on student_id or course_id alone — so there is no partial
-- dependency, and 2NF holds.

-- 3NF ANALYSIS:
-- No non-key column in any table depends transitively on another
-- non-key column. Storing dept_name directly in the students table WOULD
-- violate 3NF, because dept_name depends on department_id, which depends
-- on student_id (student_id -> department_id -> dept_name is a
-- transitive dependency) rather than depending directly on student_id.
-- Keeping department_id as a foreign key (and looking up dept_name via
-- JOIN) is what keeps the schema in 3NF.

-- 3NF ANALYSIS SPECIFIC TO enrollments (Step 9 requirement):
-- enrollment_date and grade both depend only on the (student_id,
-- course_id) composite key directly - neither one depends on the other
-- non-key column, so there is no transitive dependency and enrollments
-- satisfies 3NF.


-- =====================================================================
-- Task 3: Alter and Extend the Schema (Steps 10-14)
-- =====================================================================

-- Step 10: add phone_number to students
ALTER TABLE students ADD COLUMN phone_number VARCHAR(15);

-- Step 11: add max_seats to courses with a default
ALTER TABLE courses ADD COLUMN max_seats INT DEFAULT 60;

-- Step 12: CHECK constraint on grade
ALTER TABLE enrollments
    ADD CONSTRAINT chk_grade_valid
    CHECK (grade IN ('A','B','C','D','F') OR grade IS NULL);

-- Step 13: rename hod_name to head_of_dept
-- PostgreSQL:
ALTER TABLE departments RENAME COLUMN hod_name TO head_of_dept;
-- MySQL 8+ equivalent:
-- ALTER TABLE departments CHANGE hod_name head_of_dept VARCHAR(100);

-- Step 14: drop phone_number (simulate rollback)
ALTER TABLE students DROP COLUMN phone_number;

-- Verify changes:
-- PostgreSQL: SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'students';
-- MySQL:      SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'students' AND table_schema = 'college_db';
