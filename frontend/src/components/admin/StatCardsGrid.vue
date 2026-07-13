<template>
  <section class="stat-cards">
    <StatCard
      v-for="stat in stats"
      :key="stat.label"
      v-bind="stat"
    />
  </section>
</template>

<script setup>
import StatCard from './StatCard.vue'

defineProps({
  stats: {
    type: Array,
    required: true,
  },
})
</script>

<style scoped>
.stat-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
</style>
