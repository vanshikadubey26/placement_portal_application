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
      <header class="topbar">
        <div class="topbar-title-group">
          <h1 class="topbar-title">Shortlisted Candidates</h1>
          <p class="topbar-subtitle">Schedule interviews for shortlisted applicants</p>
        </div>
      </header>

      <section class="card-section">
        <div class="table-wrapper">
          <table class="applications-table">
            <thead>
              <tr>
                <th>Student</th>
                <th>Roll No.</th>
                <th>Branch</th>
                <th class="text-center">CGPA</th>
                <th>Drive</th>
                <th class="text-center">Status</th>
                <th class="text-center">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="app in shortlistedApps" :key="app.id">
                <td>
                  <div class="candidate-cell">
                    <span class="avatar-small">{{ app.studentName.charAt(0) }}</span>
                    <div class="candidate-text">
                      <span class="name-text">{{ app.studentName }}</span>
                      <span class="sub-text">{{ app.branch }}</span>
                    </div>
                  </div>
                </td>
                <td>{{ app.rollNumber }}</td>
                <td><span class="badge-branch">{{ app.branch }}</span></td>
                <td class="text-center cgpa-cell">{{ Number(app.cgpa).toFixed(2) }}</td>
                <td>{{ app.driveTitle }}</td>
                <td class="text-center">
                  <span :class="['status-badge', getStatusClass(app.status)]">{{ app.status }}</span>
                </td>
                <td class="text-center">
                  <button class="btn-schedule" @click="openScheduleModal(app)">
                    <i class="bi bi-calendar-plus"></i> Schedule Interview
                  </button>
                </td>
              </tr>
              <tr v-if="shortlistedApps.length === 0 && !loading">
                <td colspan="7" class="empty-state">
                  <i class="bi bi-patch-check" style="font-size:28px;display:block;margin-bottom:8px;color:#8a9e9a;"></i>
                  No shortlisted candidates yet.
                </td>
              </tr>
              <tr v-if="loading">
                <td colspan="7" class="empty-state">Loading...</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>

    <!-- Schedule Interview Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-box">
        <div class="modal-header">
          <h3 class="modal-title">Schedule Interview</h3>
          <button class="modal-close" @click="closeModal">✕</button>
        </div>
        <div class="modal-body">
          <p class="modal-subtitle">
            Scheduling for <strong>{{ selectedApp?.studentName }}</strong>
            — <span class="drive-name">{{ selectedApp?.driveTitle }}</span>
          </p>

          <div class="form-group">
            <label>Date & Time <span class="required">*</span></label>
            <input type="datetime-local" v-model="form.scheduled_at" class="form-input" />
          </div>

          <div class="form-group">
            <label>Interview Mode <span class="required">*</span></label>
            <select v-model="form.mode" class="form-input">
              <option value="">— Select mode —</option>
              <option value="Online">Online</option>
              <option value="In-Person">In-Person</option>
              <option value="Hybrid">Hybrid</option>
            </select>
          </div>

          <div class="form-group" v-if="form.mode === 'In-Person' || form.mode === 'Hybrid'">
            <label>Location</label>
            <input type="text" v-model="form.location" class="form-input" placeholder="e.g. Conference Room A, HQ" />
          </div>

          <div class="form-group" v-if="form.mode === 'Online' || form.mode === 'Hybrid'">
            <label>Meeting Link</label>
            <input type="url" v-model="form.meeting_link" class="form-input" placeholder="https://meet.google.com/..." />
          </div>

          <div v-if="modalError" class="modal-error">{{ modalError }}</div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="closeModal">Cancel</button>
          <button class="btn-confirm" @click="submitInterview" :disabled="submitting">
            <span v-if="submitting">Scheduling...</span>
            <span v-else><i class="bi bi-calendar-check"></i> Confirm Schedule</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Toast -->
    <div v-if="toastMessage" :class="['toast', toastType === 'error' ? 'toast-error' : 'toast-success']">
      {{ toastMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'

const router = useRouter()
const activeNav = ref('Shortlisted')

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
  if (newVal === 'Profile') {
    const userJson = localStorage.getItem('user')
    if (userJson) {
      const u = JSON.parse(userJson)
      router.push(`/company/profile/${u.id}`)
    } else {
      router.push('/company/dashboard')
    }
    return
  }
  const routes = {
    Dashboard: '/company/dashboard',
    Drives: '/company/drives',
    Applications: '/company/applications',
    Shortlisted: '/company/shortlisted',
    Interviews: '/company/interviews',
    Report: '/company/reports'
  }
  if (routes[newVal]) router.push(routes[newVal])
})

