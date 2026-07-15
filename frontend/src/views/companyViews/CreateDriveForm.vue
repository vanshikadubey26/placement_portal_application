<template>
  <div class="company-layout">
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
          <h1 class="topbar-title">Create Placement Drive</h1>
          <p class="topbar-subtitle">LaunchPad Recruiter Console</p>
        </div>
      </header>

      <!-- Toast Alerts -->
      <div v-if="toastMessage" class="toast-alert" :class="toastType">
        <i :class="toastType === 'success' ? 'bi bi-check-circle-fill' : 'bi bi-exclamation-circle-fill'"></i>
        <span>{{ toastMessage }}</span>
      </div>

      <!-- Create Form Card -->
      <section class="card form-card">
        <div class="card-header mb-4 d-flex justify-content-between align-items-center">
          <div>
            <h2 class="card-title">Placement Drive Details</h2>
            <p class="card-subtitle">Fill in the fields below to publish a new placement drive. Requires admin approval before going live.</p>
          </div>
          <button class="btn-secondary" @click="goBack">
            <i class="bi bi-arrow-left me-2"></i> Cancel & Go Back
          </button>
        </div>

        <form @submit.prevent="submitDrive">
          <div class="form-grid mb-4">
            <!-- Job Title -->
            <div class="form-group">
              <label class="form-label">Job Title *</label>
              <input type="text" class="form-control" :class="{ 'is-invalid': errors.title }" v-model="newDrive.title" placeholder="e.g. Graduate Engineer Trainee" required />
              <span v-if="errors.title" class="error-feedback">{{ errors.title }}</span>
            </div>

            <!-- Target Branches -->
            <div class="form-group">
              <label class="form-label">Target Branches</label>
              <input type="text" class="form-control" :class="{ 'is-invalid': errors.branches }" v-model="newDrive.branches" placeholder="e.g. CSE, IT, ECE" />
              <span v-if="errors.branches" class="error-feedback">{{ errors.branches }}</span>
            </div>

            <!-- Eligible Batches -->
            <div class="form-group">
              <label class="form-label">Eligible Batches</label>
              <input type="text" class="form-control" :class="{ 'is-invalid': errors.batch }" v-model="newDrive.batch" placeholder="e.g. 2026, 2027" />
              <span v-if="errors.batch" class="error-feedback">{{ errors.batch }}</span>
            </div>

            <!-- Pay Scale / Package -->
            <div class="form-group">
              <label class="form-label">Pay Scale / CTC Package</label>
              <input type="text" class="form-control" :class="{ 'is-invalid': errors.payScale }" v-model="newDrive.payScale" placeholder="e.g. 12 LPA or 50,000 / month" />
              <span v-if="errors.payScale" class="error-feedback">{{ errors.payScale }}</span>
            </div>

            <!-- Positions -->
            <div class="form-group">
              <label class="form-label">Open Positions</label>
              <input type="number" class="form-control" :class="{ 'is-invalid': errors.positions }" v-model="newDrive.positions" min="1" />
              <span v-if="errors.positions" class="error-feedback">{{ errors.positions }}</span>
            </div>

            <!-- Work Mode -->
            <div class="form-group">
              <label class="form-label">Work Mode</label>
              <select class="form-control" v-model="newDrive.workMode">
                <option>On-site</option>
                <option>Remote</option>
                <option>Hybrid</option>
              </select>
            </div>

            <!-- Location / Room -->
            <div class="form-group">
              <label class="form-label">Location / Venue</label>
              <input type="text" class="form-control" :class="{ 'is-invalid': errors.location }" v-model="newDrive.location" placeholder="e.g. Bangalore Office or Online" />
              <span v-if="errors.location" class="error-feedback">{{ errors.location }}</span>
            </div>

            <!-- Application Deadline -->
            <div class="form-group">
              <label class="form-label">Application Deadline</label>
              <input type="datetime-local" class="form-control" :class="{ 'is-invalid': errors.deadline }" v-model="newDrive.deadline" />
              <span v-if="errors.deadline" class="error-feedback">{{ errors.deadline }}</span>
            </div>

            <!-- Eligibility Criteria -->
            <div class="form-group">
              <label class="form-label">Eligibility Criteria (e.g. CGPA >= 8.0)</label>
              <input type="text" class="form-control" :class="{ 'is-invalid': errors.eligibility }" v-model="newDrive.eligibility" placeholder="e.g. CGPA >= 8.0, No active backlogs" />
              <span v-if="errors.eligibility" class="error-feedback">{{ errors.eligibility }}</span>
            </div>

            <!-- Required Skills -->
            <div class="form-group">
              <label class="form-label">Required Skills</label>
              <input type="text" class="form-control" :class="{ 'is-invalid': errors.skillsRequired }" v-model="newDrive.skillsRequired" placeholder="e.g. Python, Docker, React" />
              <span v-if="errors.skillsRequired" class="error-feedback">{{ errors.skillsRequired }}</span>
            </div>

            <!-- Selection/Interview Rounds -->
            <div class="form-group">
              <label class="form-label">Selection / Interview Rounds</label>
              <input type="text" class="form-control" :class="{ 'is-invalid': errors.interviewRounds }" v-model="newDrive.interviewRounds" placeholder="e.g. MCQ Test -> Technical -> HR Interview" />
              <span v-if="errors.interviewRounds" class="error-feedback">{{ errors.interviewRounds }}</span>
            </div>
          </div>

          <!-- Job Description -->
          <div class="form-group mb-4">
            <label class="form-label">Job Description</label>
            <textarea class="form-control text-area" v-model="newDrive.description" rows="5" placeholder="Provide details about job responsibilities, project scope, qualifications..."></textarea>
          </div>

          <div class="d-flex justify-content-end gap-3">
            <button type="button" class="btn-secondary" @click="goBack">Cancel</button>
            <button type="submit" class="btn-primary" :disabled="submitting">
              <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
              Create & Publish Drive
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
const activeNav = ref('Drives')

