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
          <h1 class="topbar-title">Received Applications</h1>
          <p class="topbar-subtitle">LaunchPad Corporate Dashboard</p>
        </div>
      </header>

      <!-- Toast Alerts -->
      <div v-if="toastMessage" class="toast-alert" :class="toastType">
        <i :class="toastType === 'success' ? 'bi bi-check-circle-fill' : 'bi bi-exclamation-circle-fill'"></i>
        <span>{{ toastMessage }}</span>
      </div>

      <!-- Applications Table -->
      <section class="card table-card">
        <div class="table-header">
          <div class="table-title-group">
            <h2 class="table-title">Received Applications</h2>
            <p class="table-subtitle">Review applicant profiles, qualifications, and update their pipeline stage.</p>
          </div>
        </div>

        <div class="table-wrapper">
          <table class="applications-table">
            <thead>
              <tr>
                <th>Candidate Name</th>
                <th>Applied Drive</th>
                <th>Branch</th>
                <th class="text-center">CGPA</th>
                <th class="text-center">Status</th>
                <th class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="app in applications" :key="app.id">
                <td class="student-name-cell">
                  <div class="candidate-cell">
                    <span class="avatar-small">{{ app.studentName.charAt(0) }}</span>
                    <div class="candidate-text">
                      <span class="name-text">{{ app.studentName }}</span>
                      <span class="sub-text">{{ app.rollNumber }}</span>
                    </div>
                  </div>
                </td>
                <td>{{ app.driveTitle }}</td>
                <td><span class="badge-branch">{{ app.branch }}</span></td>
                <td class="text-center cgpa-cell">{{ app.cgpa.toFixed(2) }}</td>
                <td class="text-center">
                  <span :class="['status-badge', getStatusClass(app.status)]">{{ app.status }}</span>
                </td>
                <td class="text-center">
                  <div class="action-buttons-wrapper" v-if="app.status && app.status.toLowerCase() === 'applied'">
                    <button class="btn-approve" @click="updateAppStatus(app.id, 'Shortlisted')">Shortlist</button>
                    <button class="btn-unapprove" @click="openRejectModal(app)">Reject</button>
                  </div>
                  <span v-else class="text-muted text-sm">—</span>
                </td>
              </tr>
              <tr v-if="applications.length === 0">
                <td colspan="6" class="empty-state">No student applications received.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Reject Comment Modal -->
      <Teleport to="body">
        <div class="modal-overlay" v-if="showRejectModal" @click.self="closeRejectModal">
          <div class="modal">
            <div class="modal-header">
              <span class="modal-icon"><i class="bi bi-exclamation-triangle"></i></span>
              <div>
                <h3 class="modal-title">Reject Application</h3>
                <span class="modal-subtitle">Provide a reason or comment for candidate rejection</span>
              </div>
            </div>
            <form @submit.prevent="confirmRejection">
              <div class="modal-body" v-if="selectedApp">
                <div class="candidate-context mb-3">
                  <strong>Candidate:</strong> {{ selectedApp.studentName }} ({{ selectedApp.rollNumber }}) <br />
                  <strong>Drive:</strong> {{ selectedApp.driveTitle }}
                </div>
                <div class="form-group">
                  <label class="form-label">Rejection Comment / Feedback *</label>
                  <textarea class="form-control text-area" v-model="rejectComment" rows="4" placeholder="Enter reason (e.g. Required skills mismatch, did not meet threshold criteria)..." required></textarea>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn-secondary me-2" @click="closeRejectModal">Cancel</button>
                <button type="submit" class="btn-unapprove-confirm" :disabled="submittingRejection">
                  Confirm Rejection
                </button>
              </div>
            </form>
          </div>
        </div>
      </Teleport>

    </main>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'

const router = useRouter()
const activeNav = ref('Applications')

// Sidebar Nav Items
const navItems = [
  { label: 'Dashboard',    icon: '<i class="bi bi-speedometer2"></i>' },
  { label: 'Profile',      icon: '<i class="bi bi-building"></i>' },
  { label: 'Drives',       icon: '<i class="bi bi-megaphone"></i>' },
  { label: 'Applications', icon: '<i class="bi bi-file-earmark-text"></i>' },
  { label: 'Shortlisted',  icon: '<i class="bi bi-patch-check"></i>' },
  { label: 'Interviews',   icon: '<i class="bi bi-calendar-event"></i>' }
]

