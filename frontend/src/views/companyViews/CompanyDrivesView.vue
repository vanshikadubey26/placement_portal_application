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
          <h1 class="topbar-title">Placement Drives</h1>
          <p class="topbar-subtitle">LaunchPad Corporate Dashboard</p>
        </div>
      </header>

      <!-- Toast Alerts -->
      <div v-if="toastMessage" class="toast-alert" :class="toastType">
        <i :class="toastType === 'success' ? 'bi bi-check-circle-fill' : 'bi bi-exclamation-circle-fill'"></i>
        <span>{{ toastMessage }}</span>
      </div>

      <!-- Drives Table -->
      <section class="card table-card">
        <div class="table-header">
          <div class="table-title-group">
            <h2 class="table-title">Placement Drives</h2>
            <p class="table-subtitle">Create and manage job openings and qualification requirements.</p>
          </div>
          <button class="btn-primary" @click="router.push('/company/drives/create')">
            <i class="bi bi-plus-lg me-2"></i> Create Placement Drive
          </button>
        </div>

        <div class="table-wrapper">
          <table class="drives-table">
            <thead>
              <tr>
                <th>Job Title</th>
                <th>Pay Scale</th>
                <th>Location</th>
                <th class="text-center">Positions</th>
                <th>Deadline</th>
                <th class="text-center">Status</th>
                <th class="text-center">Approval</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="drive in drives" :key="drive.id">
                <td class="drive-title-cell">
                  <div class="drive-cell-content">
                    <span class="drive-title-text">{{ drive.title }}</span>
                  </div>
                </td>
                <td class="pay-cell">{{ drive.payScale }}</td>
                <td>
                  <div class="drive-title-info">
                    <span>{{ drive.location }}</span>
                    <span class="drive-sub-text">{{ drive.workMode }}</span>
                  </div>
                </td>
                <td class="text-center positions-cell">{{ drive.positions }}</td>
                <td class="date-cell">{{ formatDate(drive.deadline) }}</td>
                <td class="text-center">
                  <span :class="['status-badge', getStatusClass(drive.approved ? drive.status : 'Unapproved')]">
                    {{ drive.approved ? (drive.status === 'Unapproved' ? 'Hiring' : drive.status) : 'Unapproved' }}
                  </span>
                </td>
                <td class="text-center">
                  <span :class="['status-badge', drive.approved ? 'badge-approved' : 'badge-unapproved']">
                    {{ drive.approved ? 'Approved' : 'Pending' }}
                  </span>
                </td>
              </tr>
              <tr v-if="drives.length === 0">
                <td colspan="6" class="empty-state">No placement drives found. Create one to get started.</td>
              </tr>
            </tbody>
          </table>
        </div>
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

// Recruiter Profile Info
const companyProfile = ref({
  name: 'NexusTech Solutions',
  industry: 'Cloud Infrastructure',
  website: 'https://nexustech.io',
  headOffice: 'Bangalore, India',
  description: 'NexusTech provides scalable multi-cloud architectures and hybrid hosting virtualization paradigms.',
  pocName: 'Divya Vardhan',
  pocEmail: 'hr@nexustech.io'
})

// Mock Drives Data
const drives = ref([])

const showCreateDriveModal = ref(false)
const toastMessage = ref('')
const toastType = ref('success')

const newDrive = ref({
  title: '',
  branches: '',
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

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    showToast('Unauthorized session. Redirecting to login...', 'error')
    setTimeout(() => router.push('/login'), 1500)
    return
  }

  // Load profile name/poc
  const userJson = localStorage.getItem('user')
  if (userJson) {
    try {
      const u = JSON.parse(userJson)
      companyProfile.value.name = u.name || companyProfile.value.name
      companyProfile.value.pocEmail = u.email || companyProfile.value.pocEmail
      companyProfile.value.pocName = u.name || companyProfile.value.pocName
    } catch (e) {
      console.error(e)
    }
  }

  // Fetch drives
  try {
    const res = await fetch('http://localhost:5555/api/company/drives', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    if (!res.ok) {
      const data = await res.json()
      showToast(data.message || 'Failed to load placement drives.', 'error')
      return
    }
    const data = await res.json()
    drives.value = data
  } catch (err) {
    showToast('Cannot connect to server to fetch drives.', 'error')
  }
})

function showToast(msg, type = 'success') {
  toastMessage.value = msg
  toastType.value = type
  setTimeout(() => {
    toastMessage.value = ''
  }, 3500)
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('en-IN', {
    year: 'numeric', month: 'short', day: 'numeric'
  })
}

