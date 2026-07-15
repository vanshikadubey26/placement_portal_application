<template>
  <div class="student-layout">
    <!-- Sidebar -->
    <Sidebar
      v-model="activeNav"
      :nav-items="navItems"
      logo-img="/Only_logo.png"
      title="LaunchPad"
      subtitle="Student Portal"
      @logout="handleLogout"
    />

    <!-- Main Content -->
    <main class="main-content">
      <!-- Top Bar -->
      <header class="topbar">
        <div class="topbar-title-group">
          <h1 class="topbar-title">My Profile</h1>
          <p class="topbar-subtitle">LaunchPad Student Dashboard</p>
        </div>
      </header>

      <!-- Toast Alerts -->
      <div v-if="toastMessage" class="toast-alert" :class="toastType">
        <i :class="toastType === 'error' ? 'bi bi-exclamation-circle-fill' : 'bi bi-check-circle-fill'"></i>
        <span>{{ toastMessage }}</span>
      </div>

      <!-- Profile Form -->
      <section class="card form-card">
        <div class="card-header mb-4" style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h2 class="card-title">Student Profile Details</h2>
            <p class="card-subtitle">Keep your academic achievements and contact credentials up to date.</p>
          </div>
          <button type="button" @click="goBack" class="btn-secondary" style="padding: 6px 12px; font-size: 12px;">
            <i class="bi bi-arrow-left"></i> Back to Profile
          </button>
        </div>

        <form @submit.prevent="saveProfile">
          <div class="form-grid mb-4">
            <!-- Full Name -->
            <div class="form-group">
              <label class="form-label">Full Name</label>
              <input type="text" class="form-control" v-model="profileData.name" required />
            </div>

            <!-- Email Address -->
            <div class="form-group">
              <label class="form-label">Email Address</label>
              <input type="email" class="form-control" v-model="profileData.email" required />
            </div>

            <!-- Roll Number -->
            <div class="form-group">
              <label class="form-label">Roll Number</label>
              <input type="text" class="form-control" v-model="profileData.roll_number" required />
            </div>

            <!-- Branch -->
            <div class="form-group">
              <label class="form-label">Branch</label>
              <input type="text" class="form-control" v-model="profileData.branch" required />
            </div>

            <!-- Year of Study -->
            <div class="form-group">
              <label class="form-label">Year of Study</label>
              <select class="form-control" v-model.number="profileData.year_of_study" required>
                <option :value="1">First Year</option>
                <option :value="2">Second Year</option>
                <option :value="3">Third Year</option>
                <option :value="4">Fourth Year</option>
                <option :value="5">Fifth Year</option>
              </select>
            </div>

            <!-- CGPA -->
            <div class="form-group">
              <label class="form-label">Current CGPA</label>
              <input type="number" class="form-control" v-model.number="profileData.cgpa" min="0" max="10" step="0.01" required />
            </div>

            <!-- Resume Link -->
            <div class="form-group" style="grid-column: span 2;">
              <label class="form-label">Resume Link / URL (PDF)</label>
              <input type="url" class="form-control" v-model="profileData.resume" placeholder="e.g. Google Drive link to your resume PDF" />
            </div>
          </div>

          <div class="d-flex justify-content-end">
            <button type="submit" class="btn-primary" :disabled="saving">
              <span v-if="saving">Saving Changes...</span>
              <span v-else>Save Changes</span>
            </button>
          </div>
        </form>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'

const router = useRouter()
const activeNav = ref('Profile')
const saving = ref(false)
const toastMessage = ref('')
const toastType = ref('success')

const navItems = [
  { label: 'Dashboard', icon: '<i class="bi bi-speedometer2"></i>' },
  { label: 'Drives',    icon: '<i class="bi bi-megaphone"></i>' },
  { label: 'Applications', icon: '<i class="bi bi-file-earmark-text"></i>' },
  { label: 'Profile',   icon: '<i class="bi bi-person-bounding-box"></i>' }
]

const profileData = reactive({
  name: '',
  email: '',
  roll_number: '',
  branch: '',
  year_of_study: 1,
  cgpa: 0.0,
  resume: ''
})

let isInitialized = false

watch(activeNav, (newVal) => {
  if (!isInitialized) return
  if (newVal === 'Dashboard') {
    router.push('/student/dashboard')
  } else if (newVal === 'Drives') {
    router.push('/student/drives')
  } else if (newVal === 'Applications') {
    router.push('/student/applications')
  } else if (newVal === 'Profile') {
    const userJson = localStorage.getItem('user')
    if (userJson) {
      const u = JSON.parse(userJson)
      router.push(`/student/profile/${u.id}`)
    } else {
      router.push('/student/dashboard')
    }
  }
})

