<template>
  <header class="topbar">
    <h1 class="page-title">{{ title }}</h1>

    <div class="topbar-right">
      <!-- Global Search -->
      <div class="search-box">
        <input
          type="text"
          placeholder="search..."
          :value="modelValue"
          @input="$emit('update:modelValue', $event.target.value)"
        />
      </div>
    </div>
  </header>
</template>

<script setup>
defineProps({
  /** Page heading text */
  title: {
    type: String,
    default: 'Dashboard Overview',
  },
  /** Global search input value */
  modelValue: {
    type: String,
    default: '',
  }
})

defineEmits(['update:modelValue', 'notifications', 'settings'])
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-family: 'Inter', sans-serif;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: #1a2e28;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* Search */
.search-box {
  display: flex;
  align-items: center;
  background: #fff;
  border: 1px solid #dde5e3;
  border-radius: 8px;
  padding: 7px 14px;
  gap: 8px;
  min-width: 200px;
}

.search-box input {
  border: none;
  outline: none;
  font-size: 13px;
  color: #333;
  background: transparent;
  width: 100%;
}

/* Icon buttons */
.icon-btn {
  background: #fff;
  border: 1px solid #dde5e3;
  border-radius: 8px;
  padding: 7px 10px;
  cursor: pointer;
  font-size: 16px;
  position: relative;
  transition: background 0.15s;
}

.icon-btn:hover { background: #f0f4f3; }


</style>