function getStatusClass(status) {
  if (!status) return 'badge-hiring'
  const s = status.toLowerCase()
  if (s === 'unapproved') return 'badge-unapproved'
  if (s === 'hiring') return 'badge-hiring'
  if (s === 'shortlisted') return 'badge-shortlisted'
  if (s === 'closed') return 'badge-closed'
  return 'badge-hiring'
}

async function createDrive() {
  const token = localStorage.getItem('access_token')
  if (!token) {
    showToast('Unauthorized session. Please login again.', 'error')
    return
  }

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

    drives.value.push(data.drive)
    showCreateDriveModal.value = false
    newDrive.value = {
      title: '',
      branches: '',
      payScale: '',
      positions: 1,
      workMode: 'On-site',
      location: '',
      deadline: '',
      eligibility: '',
      skillsRequired: '',
      interviewRounds: '',
      description: ''
    }
    showToast('Placement drive created successfully! Pending admin approval.')
  } catch (err) {
    showToast('Cannot connect to server to publish drive.', 'error')
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

/* ── Cards & Tables ────────────── */
.card {
  background: #fff;
  border-radius: 14px;
  padding: 22px;
  box-shadow: 0 1px 4px rgba(0,0,0,.06);
}

.table-card {
  display: flex;
  flex-direction: column;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-title {
  font-size: 15px;
  font-weight: 700;
  color: #1a2e28;
  margin: 0;
}

.table-subtitle {
  font-size: 12.5px;
  color: #8a9e9a;
  margin-top: 4px;
}

.table-wrapper {
  overflow-x: auto;
  border-radius: 10px;
  border: 1px solid #eff3f2;
}

.drives-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 13px;
}

.drives-table th {
  background: #f9fdfb;
  color: #5a7a75;
  font-weight: 600;
  padding: 12px 14px;
  border-bottom: 1.5px solid #eff3f2;
}

.drives-table td {
  padding: 12px 14px;
  border-bottom: 1px solid #eff3f2;
  color: #2e3e3b;
  vertical-align: middle;
}

.drives-table tr:last-child td {
  border-bottom: none;
}

.drive-title-cell {
  min-width: 180px;
}

.drive-title-info {
  display: flex;
  flex-direction: column;
}

.drive-title-text {
  font-weight: 600;
  color: #1a2e28;
}

.drive-sub-text {
  font-size: 11px;
  color: #8a9e9a;
}

.pay-cell {
  font-weight: 600;
  color: #2d6b5e;
}

.positions-cell {
  font-weight: 600;
}

.date-cell {
  white-space: nowrap;
}

.status-badge {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 12px;
}
.badge-approved { background: #e6f4ea; color: #137333; }
.badge-unapproved { background: #fde8e8; color: #c5221f; }

.status-badge.badge-hiring {
  background: #e6f4ea;
  color: #137333;
}
.status-badge.badge-shortlisted {
  background: #f3e8ff;
  color: #6b21a8;
}
.status-badge.badge-closed {
  background: #fde8e8;
  color: #c5221f;
}

.empty-state {
  text-align: center;
  padding: 40px 0 !important;
  color: #8a9e9a;
  font-size: 13.5px;
}

/* ── Buttons ───────────────────── */
.btn-primary {
  background: #2d6b5e;
  color: white;
  border: none;
  border-radius: 7px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: background 0.15s;
}
.btn-primary:hover {
  background: #235349;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
  border-radius: 7px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}
.btn-secondary:hover {
  background: #e5e7eb;
}

/* ── Form Styles ───────────────── */
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

/* ── Modals ────────────────────── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.35);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal {
  background: #fff;
  border-radius: 14px;
  padding: 24px 28px;
  width: 100%;
  max-width: 580px;
  box-shadow: 0 8px 40px rgba(0,0,0,.18);
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  align-items: center;
  gap: 14px;
  border-bottom: 1px solid #eff3f2;
  padding-bottom: 14px;
  margin-bottom: 16px;
}

.modal-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: #e8f4f1;
  color: #2d6b5e;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-title {
  font-size: 16px;
  font-weight: 700;
  color: #1a2e28;
  margin: 0;
}

.modal-subtitle {
  font-size: 12px;
  color: #8a9e9a;
}

.modal-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.modal-footer {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid #eff3f2;
  padding-top: 14px;
}

.me-2 { margin-right: 8px; }
.mb-2 { margin-bottom: 8px; }
.text-center { text-align: center; }
</style>