function handleLogout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user')
  router.push('/login')
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

// Data
const applications = ref([])
const loading = ref(false)
const toastMessage = ref('')
const toastType = ref('success')

// Modal state
const showModal = ref(false)
const selectedApp = ref(null)
const submitting = ref(false)
const modalError = ref('')
const form = ref({ scheduled_at: '', mode: '', location: '', meeting_link: '' })

const shortlistedApps = computed(() =>
  applications.value.filter(app => app.status && app.status.toLowerCase() === 'shortlisted')
)

function showToast(msg, type = 'success') {
  toastMessage.value = msg
  toastType.value = type
  setTimeout(() => { toastMessage.value = '' }, 3500)
}

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    showToast('Unauthorized. Redirecting to login...', 'error')
    setTimeout(() => router.push('/login'), 1500)
    return
  }
  loading.value = true
  try {
    const res = await fetch('http://localhost:5555/api/company/applications', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (!res.ok) {
      const data = await res.json()
      showToast(data.message || 'Failed to load applications.', 'error')
      return
    }
    applications.value = await res.json()
  } catch {
    showToast('Unable to fetch applications.', 'error')
  } finally {
    loading.value = false
  }
})

function openScheduleModal(app) {
  selectedApp.value = app
  form.value = { scheduled_at: '', mode: '', location: '', meeting_link: '' }
  modalError.value = ''
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  selectedApp.value = null
  modalError.value = ''
}

