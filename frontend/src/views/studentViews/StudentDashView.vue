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
      <header class="topbar">
        <div class="topbar-title-group">
          <h1 class="topbar-title">Welcome back, {{ userName }}</h1>
          <p class="topbar-subtitle">Manage your profile, browse drives, and track your applications</p>
        </div>
      </header>

      <!-- Toast Alert -->
      <div v-if="toastMessage" :class="['toast-alert', toastType === 'error' ? 'error' : 'success']">
        <i :class="toastType === 'error' ? 'bi bi-exclamation-circle' : 'bi bi-check-circle'"></i>
        {{ toastMessage }}
      </div>

      <!-- If student has no profile setup, show setup form card -->
      <section v-if="!hasProfile" class="card setup-card animate-fade-in">
        <div class="card-header border-none">
          <div class="header-icon-box">
            <i class="bi bi-person-fill-gear"></i>
          </div>
          <div>
            <h2 class="card-title text-lg font-bold">Complete Your Placement Profile</h2>
            <p class="card-subtitle">Provide your academic and personal details to start applying for jobs.</p>
          </div>
        </div>
        <div class="card-body">
          <form @submit.prevent="saveProfile" class="setup-form">
            <div class="form-grid">
              <div class="form-group">
                <label>Roll Number <span class="required">*</span></label>
                <input type="text" v-model="profileForm.roll_number" placeholder="e.g. Roll No/Branch/Year" class="form-input" required />
              </div>
              <div class="form-group">
                <label>Branch <span class="required">*</span></label>
                <input type="text" v-model="profileForm.branch" placeholder="e.g. Computer Science and Engineering" class="form-input" required />
              </div>
              <div class="form-group">
                <label>Year of Study <span class="required">*</span></label>
                <select v-model="profileForm.year_of_study" class="form-input" required>
                  <option value="" disabled>Select Year</option>
                  <option :value="1">1st Year</option>
                  <option :value="2">2nd Year</option>
                  <option :value="3">3rd Year</option>
                  <option :value="4">4th Year</option>
                </select>
              </div>
              <div class="form-group">
                <label>Current CGPA <span class="required">*</span></label>
                <input type="number" step="0.01" min="0" max="10" v-model="profileForm.cgpa" placeholder="e.g. 9.15" class="form-input" required />
              </div>
              <div class="form-group span-2">
                <label>Resume Link / File Drive URL</label>
                <input type="url" v-model="profileForm.resume" placeholder="e.g. https://drive.google.com/your-resume-link" class="form-input" />
              </div>
            </div>
            <div class="form-actions mt-4">
              <button type="submit" class="btn-primary" :disabled="submittingProfile">
                <span v-if="submittingProfile">Saving...</span>
                <span v-else><i class="bi bi-save"></i> Save Profile Details</span>
              </button>
            </div>
          </form>
        </div>
      </section>

      <!-- Dashboard Statistics and Drive list -->
      <div v-else class="dashboard-body">
        
        <!-- Application Stats Summary -->
        <section class="stats-row">
          <div class="stat-card">
            <div class="stat-icon-wrapper blue">
              <i class="bi bi-briefcase"></i>
            </div>
            <div class="stat-details">
              <span class="stat-label">Applications</span>
              <span class="stat-value">{{ applications.length }}</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon-wrapper green">
              <i class="bi bi-check2-all"></i>
            </div>
            <div class="stat-details">
              <span class="stat-label">Shortlisted / Scheduled</span>
              <span class="stat-value">{{ shortlistedCount }}</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon-wrapper purple">
              <i class="bi bi-calendar-event"></i>
            </div>
            <div class="stat-details">
              <span class="stat-label">Interviews</span>
              <span class="stat-value">{{ interviews.length }}</span>
            </div>
          </div>
        </section>

        <!-- Main Workspace split (Removed active drives, interview list, and application history) -->
        <div class="main-grid">
          <!-- Empty for now, stats display above -->
        </div>

        <!-- Charts Section -->
        <section class="charts-grid">
          <div class="chart-card">
            <h3 class="chart-title"><i class="bi bi-pie-chart-fill"></i> Application Status</h3>
            <div class="chart-wrap">
              <canvas ref="statusChartRef"></canvas>
            </div>
          </div>
          <div class="chart-card">
            <h3 class="chart-title"><i class="bi bi-graph-up-arrow"></i> My Placement Journey</h3>
            <div class="chart-wrap">
              <canvas ref="journeyChartRef"></canvas>
            </div>
          </div>
        </section>

      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import Chart from 'chart.js/auto'

