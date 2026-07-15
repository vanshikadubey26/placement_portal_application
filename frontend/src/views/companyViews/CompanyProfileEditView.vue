<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <Sidebar
      v-model="activeNav"
      :nav-items="navItems"
      logo-img="/Only_logo.png"
      title="LaunchPad"
      subtitle="Recruiter Console"
      @logout="handleLogout"
    />

    <!-- Main Content -->
    <main class="main-content">
      <!-- Top Bar -->
      <header class="topbar">
        <div class="topbar-title-group">
          <h1 class="topbar-title">Company Profile</h1>
          <p class="topbar-subtitle">LaunchPad Corporate Dashboard</p>
        </div>
      </header>

      <!-- Toast Alerts -->
      <div v-if="toastMessage" class="toast-alert" :class="toastType">
        <i :class="toastType === 'success' ? 'bi bi-check-circle-fill' : 'bi bi-exclamation-circle-fill'"></i>
        <span>{{ toastMessage }}</span>
      </div>

      <!-- Profile Form -->
      <section class="card form-card">
        <div class="card-header mb-4" style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <h2 class="card-title">Company Profile Details</h2>
            <p class="card-subtitle">Keep your company credentials and public interface up to date.</p>
          </div>
          <button type="button" @click="goBack" class="btn-secondary" style="padding: 6px 12px; font-size: 12px; border: 1px solid #ced4da; border-radius: 6px; background: #fff; font-weight: 600; color: #495057; cursor: pointer;">
            <i class="bi bi-arrow-left"></i> Back to Profile
          </button>
        </div>

        <form @submit.prevent="saveProfile">
          <div class="form-grid mb-4">
            <!-- Company Name -->
            <div class="form-group">
              <label class="form-label">Company Name</label>
              <input type="text" class="form-control" :value="companyProfile.name" disabled />
            </div>

            <!-- Industry Sector -->
            <div class="form-group">
              <label class="form-label">Industry Sector</label>
              <input type="text" class="form-control" :class="{ 'is-invalid': errors.industry }" v-model="companyProfile.industry" placeholder="e.g. Technology, Finance" required />
              <span v-if="errors.industry" class="error-feedback">{{ errors.industry }}</span>
            </div>

            <!-- Company Scale -->
            <div class="form-group">
              <label class="form-label">Company Scale / Size</label>
              <select class="form-control" :class="{ 'is-invalid': errors.scale }" v-model="companyProfile.scale" required>
                <option>1-10 employees</option>
                <option>11-50 employees</option>
                <option>51-200 employees</option>
                <option>201-500 employees</option>
                <option>500+ employees</option>
              </select>
              <span v-if="errors.scale" class="error-feedback">{{ errors.scale }}</span>
            </div>

            <!-- Website URL -->
            <div class="form-group">
              <label class="form-label">Website URL</label>
              <input type="text" class="form-control" :class="{ 'is-invalid': errors.website }" v-model="companyProfile.website" placeholder="https://example.com" />
              <span v-if="errors.website" class="error-feedback">{{ errors.website }}</span>
            </div>

            <!-- Head Office Location -->
            <div class="form-group">
              <label class="form-label">Head Office Location</label>
              <input type="text" class="form-control" :class="{ 'is-invalid': errors.headOffice }" v-model="companyProfile.headOffice" placeholder="e.g. Bangalore, India" />
              <span v-if="errors.headOffice" class="error-feedback">{{ errors.headOffice }}</span>
            </div>

            <!-- Logo Image URL / Path -->
            <div class="form-group">
              <label class="form-label">Logo URL or Path</label>
              <input type="text" class="form-control" :class="{ 'is-invalid': errors.logo }" v-model="companyProfile.logo" placeholder="e.g. /logos/nexustech.png or http://..." />
              <span v-if="errors.logo" class="error-feedback">{{ errors.logo }}</span>
            </div>

            <!-- POC Name -->
            <div class="form-group">
              <label class="form-label">Point of Contact (POC) Name</label>
              <input type="text" class="form-control" :class="{ 'is-invalid': errors.pocName }" v-model="companyProfile.pocName" required />
              <span v-if="errors.pocName" class="error-feedback">{{ errors.pocName }}</span>
            </div>

            <!-- POC Email Address -->
            <div class="form-group">
              <label class="form-label">Point of Contact (POC) Email</label>
              <input type="email" class="form-control" :class="{ 'is-invalid': errors.pocEmail }" v-model="companyProfile.pocEmail" required />
              <span v-if="errors.pocEmail" class="error-feedback">{{ errors.pocEmail }}</span>
            </div>
          </div>

          <!-- Corporate Description -->
          <div class="form-group mb-4">
            <label class="form-label">Corporate Description</label>
            <textarea class="form-control text-area" :class="{ 'is-invalid': errors.description }" v-model="companyProfile.description" rows="4" placeholder="Briefly describe your company..."></textarea>
            <span v-if="errors.description" class="error-feedback">{{ errors.description }}</span>
          </div>

          <div class="d-flex justify-content-end">
            <button type="submit" class="btn-primary" :disabled="savingProfile">
              <span v-if="savingProfile" class="spinner-border spinner-border-sm me-2"></span>
              Save Changes
            </button>
          </div>
        </form>
      </section>

    </main>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'