// Navigation Watch
watch(activeNav, (newVal) => {
  if (newVal === 'Dashboard') {
    router.push('/company/dashboard')
  } else if (newVal === 'Profile') {
    router.push('/company/profile')
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

// Mock Applications Data
const applications = ref([])

const toastMessage = ref('')
const toastType = ref('success')

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    showToast('Unauthorized session. Redirecting to login...', 'error')
    setTimeout(() => router.push('/login'), 1500)
    return
  }

  // Load profile metadata
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

  // Fetch received applications
  try {
    const res = await fetch('http://localhost:5555/api/company/applications', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    if (!res.ok) {
      const data = await res.json()
      showToast(data.message || 'Failed to load applications.', 'error')
      return
    }
    const data = await res.json()
    applications.value = data
  } catch (err) {
    showToast('Cannot connect to server to fetch applications.', 'error')
  }
})

function showToast(msg, type = 'success') {
  toastMessage.value = msg
  toastType.value = type
  setTimeout(() => {
    toastMessage.value = ''
  }, 3500)
}

function getStatusClass(status) {
  if (!status) return 'badge-applied'
  const s = status.toLowerCase()
  if (s === 'shortlisted') return 'badge-approved'
  if (s === 'rejected') return 'badge-unapproved'
  return 'badge-applied'
}

const showRejectModal = ref(false)
const rejectComment = ref('')
const selectedApp = ref(null)
const submittingRejection = ref(false)

function openRejectModal(app) {
  selectedApp.value = app
  rejectComment.value = ''
  showRejectModal.value = true
}

function closeRejectModal() {
  selectedApp.value = null
  rejectComment.value = ''
  showRejectModal.value = false
}

async function confirmRejection() {
  if (!selectedApp.value) return
  submittingRejection.value = true
  await updateAppStatus(selectedApp.value.id, 'Rejected', rejectComment.value)
  submittingRejection.value = false
  closeRejectModal()
}

async function updateAppStatus(appId, status, comment = null) {
  const token = localStorage.getItem('access_token')
  if (!token) {
    showToast('Unauthorized session. Please login again.', 'error')
    return
  }

  try {
    const res = await fetch(`http://localhost:5555/api/company/application/${appId}/status`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ status, comment })
    })

    const data = await res.json()
    if (!res.ok) {
      showToast(data.message || 'Failed to update application status.', 'error')
      return
    }

    const app = applications.value.find(a => a.id === appId)
    if (app) {
      app.status = status
    }
    showToast(`Candidate has been successfully ${status.toLowerCase()}!`)
  } catch (err) {
    showToast('Cannot connect to server to update status.', 'error')
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

.applications-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 13px;
}

.applications-table th {
  background: #f9fdfb;
  color: #5a7a75;
  font-weight: 600;
  padding: 12px 14px;
  border-bottom: 1.5px solid #eff3f2;
}

.applications-table td {
  padding: 12px 14px;
  border-bottom: 1px solid #eff3f2;
  color: #2e3e3b;
  vertical-align: middle;
}

.applications-table tr:last-child td {
  border-bottom: none;
}

.candidate-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar-small {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #e8f4f1;
  color: #2d6b5e;
  font-size: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

.candidate-text {
  display: flex;
  flex-direction: column;
}

.name-text {
  font-weight: 600;
  color: #1a2e28;
}

.sub-text {
  font-size: 11px;
  color: #8a9e9a;
}

/* ── Badges ────────────────────── */
.status-badge {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 12px;
}
.badge-approved { background: #e6f4ea; color: #137333; }
.badge-unapproved { background: #fde8e8; color: #c5221f; }
.badge-applied { background: #e0f2fe; color: #0369a1; }

.badge-branch {
  background: #f3f4f6;
  color: #374151;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}

.empty-state {
  text-align: center;
  padding: 40px 0 !important;
  color: #8a9e9a;
  font-size: 13.5px;
}

/* Actions cell wrapper */
.action-buttons-wrapper {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.btn-approve {
  background: #2d6b5e;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 5px 12px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}
.btn-approve:hover { background: #235349; }

.btn-unapprove {
  background: #fde8e8;
  color: #9b1c1c;
  border: 1.5px solid #f8b4b4;
  border-radius: 6px;
  padding: 4px 12px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}
.btn-unapprove:hover {
  background: #fbd5d5;
  border-color: #f0a3a3;
}

.text-center { text-align: center; }
.text-muted { color: #8a9e9a; }
.text-sm { font-size: 12.5px; }

/* ── Rejection Modal Styles ────── */
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
  max-width: 500px;
  box-shadow: 0 8px 40px rgba(0,0,0,.18);
  max-height: 90vh;
  overflow-y: auto;
  text-align: left;
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
  background: #fde8e8;
  color: #c5221f;
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

.candidate-context {
  background: #f9fafb;
  border: 1px solid #eff3f2;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 13px;
  color: #374151;
  line-height: 1.5;
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
  border-color: #e07a5f;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(224,122,95,0.15);
}

.text-area {
  resize: vertical;
  font-family: inherit;
}

.modal-footer {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid #eff3f2;
  padding-top: 14px;
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

.btn-unapprove-confirm {
  background: #c5221f;
  color: white;
  border: none;
  border-radius: 7px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}
.btn-unapprove-confirm:hover {
  background: #9b1c1c;
}
.btn-unapprove-confirm:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.me-2 { margin-right: 8px; }
.mb-3 { margin-bottom: 12px; }
</style>
