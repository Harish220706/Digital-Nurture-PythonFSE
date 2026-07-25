<script setup>
import { useEnrollmentStore } from '../stores/enrollment';
import { storeToRefs } from 'pinia';

const store = useEnrollmentStore();
const { enrolledCourses } = storeToRefs(store);
</script>

<template>
  <header>
    <div class="site-name">Student Portal</div>
    <nav aria-label="Main navigation">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/courses">Courses</RouterLink>
      <RouterLink to="/profile">Profile ({{ enrolledCourses.length }})</RouterLink>
    </nav>
  </header>
</template>