const router = useRouter()
const activeNav = ref('Profile')

// Sidebar Nav Items
const navItems = [
  { label: 'Dashboard',    icon: '<i class="bi bi-speedometer2"></i>' },
  { label: 'Drives',       icon: '<i class="bi bi-megaphone"></i>' },
  { label: 'Applications', icon: '<i class="bi bi-file-earmark-text"></i>' },
  { label: 'Shortlisted',  icon: '<i class="bi bi-patch-check"></i>' },
  { label: 'Interviews',   icon: '<i class="bi bi-calendar-event"></i>' },
  { label: 'Report',       icon: '<i class="bi bi-file-earmark-bar-graph"></i>' },
  { label: 'Profile',      icon: '<i class="bi bi-building"></i>' }
]

let isInitialized = false

// Navigation Watch
watch(activeNav, (newVal) => {
  if (!isInitialized) return
  if (newVal === 'Dashboard') {
    router.push('/company/dashboard')
  } else if (newVal === 'Profile') {
    const userJson = localStorage.getItem('user')
    if (userJson) {
      const u = JSON.parse(userJson)
      router.push(`/company/profile/${u.id}`)
    } else {
      router.push('/company/dashboard')
    }
  } else if (newVal === 'Drives') {
    router.push('/company/drives')
  } else if (newVal === 'Applications') {
    router.push('/company/applications')
  } else if (newVal === 'Shortlisted') {
    router.push('/company/shortlisted')
  } else if (newVal === 'Interviews') {
    router.push('/company/interviews')
  } else if (newVal === 'Report') {
    router.push('/company/reports')
  }
})

// Recruiter Profile Info
const companyProfile = ref({
  name: 'NexusTech Solutions',
  industry: 'Cloud Infrastructure',
  website: 'https://nexustech.io',
  headOffice: 'Bangalore, India',
  description: 'NexusTech provides scalable multi-cloud architectures and hybrid hosting virtualization paradigms.',
  pocName: 'Divya Vardhan',
  pocEmail: 'hr@nexustech.io',
  scale: '51-200 employees',
  logo: '/logos/nexustech.png'
})

const errors = ref({
  industry: '',
  website: '',
  headOffice: '',
  pocName: '',
  pocEmail: '',
  scale: '',
  logo: '',
  description: ''
})

