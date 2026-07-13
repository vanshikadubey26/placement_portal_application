<template>
  <div class="portal-container">
    <div class="portal-card">
      <div class="icon-header">
        <i class="bi bi-mortarboard"></i>
      </div>
      <h1 class="title">Student Dashboard</h1>
      <p class="subtitle">Welcome to your LaunchPad student portal.</p>
      
      <div class="user-info" v-if="user">
        <div class="info-row">
          <span class="label">Name:</span>
          <span class="value">{{ user.name }}</span>
        </div>
        <div class="info-row">
          <span class="label">Username:</span>
          <span class="value">@{{ user.username }}</span>
        </div>
        <div class="info-row">
          <span class="label">Email:</span>
          <span class="value">{{ user.email }}</span>
        </div>
      </div>

      <button class="btn-logout" @click="handleLogout" :disabled="loading">
        <i class="bi bi-box-arrow-right"></i>
        <span>{{ loading ? 'Logging out...' : 'Logout' }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref(null)
const loading = ref(false)

onMounted(() => {
  const userJson = localStorage.getItem('user')
  if (userJson) {
    try {
      user.value = JSON.parse(userJson)
    } catch (e) {
      console.error(e)
    }
  }
})

async function handleLogout() {
  loading.value = true
  try {
    const token = localStorage.getItem('access_token')
    await fetch('http://localhost:5555/api/auth/logout', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
  } catch (err) {
    console.error('Logout error:', err)
  } finally {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    router.push('/login')
    loading.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.portal-container {
  font-family: 'Inter', sans-serif;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle at 10% 20%, #1a2e28 0%, #111a17 100%);
  padding: 20px;
  color: #e5ecea;
}

.portal-card {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 40px;
  max-width: 440px;
  width: 100%;
  text-align: center;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
}

.icon-header {
  font-size: 48px;
  color: #3b9c80;
  margin-bottom: 20px;
}

.title {
  font-size: 26px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #ffffff;
}

.subtitle {
  font-size: 14px;
  color: #8da39e;
  margin-bottom: 30px;
}

.user-info {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 30px;
  text-align: left;
}

.info-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  font-size: 13.5px;
}

.info-row:last-child {
  margin-bottom: 0;
}

.label {
  color: #8da39e;
  font-weight: 500;
}

.value {
  color: #ffffff;
  font-weight: 600;
}

.btn-logout {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: #b94a3b;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  font-size: 14.5px;
  font-weight: 600;
  cursor: pointer;
  width: 100%;
  transition: background 0.18s, transform 0.1s;
}

.btn-logout:hover {
  background: #c95a4b;
}

.btn-logout:active {
  transform: scale(0.98);
}

.btn-logout:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>