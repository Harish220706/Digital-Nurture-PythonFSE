import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { courses } from '../data/courses';
import { enroll } from '../store/enrollmentSlice';

export default function CourseDetailPage() {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const course = courses.find((c) => c.id === Number(courseId));
  const isEnrolled = useSelector((state) =>
    course ? state.enrollment.enrolledCourses.some((c) => c.id === course.id) : false
  );

  if (!course) {
    return <p>Course not found.</p>;
  }

  const handleEnroll = () => {
    dispatch(enroll(course));
    navigate('/profile');
  };

  return (
    <section className="course-card" style={{ maxWidth: 480 }}>
      <h2>{course.name}</h2>
      <p>{course.code}</p>
      <span className="credits">{course.credits} credits · Grade: {course.grade}</span>
      <button type="button" disabled={isEnrolled} onClick={handleEnroll}>
        {isEnrolled ? 'Enrolled' : 'Enroll'}
      </button>
    </section>
  );
}
