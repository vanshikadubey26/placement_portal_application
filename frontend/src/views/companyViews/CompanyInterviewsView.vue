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
          <h1 class="topbar-title">Interview Schedules</h1>
          <p class="topbar-subtitle">LaunchPad Corporate Dashboard</p>
        </div>
      </header>

      <!-- Toast Alerts -->
      <div v-if="toastMessage" class="toast-alert" :class="toastType">
        <i :class="toastType === 'success' ? 'bi bi-check-circle-fill' : 'bi bi-exclamation-circle-fill'"></i>
        <span>{{ toastMessage }}</span>
      </div>

      <!-- Interviews Table -->
      <section class="card table-card">
        <div class="table-header">
          <div class="table-title-group">
            <h2 class="table-title">Interview Schedules</h2>
            <p class="table-subtitle">Coordinate and run interviews for shortlisted candidates.</p>
          </div>
        </div>

        <div class="table-wrapper">
          <table class="interviews-table">
            <thead>
              <tr>
                <th>Candidate</th>
                <th>Drive</th>
                <th>Time / Date</th>
                <th>Mode</th>
                <th>Location / Meeting Link</th>
                <th class="text-center">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="interview in interviews" :key="interview.id">
                <td>
                  <div class="candidate-cell">
                    <span class="avatar-small">{{ interview.studentName.charAt(0) }}</span>
                    <div class="candidate-info">
                      <span class="name-text">{{ interview.studentName }}</span>
                      <span :class="['app-status-badge', getStatusClass(interview.application_status)]">
                        {{ interview.application_status || 'Interview Scheduled' }}
                      </span>
                    </div>
                  </div>
                </td>
                <td>{{ interview.driveTitle }}</td>
                <td class="date-cell">{{ formatDateTime(interview.scheduled_at) }}</td>
                <td>
                  <span class="work-mode-badge" :class="interview.mode.toLowerCase().replace('-', '').replace(' ', '')">{{ interview.mode }}</span>
                </td>
                <td>
                  <a v-if="interview.meeting_link" :href="interview.meeting_link" target="_blank" class="link-style">
                    Join Meeting <i class="bi bi-box-arrow-up-right text-xs"></i>
                  </a>
                  <span v-else>{{ interview.location || '—' }}</span>
                </td>
                <td class="text-center" style="display: flex; gap: 8px; justify-content: center; align-items: center;">
                    <!-- Reminder Button -->
                    <button
                      class="btn-reminder"
                      :disabled="sendingReminderId === interview.id"
                      @click="sendReminder(interview)"
                      style="background: #253a35; color: white; border: none; border-radius: 6px; padding: 6px 12px; font-size: 12px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 4px; transition: background 0.15s;"
                    >
                      <span v-if="sendingReminderId === interview.id">
                        <i class="bi bi-hourglass-split"></i> Reminding...
                      </span>
                      <span v-else>
                        <i class="bi bi-bell"></i> Remind
                      </span>
                    </button>

                    <button
                      v-if="interview.application_status === 'Job Offered'"
                      class="btn-offer-sent"
                      disabled
                    >
                      <i class="bi bi-envelope-check-fill"></i> Offer Sent
                    </button>
                    <button
                      v-else
                      class="btn-offer"
                      :disabled="sendingOfferId === interview.application_id"
                      @click="sendOfferLetter(interview)"
                    >
                      <span v-if="sendingOfferId === interview.application_id">
                        <i class="bi bi-hourglass-split"></i> Sending...
                      </span>
                      <span v-else>
                        <i class="bi bi-envelope-arrow-up"></i> Send Offer
                      </span>
                    </button>
                  </td>
                </tr>
                <tr v-if="interviews.length === 0 && !loading">
                <td colspan="5" class="empty-state">No interviews scheduled yet.</td>
              </tr>
              <tr v-if="loading">
                <td colspan="5" class="empty-state">Loading interviews...</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Schedule Interview Modal -->
      <Teleport to="body">
        <div class="modal-overlay" v-if="showScheduleModal" @click.self="showScheduleModal = false">
          <div class="modal">
            <div class="modal-header">
              <span class="modal-icon"><i class="bi bi-calendar-event"></i></span>
              <div>
                <h3 class="modal-title">Schedule Interview</h3>
                <span class="modal-subtitle">Invite a candidate for evaluation</span>
              </div>
            </div>
            <form @submit.prevent="scheduleInterview">
              <div class="modal-body">
                <div class="form-group mb-3">
                  <label class="form-label">Select Candidate</label>
                  <select class="form-control" v-model="newInterview.studentName" required>
                    <option v-for="candidate in shortlistedCandidates" :key="candidate.id" :value="candidate.studentName">
                      {{ candidate.studentName }} ({{ candidate.driveTitle }})
                    </option>
                  </select>
                </div>
                <div class="form-group mb-3">
                  <label class="form-label">Drive Title</label>
                  <select class="form-control" v-model="newInterview.driveTitle" required>
                    <option v-for="drive in drives" :key="drive.id" :value="drive.title">{{ drive.title }}</option>
                  </select>
                </div>
                <div class="form-group mb-3">
                  <label class="form-label">Scheduled Date & Time</label>
                  <input type="datetime-local" class="form-control" v-model="newInterview.scheduled_at" required />
                </div>
                <div class="form-group mb-3">
                  <label class="form-label">Interview Mode</label>
                  <select class="form-control" v-model="newInterview.mode" required>
                    <option>Remote</option>
                    <option>On-site</option>
                    <option>Hybrid</option>
                  </select>
                </div>
                <div class="form-group mb-3" v-if="newInterview.mode === 'Remote'">
                  <label class="form-label">Meeting Link</label>
                  <input type="url" class="form-control" v-model="newInterview.meeting_link" placeholder="https://meet.google.com/..." required />
                </div>
                <div class="form-group mb-3" v-else>
                  <label class="form-label">Location / Room Office</label>
                  <input type="text" class="form-control" v-model="newInterview.location" placeholder="e.g. Conference Room 3B" required />
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn-secondary me-2" @click="showScheduleModal = false">Cancel</button>
                <button type="submit" class="btn-primary">Schedule</button>
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
const activeNav = ref('Interviews')

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
  pocEmail: 'hr@nexustech.io'
})