function showToast(msg, type = 'success') {
  toastMessage.value = msg
  toastType.value = type
  setTimeout(() => { toastMessage.value = '' }, 3500)
}

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    router.push('/login')
    return
  }

  setTimeout(() => {
    isInitialized = true
  }, 150)

  try {
    const res = await fetch('http://localhost:5555/api/student/profile', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (res.ok) {
      const data = await res.json()
      profileData.name = data.name || ''
      profileData.email = data.email || ''
      profileData.roll_number = data.roll_number || ''
      profileData.branch = data.branch || ''
      profileData.year_of_study = data.year_of_study || 1
      profileData.cgpa = data.cgpa || 0.0
      profileData.resume = data.resume || ''
    } else {
      showToast('Failed to fetch profile information.', 'error')
    }
  } catch (err) {
    showToast('Network error while loading profile.', 'error')
  }
})

async function saveProfile() {
  const token = localStorage.getItem('access_token')
  if (!token) return

  saving.value = true
  try {
    const res = await fetch('http://localhost:5555/api/student/profile', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(profileData)
    })
    const data = await res.json()
    if (!res.ok) {
      showToast(data.message || 'Failed to update profile.', 'error')
      return
    }
    showToast('Profile updated successfully!')
    
    // Update local cache user name/email if updated
    const userJson = localStorage.getItem('user')
    if (userJson) {
      const u = JSON.parse(userJson)
      u.name = profileData.name
      u.email = profileData.email
      localStorage.setItem('user', JSON.stringify(u))
    }

    setTimeout(() => {
      const userJson = localStorage.getItem('user')
      if (userJson) {
        const u = JSON.parse(userJson)
        router.push(`/student/profile/${u.id}`)
      } else {
        router.push('/student/dashboard')
      }
    }, 1000)
  } catch (err) {
    showToast('Network error while saving changes.', 'error')
  } finally {
    saving.value = false
  }
}

function goBack() {
  const userJson = localStorage.getItem('user')
  if (userJson) {
    const u = JSON.parse(userJson)
    router.push(`/student/profile/${u.id}`)
  } else {
    router.push('/student/dashboard')
  }
}

function handleLogout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

.student-layout { display: flex; min-height: 100vh; background: #f4f9f8; }
.main-content { flex: 1; display: flex; flex-direction: column; overflow-y: auto; }

.topbar { padding: 20px 28px 16px; background: #fff; border-bottom: 1px solid #eff3f2; }
.topbar-title { font-size: 20px; font-weight: 700; color: #1a2e28; margin: 0; }
.topbar-subtitle { font-size: 12.5px; color: #8a9e9a; margin-top: 4px; }

.card { background: #fff; border-radius: 14px; padding: 24px 28px; box-shadow: 0 1px 4px rgba(0,0,0,.06); margin: 24px 28px; }
.card-title { font-size: 16.5px; font-weight: 700; color: #1a2e28; margin: 0; }
.card-subtitle { font-size: 12.5px; color: #8a9e9a; margin-top: 4px; }

.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-label { font-size: 12.5px; font-weight: 600; color: #5a7a75; }

.form-control {
  padding: 9px 12px;
  border: 1.5px solid #d4e6e1;
  border-radius: 8px;
  font-size: 13.5px;
  outline: none;
  background: #fafafa;
  color: #1a2e28;
  transition: all 0.2s;
}
.form-control:focus {
  border-color: #2d6b5e;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(45,107,94,0.15);
}

.btn-primary {
  background: #2d6b5e;
  color: white;
  border: none;
  border-radius: 7px;
  padding: 10px 20px;
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}
.btn-primary:hover { background: #235349; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }

.d-flex { display: flex; }
.justify-content-end { justify-content: flex-end; }
.mb-4 { margin-bottom: 20px; }

/* Toast */
.toast-alert { position: fixed; top: 24px; right: 24px; padding: 12px 20px; border-radius: 8px; font-size: 13px; font-weight: 500; color: #fff; z-index: 9999; box-shadow: 0 4px 16px rgba(0,0,0,0.15); display: flex; align-items: center; gap: 8px; }
.toast-alert.success { background: #2d6b5e; }
.toast-alert.error { background: #dc2626; }
</style>
