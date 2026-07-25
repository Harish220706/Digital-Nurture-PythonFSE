import { useSelector, useDispatch } from 'react-redux';
import { unenroll } from '../store/enrollmentSlice';

export default function ProfilePage() {
  const enrolledCourses = useSelector((state) => state.enrollment.enrolledCourses);
  const dispatch = useDispatch();

  const totalCredits = enrolledCourses.reduce((sum, c) => sum + c.credits, 0);

  return (
    <section>
      <h2>My Profile</h2>
      <p>Enrolled courses: {enrolledCourses.length} &middot; Total credits: {totalCredits}</p>
      <div className="course-grid">
        {enrolledCourses.map((course) => (
          <article className="course-card" key={course.id}>
            <h3>{course.name}</h3>
            <span className="credits">{course.credits} credits</span>
            <button type="button" onClick={() => dispatch(unenroll(course.id))}>
              Remove
            </button>
          </article>
        ))}
      </div>
      {enrolledCourses.length === 0 && <p>You have not enrolled in any courses yet.</p>}
    </section>
  );
}
