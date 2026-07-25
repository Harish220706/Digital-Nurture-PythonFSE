import { Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { enroll } from '../store/enrollmentSlice';

export default function CourseCard({ id, name, code, credits, grade }) {
  const dispatch = useDispatch();
  const isEnrolled = useSelector((state) =>
    state.enrollment.enrolledCourses.some((c) => c.id === id)
  );

  return (
    <article className="course-card">
      <h3>
        <Link to={`/courses/${id}`}>{name}</Link>
      </h3>
      <p>{code}</p>
      <span className="credits">{credits} credits · Grade: {grade}</span>
      <button
        type="button"
        disabled={isEnrolled}
        onClick={() => dispatch(enroll({ id, name, code, credits, grade }))}
      >
        {isEnrolled ? 'Enrolled' : 'Enroll'}
      </button>
    </article>
  );
}
