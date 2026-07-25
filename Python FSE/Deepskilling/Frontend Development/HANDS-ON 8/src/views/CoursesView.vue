<script setup>
import { ref, onMounted, computed } from 'vue';
import { courses } from '../data/courses';
import CourseCard from '../components/CourseCard.vue';
import { useEnrollmentStore } from '../stores/enrollment';

const courseList = ref([]);
const searchTerm = ref('');
const store = useEnrollmentStore();

onMounted(() => {
  courseList.value = courses;
});

const filteredCourses = computed(() =>
  courseList.value.filter((c) => c.name.toLowerCase().includes(searchTerm.value.toLowerCase()))
);
</script>

<template>
  <section>
    <h2>Courses</h2>
    <label for="search">Search courses</label>
    <input id="search" v-model="searchTerm" placeholder="Search courses..." />
    <div class="course-grid">
      <div v-for="course in filteredCourses" :key="course.id">
        <CourseCard v-bind="course" />
        <button type="button" @click="store.enroll(course)">Enroll</button>
      </div>
    </div>
  </section>
</template>
