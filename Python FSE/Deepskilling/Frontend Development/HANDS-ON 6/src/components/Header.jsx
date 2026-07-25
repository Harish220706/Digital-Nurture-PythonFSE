import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';

export default function Header({ siteName }) {
  const enrolledCount = useSelector((state) => state.enrollment.enrolledCourses.length);

  return (
    <header>
      <div className="site-name">{siteName}</div>
      <nav aria-label="Main navigation">
        <ul>
          <li><Link to="/" className="nav-link">Home</Link></li>
          <li><Link to="/courses" className="nav-link">Courses</Link></li>
          <li>
            <Link to="/profile" className="nav-link">
              Profile <span className="badge">{enrolledCount}</span>
            </Link>
          </li>
        </ul>
      </nav>
    </header>
  );
}
