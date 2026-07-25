<script setup>
import { storeToRefs } from 'pinia';
import { useEnrollmentStore } from '../stores/enrollment';

const store = useEnrollmentStore();
const { enrolledCourses, totalCredits } = storeToRefs(store);
</script>

<template>
  <section>
    <h2>My Profile</h2>
    <p>Enrolled: {{ enrolledCourses.length }} &middot; Total credits: {{ totalCredits }}</p>
    <div class="course-grid">
      <article class="course-card" v-for="course in enrolledCourses" :key="course.id">
        <h3>{{ course.name }}</h3>
        <span class="credits">{{ course.credits }} credits</span>
        <button type="button" @click="store.unenroll(course.id)">Remove</button>
      </article>
    </div>
    <p v-if="enrolledCourses.length === 0">You have not enrolled in any courses yet.</p>
  </section>
</template>