// Interviews fetched from API
const interviews = ref([])
const loading = ref(false)
const sendingOfferId = ref(null)
const sendingReminderId = ref(null)

async function sendReminder(interview) {
  const token = localStorage.getItem('access_token')
  sendingReminderId.value = interview.id
  try {
    const res = await fetch(`http://localhost:5555/api/company/interview/${interview.id}/remind`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    const data = await res.json()
    if (res.ok) {
      showToast(data.message || 'Reminder sent successfully!')
    } else {
      showToast(data.message || 'Failed to send reminder.', 'error')
    }
  } catch (err) {
    showToast('Cannot connect to server to send reminder.', 'error')
  } finally {
    sendingReminderId.value = null
  }
}

const showScheduleModal = ref(false)
const toastMessage = ref('')
const toastType = ref('success')

const newInterview = ref({
  studentName: '',
  driveTitle: '',
  scheduled_at: '',
  mode: 'Remote',
  meeting_link: '',
  location: ''
})

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    showToast('Unauthorized. Redirecting to login...', 'error')
    setTimeout(() => router.push('/login'), 1500)
    return
  }
  loading.value = true
  try {
    const res = await fetch('http://localhost:5555/api/company/interviews', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (!res.ok) {
      const data = await res.json()
      showToast(data.message || 'Failed to load interviews.', 'error')
      return
    }
    interviews.value = await res.json()
  } catch {
    showToast('Unable to fetch interviews.', 'error')
  } finally {
    loading.value = false
  }
})

function showToast(msg, type = 'success') {
  toastMessage.value = msg
  toastType.value = type
  setTimeout(() => {
    toastMessage.value = ''
  }, 3500)
}

function formatDateTime(dateTimeStr) {
  if (!dateTimeStr) return '—'
  return new Date(dateTimeStr).toLocaleDateString('en-IN', {
    day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit'
  })
}

