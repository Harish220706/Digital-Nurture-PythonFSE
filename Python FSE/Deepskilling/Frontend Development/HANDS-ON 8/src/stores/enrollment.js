import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

// Task 3, step 117: Composition-API style Pinia store
export const useEnrollmentStore = defineStore('enrollment', () => {
  const enrolledCourses = ref([]);

  const totalCredits = computed(() =>
    enrolledCourses.value.reduce((sum, c) => sum + c.credits, 0)
  );

  function enroll(course) {
    const exists = enrolledCourses.value.some((c) => c.id === course.id);
    if (!exists) enrolledCourses.value.push(course);
  }

  function unenroll(courseId) {
    enrolledCourses.value = enrolledCourses.value.filter((c) => c.id !== courseId);
  }

  // Task 3 (Hands-On 10 preview), step 149: async action + $reset pattern
  async function fetchAndEnroll(courseId) {
    const res = await fetch(`https://jsonplaceholder.typicode.com/posts/${courseId}`);
    const data = await res.json();
    enroll({ id: data.id, name: data.title.slice(0, 24), code: `CS10${data.id}`, credits: 3, grade: 'A' });
  }

  function $reset() {
    enrolledCourses.value = [];
  }

  return { enrolledCourses, totalCredits, enroll, unenroll, fetchAndEnroll, $reset };
});
