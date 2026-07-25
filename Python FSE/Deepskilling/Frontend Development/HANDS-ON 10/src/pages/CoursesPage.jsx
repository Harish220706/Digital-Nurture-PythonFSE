import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchAllCourses, selectCourses, selectCoursesLoading, selectCoursesError } from '../store/coursesSlice';
import { enroll } from '../store/enrollmentSlice';

export default function CoursesPage() {
  const dispatch = useDispatch();
  const courses = useSelector(selectCourses);
  const loading = useSelector(selectCoursesLoading);
  const error = useSelector(selectCoursesError);

  useEffect(() => {
    dispatch(fetchAllCourses());
  }, [dispatch]);

  if (loading) return <p className="loading">Loading courses...</p>;
  if (error) return <p className="error-box">{error}</p>;

  return (
    <section>
      <h2>Courses</h2>
      <div className="course-grid">
        {courses.map((course) => (
          <article className="course-card" key={course.id}>
            <h3>{course.name}</h3>
            <p>{course.code}</p>
            <span className="credits">{course.credits} credits</span>
            <button type="button" onClick={() => dispatch(enroll(course))}>
              Enroll
            </button>
          </article>
        ))}
      </div>
    </section>
  );
}
