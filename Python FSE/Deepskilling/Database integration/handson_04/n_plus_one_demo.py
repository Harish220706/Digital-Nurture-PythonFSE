"""
Hands-On 4, Task 3 - Identify and Fix the N+1 Problem (Steps 56-59)

Uses psycopg2 directly (no ORM) so the query count is fully visible and
controlled by hand - this makes the N+1 pattern obvious before Hands-On 6
introduces the same problem again through SQLAlchemy.

Update DB_CONFIG below with your own PostgreSQL credentials before running.
"""

import time
import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "dbname": "college_db",
    "user": "postgres",
    "password": "your_password_here",
    "port": 5432,
}


def n_plus_one_version(conn):
    """Step 56: 1 query to get enrollments, then N queries for student names."""
    query_count = 0
    start = time.time()

    with conn.cursor() as cur:
        cur.execute("SELECT enrollment_id, student_id, course_id FROM enrollments;")
        query_count += 1
        enrollments = cur.fetchall()

        results = []
        for enrollment_id, student_id, course_id in enrollments:
            cur.execute(
                "SELECT first_name, last_name FROM students WHERE student_id = %s;",
                (student_id,),
            )
            query_count += 1
            first_name, last_name = cur.fetchone()
            results.append((enrollment_id, f"{first_name} {last_name}", course_id))

    duration = time.time() - start
    print(f"N+1 version: {query_count} queries executed in {duration:.4f}s")
    return results, query_count


def single_join_version(conn):
    """Step 57: one JOIN query fetches everything at once."""
    query_count = 0
    start = time.time()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT e.enrollment_id, s.first_name || ' ' || s.last_name, e.course_id
            FROM enrollments e
            JOIN students s ON s.student_id = e.student_id;
        """)
        query_count += 1
        results = cur.fetchall()

    duration = time.time() - start
    print(f"JOIN version: {query_count} query executed in {duration:.4f}s")
    return results, query_count


if __name__ == "__main__":
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        n1_results, n1_count = n_plus_one_version(conn)
        join_results, join_count = single_join_version(conn)

        # Step 58: compare round-trips
        print(f"\nRound-trip comparison: N+1 used {n1_count} queries, "
              f"JOIN used {join_count} query - a difference of {n1_count - join_count} round-trips.")

        assert sorted(n1_results) == sorted(join_results), "Results should be identical!"
        print("Both approaches returned identical data.")

        # Step 59: extrapolation comment
        # With 10,000 enrollments, the N+1 version would issue 1 + 10,000 =
        # 10,001 queries, versus a single JOIN query (1 total) - that's
        # 10,000 EXTRA round-trips purely from the N+1 pattern, each one
        # incurring its own network latency and query-planning overhead.
    finally:
        conn.close()
