<script setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { courses } from '../data/courses';
import { useEnrollmentStore } from '../stores/enrollment';

const route = useRoute();
const router = useRouter();
const store = useEnrollmentStore();

const course = computed(() => courses.find((c) => c.id === Number(route.params.id)));

function handleEnroll() {
  store.enroll(course.value);
  router.push('/profile');
}
</script>

<template>
  <section v-if="course" class="course-card" style="max-width:480px;">
    <h2>{{ course.name }}</h2>
    <p>{{ course.code }}</p>
    <span class="credits">{{ course.credits }} credits &middot; Grade: {{ course.grade }}</span>
    <button type="button" @click="handleEnroll">Enroll</button>
  </section>
  <p v-else>Course not found.</p>
</template>
