<template>
  <aside class="sidebar">
    <!-- Logo / Header -->
    <div class="sidebar-header">
      <img v-if="logoImg" :src="logoImg" class="sidebar-logo-img" alt="logo" />
      <span v-else class="sidebar-logo-icon">{{ logoIcon }}</span>
      <div>
        <div class="sidebar-title">{{ title }}</div>
        <div class="sidebar-subtitle">{{ subtitle }}</div>
      </div>
    </div>

    <!-- Navigation Links -->
    <nav class="sidebar-nav">
      <a
        v-for="item in navItems"
        :key="item.label"
        class="nav-item"
        :class="{ active: modelValue === item.label }"
        href="#"
        @click.prevent="$emit('update:modelValue', item.label)"
      >
        <span v-if="item.icon" class="nav-icon" v-html="item.icon"></span>
        <span>{{ item.label }}</span>
      </a>
    </nav>

    <!-- Footer Actions -->
    <div class="sidebar-footer">
      
      <a class="nav-item help" href="#" @click.prevent="$emit('logout')">
        <span class="nav-icon">↪</span>
        <span>Logout</span>
      </a>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  /** Currently active nav label — use v-model on parent */
  modelValue: {
    type: String,
    required: true,
  },
  /** Array of nav items: [{ label: String, icon: String }] */
  navItems: {
    type: Array,
    required: true,
  },
  /** Optional image source path for the logo (e.g. /Only_logo.png) */
  logoImg: {
    type: String,
    default: null,
  },
  /** Fallback logo icon element/emoji when no image is supplied */
  logoIcon: {
    type: String,
    default: '🎓',
  },
  /** Sidebar primary title */
  title: {
    type: String,
    default: 'Placement Portal',
  },
  /** Sidebar subtitle/console description */
  subtitle: {
    type: String,
    default: 'Portal Console',
  },
})

defineEmits(['update:modelValue', 'logout'])
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.sidebar {
  width: 210px;
  min-width: 210px;
  flex-shrink: 0;
  height: 100vh;
  position: sticky;
  top: 0;
  background: #253a35;
  display: flex;
  flex-direction: column;
  color: #d4e4df;
  overflow-y: auto;
  font-family: 'Inter', sans-serif;
}

/* ── Header ───────────────────── */
.sidebar-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 24px 20px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
}

.sidebar-logo-img {
  width: auto;
  height: 50px;
  object-fit: contain;
}

.sidebar-logo-icon { font-size: 30px; }

.sidebar-title {
  font-size: 15px;
  font-weight: 700;
  color: #ffffff;
  line-height: 1.2;
}

.sidebar-subtitle {
  font-size: 11px;
  color: #8ab5a8;
  font-weight: 400;
}

/* ── Nav ──────────────────────── */
.sidebar-nav {
  padding: 16px 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 13.5px;
  font-weight: 500;
  color: #a8c8bf;
  text-decoration: none;
  cursor: pointer;
  transition: background 0.18s, color 0.18s;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #ffffff;
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.13);
  color: #ffffff;
  font-weight: 600;
}

.nav-icon {
  font-size: 15px;
  width: 20px;
  text-align: center;
}

/* ── Footer ───────────────────── */
.sidebar-footer {
  padding: 16px 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.07);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item.help {
  font-size: 13px;
  color: #8ab5a8;
}
</style>