const savingProfile = ref(false)
const toastMessage = ref('')
const toastType = ref('success')

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    showToast('Unauthorized session. Redirecting to login...', 'error')
    setTimeout(() => router.push('/login'), 1500)
    return
  }

  // Set isInitialized on next tick to avoid redirection loop during setup
  setTimeout(() => {
    isInitialized = true
  }, 150)

  try {
    const res = await fetch('http://localhost:5555/api/company/profile', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    if (!res.ok) {
      const data = await res.json()
      showToast(data.message || 'Failed to load company profile.', 'error')
      return
    }
    const data = await res.json()
    companyProfile.value = {
      name: data.name || '',
      description: data.description || '',
      industry: data.industry || '',
      scale: data.scale || '51-200 employees',
      headOffice: data.headOffice || '',
      website: data.website || '',
      logo: data.logo || '',
      pocName: data.pocName || '',
      pocEmail: data.pocEmail || ''
    }
  } catch (err) {
    showToast('Cannot connect to server to fetch profile.', 'error')
  }
})

function showToast(msg, type = 'success') {
  toastMessage.value = msg
  toastType.value = type
  setTimeout(() => {
    toastMessage.value = ''
  }, 3500)
}

function validateForm() {
  let isValid = true
  
  errors.value = {
    industry: '',
    website: '',
    headOffice: '',
    pocName: '',
    pocEmail: '',
    scale: '',
    logo: '',
    description: ''
  }

  if (!companyProfile.value.industry) {
    errors.value.industry = 'Industry Sector is required.'
    isValid = false
  }
  if (!companyProfile.value.pocName) {
    errors.value.pocName = 'Point of Contact Name is required.'
    isValid = false
  }
  if (!companyProfile.value.pocEmail) {
    errors.value.pocEmail = 'POC Email Address is required.'
    isValid = false
  }

  if (companyProfile.value.pocEmail) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(companyProfile.value.pocEmail)) {
      errors.value.pocEmail = 'Please enter a valid email address.'
      isValid = false
    }
  }

  if (companyProfile.value.website) {
    try {
      new URL(companyProfile.value.website)
    } catch (_) {
      errors.value.website = 'Please enter a valid URL (starting with http:// or https://).'
      isValid = false
    }
  }

  if (companyProfile.value.logo) {
    const isUrl = companyProfile.value.logo.startsWith('http://') || 
                  companyProfile.value.logo.startsWith('https://') || 
                  companyProfile.value.logo.startsWith('/')
    if (!isUrl) {
      errors.value.logo = 'Logo must be a valid URL or path (e.g. /logo.png or http://...).'
      isValid = false
    }
  }

  const stringFields = ['industry', 'scale', 'headOffice', 'website', 'logo', 'pocName', 'pocEmail']
  stringFields.forEach(field => {
    if (companyProfile.value[field] && companyProfile.value[field].length > 150) {
      errors.value[field] = 'Value must not exceed 150 characters.'
      isValid = false
    }
  })

  return isValid
}

async function saveProfile() {
  if (!validateForm()) {
    showToast('Please correct validation errors before saving.', 'error')
    return
  }

  const token = localStorage.getItem('access_token')
  if (!token) {
    showToast('Unauthorized session. Please login again.', 'error')
    return
  }

  savingProfile.value = true
  try {
    const res = await fetch('http://localhost:5555/api/company/profile', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        description: companyProfile.value.description,
        industry: companyProfile.value.industry,
        scale: companyProfile.value.scale,
        headOffice: companyProfile.value.headOffice,
        website: companyProfile.value.website,
        logo: companyProfile.value.logo,
        pocName: companyProfile.value.pocName,
        pocEmail: companyProfile.value.pocEmail
      })
    })

    const data = await res.json()
    if (!res.ok) {
      showToast(data.message || 'Failed to update profile.', 'error')
      return
    }

    showToast('Company profile updated successfully!')
    
    setTimeout(() => {
      const userJson = localStorage.getItem('user')
      if (userJson) {
        const u = JSON.parse(userJson)
        router.push(`/company/profile/${u.id}`)
      } else {
        router.push('/company/dashboard')
      }
    }, 1000)
  } catch (err) {
    showToast('Cannot connect to server to save changes.', 'error')
  } finally {
    savingProfile.value = false
  }
}

