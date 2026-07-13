<template>
  <div class="stat-card">
    <div class="stat-top">
      <div class="stat-icon" :style="{ background: iconBg, color: iconColor }">
        <span v-html="icon"></span>
      </div>
      <span class="stat-badge" :style="{ color: badgeColor }">{{ badge }}</span>
    </div>
    <div class="stat-label">{{ label }}</div>
    <div class="stat-value">{{ value }}</div>
  </div>
</template>

<script setup>
defineProps({
  label:      { type: String, required: true },
  value:      { type: String, required: true },
  /** Emoji or HTML string for the icon */
  icon:       { type: String, default: '📊' },
  iconBg:     { type: String, default: '#e8f4f1' },
  iconColor:  { type: String, default: '#2d6b5e' },
  badge:      { type: String, default: '' },
  badgeColor: { type: String, default: '#2d6b5e' },
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  transition: box-shadow 0.2s, transform 0.2s;
  font-family: 'Inter', sans-serif;
}

.stat-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.10);
  transform: translateY(-2px);
}

.stat-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.stat-badge {
  font-size: 12px;
  font-weight: 600;
}

.stat-label {
  font-size: 12.5px;
  color: #8a9e9a;
  font-weight: 500;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1a2e28;
  letter-spacing: -0.5px;
}
</style>
