import { createContext, useState } from 'react';

export const EnrollmentContext = createContext(null);

// This Context provider is kept in the project so you can compare it
// side-by-side with the Redux Toolkit store in store/. The app below
// uses Redux as the source of truth (Task 3); this file demonstrates
// the Task 2 pattern and can be swapped in by wrapping <App /> with
// <EnrollmentProvider> in main.jsx instead of <Provider store={store}>.
export function EnrollmentProvider({ children }) {
  const [enrolledCourses, setEnrolledCourses] = useState([]);

  const enrollCourse = (course) => {
    setEnrolledCourses((prev) =>
      prev.some((c) => c.id === course.id) ? prev : [...prev, course]
    );
  };

  const removeCourse = (courseId) => {
    setEnrolledCourses((prev) => prev.filter((c) => c.id !== courseId));
  };

  return (
    <EnrollmentContext.Provider value={{ enrolledCourses, enrollCourse, removeCourse }}>
      {children}
    </EnrollmentContext.Provider>
  );
}
