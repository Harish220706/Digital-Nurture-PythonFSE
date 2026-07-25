import apiClient from './apiClient';

// Task 1, step 139: components only ever call these functions, never Axios directly
export function getAllCourses() {
  return apiClient.get('/posts?_limit=5').then((posts) =>
    posts.map((p, i) => ({
      id: p.id,
      name: p.title.slice(0, 24),
      code: `CS10${i + 1}`,
      credits: 3 + (i % 2),
      grade: 'A'
    }))
  );
}

export function getCourseById(id) {
  return apiClient.get(`/posts/${id}`).then((p) => ({
    id: p.id,
    name: p.title.slice(0, 24),
    code: `CS10${id}`,
    credits: 3,
    grade: 'A'
  }));
}

export function enrollStudent(studentId, courseId) {
  return apiClient.post('/posts', { studentId, courseId });
}
