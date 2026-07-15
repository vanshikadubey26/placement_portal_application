<template>
  <div>
    <!-- Mobile Burger Button -->
    <button 
      class="burger-menu-btn" 
      @click="toggleSidebar"
      :aria-label="isOpen ? 'Close Menu' : 'Open Menu'"
    >
      <i :class="['bi', isOpen ? 'bi-x-lg' : 'bi-list']"></i>
    </button>

    <!-- Overlay backdrop when sidebar is open on mobile -->
    <div 
      v-if="isOpen" 
      class="sidebar-overlay" 
      @click="closeSidebar"
    ></div>

    <aside class="sidebar" :class="{ 'mobile-open': isOpen }">
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
          @click.prevent="selectItem(item.label)"
        >
          <span v-if="item.icon" class="nav-icon" v-html="item.icon"></span>
          <span>{{ item.label }}</span>
        </a>
      </nav>

      <!-- Footer Actions -->
      <div class="sidebar-footer">
        <a class="nav-item help" href="#" @click.prevent="handleLogout">
          <span class="nav-icon">↪</span>
          <span>Logout</span>
        </a>
      </div>
    </aside>
  </div>
</template>

<script setup>
import { ref } from 'vue'

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

const emit = defineEmits(['update:modelValue', 'logout'])

const isOpen = ref(false)

const toggleSidebar = () => {
  isOpen.value = !isOpen.value
}

const closeSidebar = () => {
  isOpen.value = false
}

const selectItem = (label) => {
  emit('update:modelValue', label)
  closeSidebar()
}

const handleLogout = () => {
  emit('logout')
  closeSidebar()
}
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

/* Mobile burger button styling */
.burger-menu-btn {
  display: none;
  position: fixed;
  left: 16px;
  top: 16px;
  z-index: 1100;
  background: #253a35;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  width: 40px;
  height: 40px;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  font-size: 20px;
  transition: background 0.2s;
}

.burger-menu-btn:hover {
  background: #1b2d29;
}

/* Mobile overlay backdrop */
.sidebar-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.4);
  z-index: 999;
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

@media (max-width: 768px) {
  .burger-menu-btn {
    display: flex;
  }
  
  .sidebar-overlay {
    display: block;
  }

  .sidebar {
    position: fixed;
    left: -220px;
    z-index: 1000;
    transition: left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 4px 0 15px rgba(0, 0, 0, 0.1);
  }

  .sidebar.mobile-open {
    left: 0;
  }
}
</style>