const router = useRouter()
const activeNav = ref('Dashboard')

const navItems = [
  { label: 'Dashboard', icon: '<i class="bi bi-speedometer2"></i>' },
  { label: 'Drives',    icon: '<i class="bi bi-megaphone"></i>' },
  { label: 'Applications', icon: '<i class="bi bi-file-earmark-text"></i>' },
  { label: 'Profile',   icon: '<i class="bi bi-person-bounding-box"></i>' }
]

watch(activeNav, (newVal) => {
  if (newVal === 'Drives') {
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

// Data references
const userName = ref('Student')
const isBlacklisted = ref(false)
const hasProfile = ref(true)
const loading = ref(false)
const toastMessage = ref('')
const toastType = ref('success')

// Profile setup form
const profileForm = ref({
  roll_number: '',
  branch: '',
  year_of_study: '',
  cgpa: '',
  resume: ''
})
const submittingProfile = ref(false)

// Dashboard data lists
const drives = ref([])
const applications = ref([])
const interviews = ref([])
const applyingDriveId = ref(null)
const statusChartRef = ref(null)
const journeyChartRef = ref(null)
let statusChartInst = null
let journeyChartInst = null

function renderCharts() {
  const applied = applications.value.filter(a => a.status?.toLowerCase() === 'applied').length
  const shortlisted = applications.value.filter(a => ['shortlisted', 'interview scheduled'].includes(a.status?.toLowerCase())).length
  const rejected = applications.value.filter(a => a.status?.toLowerCase() === 'rejected').length
  const selected = applications.value.filter(a => a.status?.toLowerCase() === 'selected').length

  if (statusChartRef.value) {
    if (statusChartInst) statusChartInst.destroy()
    statusChartInst = new Chart(statusChartRef.value.getContext('2d'), {
      type: 'doughnut',
      data: {
        labels: ['Applied', 'Shortlisted', 'Rejected', 'Selected'],
        datasets: [{ data: [applied, shortlisted, rejected, selected], backgroundColor: ['#81b29a', '#3d5a80', '#e07a5f', '#2d6b5e'], borderWidth: 0 }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { usePointStyle: true, padding: 14, font: { size: 12 } } } } }
    })
  }

  if (journeyChartRef.value) {
    if (journeyChartInst) journeyChartInst.destroy()
    journeyChartInst = new Chart(journeyChartRef.value.getContext('2d'), {
      type: 'bar',
      data: {
        labels: ['Drives Available', 'Applied', 'Shortlisted', 'Interviews', 'Selected'],
        datasets: [{
          label: 'Count',
          data: [drives.value.length, applications.value.length, shortlisted, interviews.value.length, selected],
          backgroundColor: ['#c8d3d2', '#81b29a', '#3d5a80', '#6b21a8', '#2d6b5e'],
          borderRadius: 8
        }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } } }
    })
  }
}

const shortlistedCount = computed(() => {
  return applications.value.filter(app => {
    const s = app.status.toLowerCase()
    return s === 'shortlisted' || s === 'interview scheduled' || s === 'selected'
  }).length
})

function showToast(msg, type = 'success') {
  toastMessage.value = msg
  toastType.value = type
  setTimeout(() => { toastMessage.value = '' }, 3500)
}

function handleLogout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user')
  router.push('/login')
}