// Sidebar Nav Items
const navItems = [
  { label: 'Dashboard',    icon: '<i class="bi bi-speedometer2"></i>' },
  { label: 'Drives',       icon: '<i class="bi bi-megaphone"></i>' },
  { label: 'Applications', icon: '<i class="bi bi-file-earmark-text"></i>' },
  { label: 'Shortlisted',  icon: '<i class="bi bi-patch-check"></i>' },
  { label: 'Interviews',   icon: '<i class="bi bi-calendar-event"></i>' },
  { label: 'Profile',      icon: '<i class="bi bi-building"></i>' }
]

// Navigation Watch
watch(activeNav, (newVal) => {
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
  }
})

const newDrive = ref({
  title: '',
  branches: '',
  batch: '',
  payScale: '',
  positions: 1,
  workMode: 'On-site',
  location: '',
  deadline: '',
  eligibility: '',
  skillsRequired: '',
  interviewRounds: '',
  description: ''
})

const errors = ref({
  title: '',
  branches: '',
  batch: '',
  payScale: '',
  positions: '',
  location: '',
  deadline: '',
  eligibility: '',
  skillsRequired: '',
  interviewRounds: ''
})

const submitting = ref(false)
const toastMessage = ref('')
const toastType = ref('success')

onMounted(() => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    showToast('Unauthorized session. Redirecting to login...', 'error')
    setTimeout(() => router.push('/login'), 1500)
  }
})

function showToast(msg, type = 'success') {
  toastMessage.value = msg
  toastType.value = type
  setTimeout(() => {
    toastMessage.value = ''
  }, 3500)
}

function goBack() {
  router.push('/company/drives')
}

function validateForm() {
  let isValid = true
  errors.value = {
    title: '',
    branches: '',
    batch: '',
    payScale: '',
    positions: '',
    location: '',
    deadline: '',
    eligibility: '',
    skillsRequired: '',
    interviewRounds: ''
  }

  if (!newDrive.value.title) {
    errors.value.title = 'Job Title is required.'
    isValid = false
  }

  // Validate deadline is in the future
  if (newDrive.value.deadline) {
    const deadlineDate = new Date(newDrive.value.deadline)
    if (deadlineDate <= new Date()) {
      errors.value.deadline = 'Application deadline must be a future date/time.'
      isValid = false
    }
  }

  // Length constraints corresponding to DB fields String(150), String(300)
  const string150Fields = ['title', 'branches', 'batch', 'payScale', 'location', 'eligibility', 'interviewRounds']
  string150Fields.forEach(field => {
    if (newDrive.value[field] && newDrive.value[field].length > 150) {
      errors.value[field] = 'Value cannot exceed 150 characters.'
      isValid = false
    }
  })

  if (newDrive.value.skillsRequired && newDrive.value.skillsRequired.length > 300) {
    errors.value.skillsRequired = 'Skills list cannot exceed 300 characters.'
    isValid = false
  }

  return isValid
}

async function submitDrive() {
  if (!validateForm()) {
    showToast('Please correct validation errors before submitting.', 'error')
    return
  }

  const token = localStorage.getItem('access_token')
  if (!token) {
    showToast('Session expired. Please login again.', 'error')
    return
  }

  submitting.value = true
  try {
    const res = await fetch('http://localhost:5555/api/company/drive/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(newDrive.value)
    })

    const data = await res.json()
    if (!res.ok) {
      showToast(data.message || 'Failed to create placement drive.', 'error')
      return
    }

    showToast('Placement drive created successfully!')
    setTimeout(() => {
      router.push('/company/drives')
    }, 1500)
  } catch (err) {
    showToast('Cannot connect to server to publish drive.', 'error')
  } finally {
    submitting.value = false
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

.company-layout {
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
.toast-alert.error {
  background: #fde8e8;
  color: #c5221f;
  border-color: #f8b4b4;
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
  border-bottom: 1px solid #eff3f2;
  padding-bottom: 16px;
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
  margin-top: 20px;
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

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
  border-radius: 7px;
  padding: 10px 20px;
  font-size: 13.5px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: all 0.15s;
}
.btn-secondary:hover {
  background: #e5e7eb;
}

.d-flex { display: flex; }
.justify-content-between { justify-content: space-between; }
.justify-content-end { justify-content: flex-end; }
.align-items-center { align-items: center; }
.gap-3 { gap: 12px; }
.mb-4 { margin-bottom: 20px; }
.me-2 { margin-right: 8px; }
</style>
