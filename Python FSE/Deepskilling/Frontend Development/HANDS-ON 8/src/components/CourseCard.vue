<script setup>
defineProps({
  id: Number,
  name: String,
  code: String,
  credits: Number,
  grade: String
});
</script>

<template>
  <article class="course-card">
    <h3><RouterLink :to="`/courses/${id}`">{{ name }}</RouterLink></h3>
    <p>{{ code }}</p>
    <span class="credits">{{ credits }} credits &middot; Grade: {{ grade }}</span>
  </article>
</template>