function goBack() {
  const userJson = localStorage.getItem('user')
  if (userJson) {
    const u = JSON.parse(userJson)
    router.push(`/company/profile/${u.id}`)
  } else {
    router.push('/company/dashboard')
  }
}

async function handleLogout() {
  try {
    const token = localStorage.getItem('access_token')
    await fetch('http://localhost:5555/api/auth/logout', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` },
    })
  } catch (err) {
    console.error('Logout error:', err)
  } finally {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    router.push('/login')
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
  font-family: 'Inter', sans-serif;
  box-sizing: border-box;
}

.admin-layout {
  display: flex;
  height: 100vh;
  background: #f5f5f0;
  overflow: hidden;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 28px 28px 40px;
  display: flex;
  flex-direction: column;
  gap: 22px;
}

/* ── Top Bar ───────────────────── */
.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 12px;
  border-bottom: 1px solid #eff3f2;
}

.topbar-title {
  font-size: 19px;
  font-weight: 700;
  color: #1a2e28;
  margin: 0;
}

.topbar-subtitle {
  font-size: 12.5px;
  color: #8a9e9a;
  margin: 2px 0 0;
}

.topbar-profile {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar-fallback {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #2d6b5e;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 15px;
}

.profile-info {
  display: flex;
  flex-direction: column;
}

.profile-name {
  font-size: 13.5px;
  font-weight: 600;
  color: #1a2e28;
}

.profile-subtext {
  font-size: 11px;
  color: #8a9e9a;
}

/* ── Toast Alerts ──────────────── */
.toast-alert {
  position: fixed;
  top: 24px;
  right: 24px;
  z-index: 1000;
  background: #e6f4ea;
  color: #137333;
  border: 1px solid #c3e6cb;
  border-radius: 8px;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  animation: slide-in 0.25s ease-out;
  font-size: 13.5px;
}

@keyframes slide-in {
  from { transform: translateX(120%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

/* ── Cards & Forms ─────────────── */
.card {
  background: #fff;
  border-radius: 14px;
  padding: 22px;
  box-shadow: 0 1px 4px rgba(0,0,0,.06);
}

.card-header {
  margin-bottom: 20px;
}

.card-title {
  font-size: 15px;
  font-weight: 700;
  color: #1a2e28;
  margin: 0;
}

.card-subtitle {
  font-size: 12.5px;
  color: #8a9e9a;
  margin-top: 4px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 12.5px;
  font-weight: 600;
  color: #5a7a75;
}

.form-control {
  padding: 9px 12px;
  border: 1.5px solid #e2e2de;
  border-radius: 8px;
  font-size: 13.5px;
  outline: none;
  background: #fafafa;
  color: #1a2e28;
  transition: all 0.2s;
}
.form-control:focus {
  border-color: #81B29A;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(129,178,154,0.15);
}

.text-area {
  resize: vertical;
  font-family: inherit;
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
  display: inline-flex;
  align-items: center;
  transition: background 0.15s;
}
.btn-primary:hover {
  background: #235349;
}
.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.d-flex { display: flex; }
.justify-content-end { justify-content: flex-end; }
.mb-4 { margin-bottom: 20px; }
.me-2 { margin-right: 8px; }

/* ── Validation Error Styles ───── */
.form-control.is-invalid {
  border-color: #e07a5f;
  background-color: #fff9f8;
}
.form-control.is-invalid:focus {
  box-shadow: 0 0 0 3px rgba(224, 122, 95, 0.15);
}

.error-feedback {
  font-size: 11.5px;
  color: #e07a5f;
  font-weight: 500;
  margin-top: 2px;
}
</style>
