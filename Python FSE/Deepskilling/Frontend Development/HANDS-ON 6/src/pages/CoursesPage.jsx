import { useState } from 'react';
import { courses } from '../data/courses';
import CourseCard from '../components/CourseCard';

export default function CoursesPage() {
  const [searchTerm, setSearchTerm] = useState('');

  const filtered = courses.filter((c) =>
    c.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <section>
      <h2>Courses</h2>
      <input
        type="text"
        placeholder="Search courses..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        aria-label="Search courses"
      />
      <div className="course-grid">
        {filtered.map((course) => (
          <CourseCard key={course.id} {...course} />
        ))}
      </div>
    </section>
  );
}