async function submitInterview() {
  modalError.value = ''
  if (!form.value.scheduled_at) { modalError.value = 'Please select a date and time.'; return }
  if (!form.value.mode) { modalError.value = 'Please select an interview mode.'; return }

  const token = localStorage.getItem('access_token')
  submitting.value = true
  try {
    const res = await fetch(
      `http://localhost:5555/api/company/application/${selectedApp.value.id}/interview`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          scheduled_at: form.value.scheduled_at,
          mode: form.value.mode,
          location: form.value.location || null,
          meeting_link: form.value.meeting_link || null
        })
      }
    )
    const data = await res.json()
    if (!res.ok) {
      modalError.value = data.message || 'Failed to schedule interview.'
      if (data.error) modalError.value += ` (${data.error})`
      return
    }
    // Update the status locally so this candidate moves off the shortlisted list
    const appInList = applications.value.find(a => a.id === selectedApp.value.id)
    if (appInList) appInList.status = 'Interview Scheduled'
    showToast(`✅ Interview scheduled for ${selectedApp.value.studentName}! Status updated to "Interview Scheduled".`)
    closeModal()
  } catch {
    modalError.value = 'Network error. Please try again.'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

.company-layout { display: flex; min-height: 100vh; background: #f4f9f8; }
.main-content { flex: 1; display: flex; flex-direction: column; overflow-y: auto; }

.topbar { padding: 20px 28px 16px; background: #fff; border-bottom: 1px solid #eff3f2; }
.topbar-title { font-size: 20px; font-weight: 700; color: #1a2e28; margin: 0; }
.topbar-subtitle { font-size: 12.5px; color: #8a9e9a; margin-top: 4px; }

.card-section { padding: 24px 28px; }
.table-wrapper { background: #fff; border-radius: 12px; border: 1px solid #eff3f2; overflow-x: auto; }

.applications-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; }
.applications-table th { background: #f9fdfb; color: #5a7a75; font-weight: 600; padding: 12px 16px; border-bottom: 1.5px solid #eff3f2; }
.applications-table td { padding: 12px 16px; border-bottom: 1px solid #eff3f2; color: #2e3e3b; vertical-align: middle; }
.applications-table tr:last-child td { border-bottom: none; }
.applications-table tr:hover td { background: #f9fdfb; }

.candidate-cell { display: flex; align-items: center; gap: 10px; }
.avatar-small {
  width: 32px; height: 32px; border-radius: 50%;
  background: linear-gradient(135deg, #2d6b5e, #4aa897);
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; color: #fff; font-size: 13px; flex-shrink: 0;
}
.name-text { font-weight: 600; color: #1a2e28; display: block; }
.sub-text { font-size: 11px; color: #8a9e9a; }
.badge-branch { background: #f3f4f6; color: #374151; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 500; }
.cgpa-cell { font-weight: 700; color: #2d6b5e; text-align: center; }
.empty-state { text-align: center; padding: 48px 0; color: #8a9e9a; font-size: 13.5px; }

/* Status badges */
.status-badge { font-size: 11px; font-weight: 600; padding: 3px 9px; border-radius: 20px; display: inline-block; white-space: nowrap; }
.badge-shortlisted   { background: #e0f2fe; color: #0369a1; }
.badge-interview     { background: #d1fae5; color: #065f46; }
.badge-rejected      { background: #fee2e2; color: #991b1b; }
.badge-selected      { background: #dcfce7; color: #14532d; }
.badge-applied       { background: #f3f4f6; color: #374151; }

.btn-schedule {
  background: #2d6b5e; color: white; border: none; border-radius: 6px;
  padding: 7px 14px; font-size: 12px; font-weight: 600; cursor: pointer;
  transition: background 0.15s, transform 0.1s; display: inline-flex; align-items: center; gap: 5px;
}
.btn-schedule:hover { background: #235349; transform: translateY(-1px); }

/* ── Modal ── */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.45);
  display: flex; align-items: center; justify-content: center; z-index: 1000;
  animation: fadeIn 0.2s ease;
}
.modal-box {
  background: #fff; border-radius: 14px; width: 100%; max-width: 460px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2); animation: slideUp 0.25s ease;
  overflow: hidden;
}
.modal-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 20px 24px 16px; border-bottom: 1px solid #eff3f2;
}
.modal-title { font-size: 15px; font-weight: 700; color: #1a2e28; margin: 0; }
.modal-close {
  background: none; border: none; font-size: 16px; color: #8a9e9a;
  cursor: pointer; padding: 4px 8px; border-radius: 4px; transition: color 0.15s;
}
.modal-close:hover { color: #1a2e28; }
.modal-body { padding: 20px 24px; }
.modal-subtitle { font-size: 12.5px; color: #5a7a75; margin: 0 0 18px; }
.drive-name { color: #2d6b5e; font-weight: 600; }

.form-group { margin-bottom: 14px; }
.form-group label { display: block; font-size: 12px; font-weight: 600; color: #374151; margin-bottom: 5px; }
.required { color: #dc2626; }
.form-input {
  width: 100%; padding: 8px 12px; border: 1.5px solid #d1d5db; border-radius: 7px;
  font-size: 13px; color: #1a2e28; outline: none; transition: border-color 0.15s;
}
.form-input:focus { border-color: #2d6b5e; }

.modal-error {
  background: #fef2f2; border: 1px solid #fecaca; border-radius: 6px;
  padding: 8px 12px; color: #dc2626; font-size: 12px; margin-top: 10px;
}
.modal-footer {
  display: flex; justify-content: flex-end; gap: 10px;
  padding: 16px 24px; border-top: 1px solid #eff3f2;
}
.btn-cancel {
  background: #f3f4f6; border: none; border-radius: 7px; padding: 8px 18px;
  font-size: 13px; font-weight: 500; color: #374151; cursor: pointer; transition: background 0.15s;
}
.btn-cancel:hover { background: #e5e7eb; }
.btn-confirm {
  background: #2d6b5e; border: none; border-radius: 7px; padding: 8px 18px;
  font-size: 13px; font-weight: 600; color: #fff; cursor: pointer;
  transition: background 0.15s; display: inline-flex; align-items: center; gap: 6px;
}
.btn-confirm:hover:not(:disabled) { background: #235349; }
.btn-confirm:disabled { opacity: 0.6; cursor: not-allowed; }

/* ── Toast ── */
.toast {
  position: fixed; bottom: 24px; right: 24px; padding: 12px 20px;
  border-radius: 8px; font-size: 13px; font-weight: 500; color: #fff;
  z-index: 9999; box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  animation: slideIn 0.3s ease;
}
.toast-success { background: #2d6b5e; }
.toast-error { background: #dc2626; }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
@keyframes slideIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
</style>