// Fetch stats and data
async function fetchDashboardData() {
  const token = localStorage.getItem('access_token')
  if (!token) return
  
  loading.value = true
  try {
    // 1. Fetch profile status
    const profileRes = await fetch('http://localhost:5555/api/student/profile/status', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (profileRes.ok) {
      const pData = await profileRes.json()
      hasProfile.value = pData.hasProfile
      isBlacklisted.value = pData.isBlacklisted
      
      if (!pData.hasProfile) {
        loading.value = false
        return
      }
    }

    // 2. Fetch eligible drives
    const drivesRes = await fetch('http://localhost:5555/api/student/drives', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (drivesRes.ok) {
      drives.value = await drivesRes.json()
    }

    // 3. Fetch applications
    const appsRes = await fetch('http://localhost:5555/api/student/applications', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (appsRes.ok) {
      applications.value = await appsRes.json()
    }

    // 4. Fetch interviews
    const ivRes = await fetch('http://localhost:5555/api/student/interviews', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (ivRes.ok) {
      interviews.value = await ivRes.json()
    }
  } catch (e) {
    showToast('Failed to fetch dashboard data.', 'error')
  } finally {
    loading.value = false
  }
  renderCharts()
}

onMounted(() => {
  const userJson = localStorage.getItem('user')
  if (userJson) {
    const user = JSON.parse(userJson)
    userName.value = user.name || 'Student'
  }
  fetchDashboardData()
})

// Save profile details
async function saveProfile() {
  const token = localStorage.getItem('access_token')
  submittingProfile.value = true
  try {
    const res = await fetch('http://localhost:5555/api/student/profile/setup', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(profileForm.value)
    })
    const data = await res.json()
    if (!res.ok) {
      showToast(data.message || 'Failed to save profile details.', 'error')
      return
    }
    showToast('Profile setup successfully!')
    hasProfile.value = true
    fetchDashboardData()
  } catch {
    showToast('Server connection error.', 'error')
  } finally {
    submittingProfile.value = false
  }
}

// Apply now
async function applyToDrive(drive) {
  const token = localStorage.getItem('access_token')
  applyingDriveId.value = drive.id
  try {
    const res = await fetch(`http://localhost:5555/api/student/apply/${drive.id}`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await res.json()
    if (!res.ok) {
      showToast(data.message || 'Failed to apply.', 'error')
      return
    }
    showToast(`Successfully applied to ${drive.title}!`)
    fetchDashboardData()
  } catch {
    showToast('Network error.', 'error')
  } finally {
    applyingDriveId.value = null
  }
}

// Helper formatting utilities
function formatDeadline(dateStr) {
  if (!dateStr) return 'No deadline'
  return new Date(dateStr).toLocaleDateString('en-IN', {
    day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
  })
}

function formatDateTime(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('en-IN', {
    day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit'
  })
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('en-IN', {
    day: 'numeric', month: 'short', year: 'numeric'
  })
}

function getStatusClass(status) {
  if (!status) return 'badge-applied'
  const s = status.toLowerCase()
  if (s === 'shortlisted') return 'badge-shortlisted'
  if (s === 'interview scheduled') return 'badge-interview'
  if (s === 'rejected') return 'badge-rejected'
  if (s === 'selected') return 'badge-selected'
  return 'badge-applied'
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

.dashboard-body { padding: 24px 28px; }

/* Metrics Row */
.stats-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; margin-bottom: 24px; }
.stat-card { background: #fff; border: 1px solid #eff3f2; padding: 20px; border-radius: 12px; display: flex; align-items: center; gap: 16px; }
.stat-icon-wrapper { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; }
.stat-icon-wrapper.blue { background: #e0f2fe; color: #0369a1; }
.stat-icon-wrapper.green { background: #d1fae5; color: #065f46; }
.stat-icon-wrapper.purple { background: #f3e8ff; color: #6b21a8; }
.stat-label { font-size: 12.5px; color: #8a9e9a; display: block; }
.stat-value { font-size: 22px; font-weight: 700; color: #1a2e28; margin-top: 2px; }

/* Grid splits */
.main-grid { display: grid; grid-template-columns: 1.6fr 1fr; gap: 24px; align-items: start; }
@media (max-width: 1024px) { .main-grid { grid-template-columns: 1fr; } }

.card { background: #fff; border-radius: 12px; border: 1px solid #eff3f2; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.02); }
.card-header { margin-bottom: 16px; }
.card-title { font-size: 15px; font-weight: 700; color: #1a2e28; margin: 0; }
.card-subtitle { font-size: 12px; color: #8a9e9a; margin-top: 2px; }

/* Setup profile details card styling */
.setup-card { max-width: 680px; margin: 32px auto; }
.card-header.border-none { display: flex; align-items: center; gap: 14px; margin-bottom: 24px; }
.header-icon-box { width: 50px; height: 50px; border-radius: 12px; background: #e8f4f1; color: #2d6b5e; display: flex; align-items: center; justify-content: center; font-size: 24px; }
.setup-form .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.setup-form .form-grid .span-2 { grid-column: span 2; }
.form-group label { display: block; font-size: 12.5px; font-weight: 600; color: #374151; margin-bottom: 6px; }
.form-input { width: 100%; padding: 10px 14px; border: 1.5px solid #d1d5db; border-radius: 8px; font-size: 13.5px; outline: none; transition: border-color 0.15s; background: #fafafa; }
.form-input:focus { border-color: #2d6b5e; background: #fff; }
.btn-primary { background: #2d6b5e; color: #fff; border: none; border-radius: 8px; padding: 10px 20px; font-size: 13.5px; font-weight: 600; cursor: pointer; transition: background 0.15s; }
.btn-primary:hover { background: #235349; }

/* Drives List */
.drives-list { display: flex; flex-direction: column; gap: 16px; }
.drive-item { border: 1px solid #eff3f2; border-radius: 10px; padding: 16px; transition: border-color 0.15s; }
.drive-item:hover { border-color: #cbd5e1; }
.drive-header { display: flex; justify-content: space-between; align-items: flex-start; }
.drive-title { font-size: 14.5px; color: #1a2e28; margin: 0; }
.drive-company { font-size: 12.5px; color: #4aa897; display: inline-flex; align-items: center; gap: 4px; margin-top: 4px; }
.mode-badge { font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 20px; }
.mode-badge.onsite { background: #e0f2fe; color: #0369a1; }
.mode-badge.remote { background: #d1fae5; color: #065f46; }
.mode-badge.hybrid { background: #fef3c7; color: #92400e; }

.drive-body-desc { font-size: 12.5px; color: #4b5563; margin-top: 10px; line-height: 1.5; }
.drive-tags { display: flex; gap: 8px; flex-wrap: wrap; }
.tag { font-size: 11px; font-weight: 500; background: #f3f4f6; color: #374151; padding: 2px 8px; border-radius: 4px; display: inline-flex; align-items: center; gap: 4px; }

.drive-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 14px; padding-top: 12px; border-top: 1px dashed #eff3f2; }
.deadline-box { font-size: 11.5px; color: #8a9e9a; display: flex; align-items: center; gap: 5px; }

.btn-apply { background: #2d6b5e; color: #fff; border: none; border-radius: 6px; padding: 6px 14px; font-size: 12px; font-weight: 600; cursor: pointer; transition: background 0.15s; }
.btn-apply:hover { background: #235349; }
.badge-status-applied { font-size: 11.5px; font-weight: 600; color: #2d6b5e; background: #e8f4f1; padding: 4px 10px; border-radius: 6px; }
.badge-ineligible { font-size: 11.5px; font-weight: 600; color: #b94a3b; background: #fdf2f2; padding: 4px 10px; border-radius: 6px; cursor: help; }
.badge-disabled { font-size: 11.5px; font-weight: 600; color: #6b7280; background: #f3f4f6; padding: 4px 10px; border-radius: 6px; }

/* Trackers styling */
.tracker-list { display: flex; flex-direction: column; gap: 12px; }
.tracker-item { border: 1px solid #eff3f2; border-radius: 8px; padding: 12px; }
.tracker-item.iv-item { border-left: 3px solid #6b21a8; background: #faf5ff; }
.badge-mode-online { font-size: 10.5px; font-weight: 600; padding: 2px 6px; border-radius: 4px; background: #f3e8ff; color: #6b21a8; height: fit-content; }
.btn-join-meet { font-size: 11.5px; font-weight: 600; color: #6b21a8; text-decoration: none; display: inline-flex; align-items: center; gap: 4px; }
.btn-join-meet:hover { text-decoration: underline; }

.status-badge { font-size: 10.5px; font-weight: 600; padding: 2px 7px; border-radius: 20px; }
.badge-shortlisted { background: #e0f2fe; color: #0369a1; }
.badge-interview { background: #d1fae5; color: #065f46; }
.badge-rejected { background: #fee2e2; color: #991b1b; }
.badge-selected { background: #dcfce7; color: #14532d; }
.badge-applied { background: #f3f4f6; color: #374151; }

.comment-box { font-size: 11px; background: #fef2f2; border: 1px solid #fecaca; color: #b91c1c; padding: 6px 10px; border-radius: 6px; }
.comment-lbl { font-weight: 700; }

.tracker-empty { text-align: center; padding: 20px 0; font-size: 12px; color: #8a9e9a; }
.empty-state { text-align: center; padding: 40px 0; color: #8a9e9a; font-size: 13px; }

/* Toast */
.toast-alert { position: fixed; bottom: 24px; right: 24px; padding: 12px 20px; border-radius: 8px; font-size: 13px; font-weight: 500; color: #fff; z-index: 9999; box-shadow: 0 4px 16px rgba(0,0,0,0.15); display: flex; align-items: center; gap: 8px; }
.toast-alert.success { background: #2d6b5e; }
.toast-alert.error { background: #dc2626; }

/* ── Chart Section ─────────────── */
.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 4px;
}

.chart-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 22px 24px 20px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.02);
}

.chart-title {
  font-size: 14.5px;
  font-weight: 700;
  color: #27231e;
  margin: 0 0 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.chart-title i { color: #2d6b5e; }

.chart-wrap {
  position: relative;
  height: 250px;
}

@media (max-width: 768px) {
  .charts-grid { grid-template-columns: 1fr; }
  .chart-wrap { height: 210px; }
}
</style>