function getStatusClass(status) {
  if (!status) return 'status-interview'
  const s = status.toLowerCase()
  if (s === 'job offered') return 'status-offered'
  if (s === 'shortlisted') return 'status-shortlisted'
  if (s === 'rejected') return 'status-rejected'
  if (s === 'interview scheduled') return 'status-interview'
  return 'status-applied'
}

function scheduleInterview() {
  // Redirect to Shortlisted page where interview scheduling is done per-application
  router.push('/company/shortlisted')
}

async function sendOfferLetter(interview) {
  const token = localStorage.getItem('access_token')
  sendingOfferId.value = interview.application_id
  try {
    const res = await fetch(
      `http://localhost:5555/api/company/application/${interview.application_id}/offer-letter`,
      {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      }
    )
    const data = await res.json()
    if (!res.ok) {
      showToast(data.message || 'Failed to send offer letter.', 'error')
      return
    }
    // Update application_status reactively so button switches to 'Offer Sent' permanently
    interview.application_status = 'Job Offered'
    showToast(`Offer letter sent to ${interview.studentName}!`)
  } catch {
    showToast('Network error while sending offer letter.', 'error')
  } finally {
    sendingOfferId.value = null
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

.interviews-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 13px;
}

.interviews-table th {
  background: #f9fdfb;
  color: #5a7a75;
  font-weight: 600;
  padding: 12px 14px;
  border-bottom: 1.5px solid #eff3f2;
}

.interviews-table td {
  padding: 12px 14px;
  border-bottom: 1px solid #eff3f2;
  color: #2e3e3b;
  vertical-align: middle;
}

.interviews-table tr:last-child td {
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

.name-text {
  font-weight: 600;
  color: #1a2e28;
}

.date-cell {
  white-space: nowrap;
}

.work-mode-badge {
  font-size: 10.5px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
}
.work-mode-badge.remote { background: #e0f2fe; color: #0369a1; }
.work-mode-badge.online { background: #e0f2fe; color: #0369a1; }
.work-mode-badge.hybrid { background: #fef3c7; color: #92400e; }
.work-mode-badge.on-site { background: #e6f4ea; color: #137333; }
.work-mode-badge.inperson { background: #e6f4ea; color: #137333; }

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

.link-style {
  color: #2d6b5e;
  text-decoration: none;
  font-weight: 600;
}
.link-style:hover {
  text-decoration: underline;
}

/* ── Form Styles ───────────────── */
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
  max-width: 500px;
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
.mb-3 { margin-bottom: 12px; }
.text-xs { font-size: 11px; }
.text-center { text-align: center; }

/* ── Offer Letter Button ───────── */
.btn-offer {
  background: linear-gradient(135deg, #1e4d8c, #2563eb);
  color: #fff;
  border: none;
  border-radius: 7px;
  padding: 6px 14px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: opacity 0.15s, transform 0.15s;
  white-space: nowrap;
}
.btn-offer:hover:not(:disabled) { opacity: 0.88; transform: translateY(-1px); }
.btn-offer:disabled { opacity: 0.6; cursor: not-allowed; }

.btn-offer-sent {
  background: #e6f4ea;
  color: #137333;
  border: 1.5px solid #b7dfbf;
  border-radius: 7px;
  padding: 6px 14px;
  font-size: 12px;
  font-weight: 600;
  cursor: default;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  white-space: nowrap;
}

/* Candidate info with status badge */
.candidate-info { display: flex; flex-direction: column; gap: 3px; }

.app-status-badge {
  font-size: 10px;
  font-weight: 600;
  padding: 2px 7px;
  border-radius: 10px;
  display: inline-block;
  width: fit-content;
}
.status-interview  { background: #d1fae5; color: #065f46; }
.status-shortlisted { background: #e0f2fe; color: #0369a1; }
.status-offered     { background: #fef3c7; color: #92400e; }
.status-rejected    { background: #fee2e2; color: #991b1b; }
.status-applied     { background: #f3f4f6; color: #374151; }
</style>
