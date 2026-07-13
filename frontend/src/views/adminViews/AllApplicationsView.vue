<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <Sidebar
      v-model="activeNav"
      :nav-items="navItems"
      logo-img="/Only_logo.png"
      title="LaunchPad"
      subtitle="Admin Console"
      @logout="handleLogout"
    />

    <main class="main-content">
      <!-- Top Bar -->
      <AdminTopbar title="Student Applications" v-model="searchQuery" />

      <!-- Stat Cards -->
      <section class="stat-cards">
        <div class="stat-card">
          <div class="stat-top">
            <div class="stat-icon icon-total"><i class="bi bi-file-earmark-text"></i></div>
            <span class="stat-badge badge-neutral">Total</span>
          </div>
          <div class="stat-label">All Applications</div>
          <div class="stat-value">{{ applications.length }}</div>
        </div>

        <div class="stat-card">
          <div class="stat-top">
            <div class="stat-icon icon-interview"><i class="bi bi-calendar-event"></i></div>
            <span class="stat-badge badge-positive">Scheduled</span>
          </div>
          <div class="stat-label">Interview Schedules</div>
          <div class="stat-value">{{ interviewCount }}</div>
        </div>

        <div class="stat-card">
          <div class="stat-top">
            <div class="stat-icon icon-shortlisted"><i class="bi bi-bookmark-star"></i></div>
            <span class="stat-badge badge-info">Shortlisted</span>
          </div>
          <div class="stat-label">Shortlisted</div>
          <div class="stat-value">{{ shortlistedCount }}</div>
        </div>

        <div class="stat-card">
          <div class="stat-top">
            <div class="stat-icon icon-placed"><i class="bi bi-trophy"></i></div>
            <span class="stat-badge badge-positive">Placed</span>
          </div>
          <div class="stat-label">Placed Students</div>
          <div class="stat-value">{{ placedCount }}</div>
        </div>
      </section>

      <!-- Applications Table -->
      <section class="card table-card">
        <div class="table-header">
          <div class="table-title-group">
            <h2 class="table-title">All Student Applications</h2>
            <p class="table-subtitle">Track every student's application status across all placement drives.</p>
          </div>
        </div>

        <div class="table-wrapper">
          <table class="apps-table">
            <thead>
              <tr>
                <th>Student</th>
                <th>Drive</th>
                <th>Company</th>
                <th class="text-center">Status</th>
                <th>Applied On</th>
                <th class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="app in filteredApplications" :key="app.id">
                <td class="student-cell">
                  <div class="cell-stack">
                    <span class="primary-text">{{ app.student_name }}</span>
                    <span class="sub-text">{{ app.roll_number }} · {{ app.student_email }}</span>
                  </div>
                </td>
                <td class="drive-cell">
                  <span class="primary-text">{{ app.drive_title }}</span>
                </td>
                <td>
                  <div class="cell-stack">
                    <span class="primary-text">{{ app.company_name }}</span>
                    <span class="sub-text">{{ app.company_industry }}</span>
                  </div>
                </td>
                <td class="text-center">
                  <span :class="['status-badge', statusClass(app.status)]">
                    {{ statusLabel(app.status) }}
                  </span>
                </td>
                <td class="date-cell">{{ formatDate(app.created_at) }}</td>
                <td class="text-center">
                  <div class="action-btns">
                    <button class="btn-view" @click="openDriveModal(app)">View Drive</button>
                    <button class="btn-view" @click="openStudentModal(app)">View Student</button>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredApplications.length === 0">
                <td colspan="6" class="empty-state">
                  <div class="empty-icon">📋</div>
                  <div class="empty-title">No applications found</div>
                  <p class="empty-desc">No applications match your search.</p>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Drive Detail Modal -->
      <Teleport to="body">
        <div class="modal-overlay" v-if="showDriveModal" @click.self="showDriveModal = false">
          <div class="modal">
            <div class="modal-header">
              <span class="modal-icon"><i class="bi bi-megaphone"></i></span>
              <div>
                <h3 class="modal-title">{{ activeDrive?.drive_title }}</h3>
                <span class="modal-subtitle">{{ activeDrive?.company_name }} · {{ activeDrive?.company_industry }}</span>
              </div>
            </div>
            <div class="modal-body">
              <div class="info-row"><span class="info-label">Student</span><span class="info-value">{{ activeDrive?.student_name }}</span></div>
              <div class="info-row"><span class="info-label">Roll Number</span><span class="info-value">{{ activeDrive?.roll_number }}</span></div>
              <div class="info-row"><span class="info-label">Status</span><span :class="['status-badge', statusClass(activeDrive?.status)]">{{ statusLabel(activeDrive?.status) }}</span></div>
              <div class="info-row"><span class="info-label">Applied On</span><span class="info-value">{{ formatDate(activeDrive?.created_at) }}</span></div>
              <div class="info-row" v-if="activeDrive?.comment"><span class="info-label">Comment</span><span class="info-value">{{ activeDrive?.comment }}</span></div>
            </div>
            <div class="modal-footer">
              <button class="btn-close-modal" @click="showDriveModal = false">Close</button>
            </div>
          </div>
        </div>
      </Teleport>

      <!-- Student Profile Modal -->
      <Teleport to="body">
        <div class="modal-overlay" v-if="showStudentModal" @click.self="showStudentModal = false">
          <div class="modal">
            <div class="modal-header">
              <span class="modal-avatar">{{ activeStudent?.student_name?.charAt(0) }}</span>
              <div>
                <h3 class="modal-title">{{ activeStudent?.student_name }}</h3>
                <span class="modal-subtitle">{{ activeStudent?.roll_number }}</span>
              </div>
            </div>
            <div class="modal-body">
              <div class="info-row"><span class="info-label">Email</span><span class="info-value">{{ activeStudent?.student_email }}</span></div>
              <div class="info-row"><span class="info-label">Applied For</span><span class="info-value">{{ activeStudent?.drive_title }}</span></div>
              <div class="info-row"><span class="info-label">Company</span><span class="info-value">{{ activeStudent?.company_name }}</span></div>
              <div class="info-row"><span class="info-label">Status</span><span :class="['status-badge', statusClass(activeStudent?.status)]">{{ statusLabel(activeStudent?.status) }}</span></div>
              <div class="info-row"><span class="info-label">Applied On</span><span class="info-value">{{ formatDate(activeStudent?.created_at) }}</span></div>
              <div class="info-row" v-if="activeStudent?.comment"><span class="info-label">Comment</span><span class="info-value">{{ activeStudent?.comment }}</span></div>
            </div>
            <div class="modal-footer">
              <button class="btn-close-modal" @click="showStudentModal = false">Close</button>
            </div>
          </div>
        </div>
      </Teleport>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import AdminTopbar from '@/components/admin/AdminTopbar.vue'

const router = useRouter()
const activeNav = ref('Applications')
const searchQuery = ref('')
const applications = ref([])
const showDriveModal   = ref(false)
const showStudentModal = ref(false)
const activeDrive   = ref(null)
const activeStudent = ref(null)

// ── Sidebar nav ───────────────────────────────
const navItems = [
  { label: 'Dashboard',        icon: '' },
  { label: 'Students',         icon: '' },
  { label: 'Companies',        icon: '' },
  { label: 'Placement Drives', icon: '' },
  { label: 'Applications',     icon: '' },
]

watch(activeNav, (val) => {
  if (val === 'Dashboard')        router.push('/admin/dashboard')
  else if (val === 'Students')         router.push('/admin/students')
  else if (val === 'Companies')        router.push('/admin/companies')
  else if (val === 'Placement Drives') router.push('/admin/drives')
  else if (val === 'Applications')     router.push('/admin/applications')
})

// ── Fetch ─────────────────────────────────────
onMounted(async () => {
  const token = localStorage.getItem('access_token')
  const res = await fetch('http://localhost:5555/admin/all-applications', {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (res.ok) applications.value = await res.json()
})

// ── Computed ──────────────────────────────────
const filteredApplications = computed(() => {
  if (!searchQuery.value) return applications.value
  const q = searchQuery.value.toLowerCase()
  return applications.value.filter(a =>
    (a.student_name && a.student_name.toLowerCase().includes(q)) ||
    (a.drive_title  && a.drive_title.toLowerCase().includes(q)) ||
    (a.company_name && a.company_name.toLowerCase().includes(q)) ||
    (a.roll_number  && a.roll_number.toLowerCase().includes(q))
  )
})

const interviewCount  = computed(() => applications.value.filter(a => a.status === 'interview_scheduled').length)
const shortlistedCount = computed(() => applications.value.filter(a => a.status === 'shortlisted').length)
const placedCount     = computed(() => applications.value.filter(a => a.status === 'selected').length)

// ── Helpers ───────────────────────────────────
function statusLabel(status) {
  const map = {
    applied:              'Applied',
    shortlisted:          'Shortlisted',
    interview_scheduled:  'Interview Scheduled',
    selected:             'Placed',
    rejected:             'Rejected',
  }
  return map[status] || status
}

function statusClass(status) {
  const map = {
    applied:             'badge-applied',
    shortlisted:         'badge-shortlisted',
    interview_scheduled: 'badge-interview',
    selected:            'badge-placed',
    rejected:            'badge-rejected',
  }
  return map[status] || 'badge-neutral'
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('en-IN', {
    year: 'numeric', month: 'short', day: 'numeric',
  })
}

function openDriveModal(app) {
  router.push(`/drive/profile/${app.drive_id}`)
}

function openStudentModal(app) {
  router.push(`/student/profile/${app.student_id}`)
}

async function handleLogout() {
  try {
    const token = localStorage.getItem('access_token')
    await fetch('http://localhost:5555/api/auth/logout', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
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

* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

/* ─── Layout ─────────────────── */
.admin-layout { display: flex; height: 100vh; background: #f5f5f0; overflow: hidden; }

.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 28px 28px 40px;
  display: flex;
  flex-direction: column;
  gap: 22px;
}

/* ─── Stat Cards ─────────────── */
.stat-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0,0,0,.06);
  transition: box-shadow .2s, transform .2s;
}
.stat-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,.1); transform: translateY(-2px); }

.stat-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }

.stat-icon {
  width: 40px; height: 40px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center; font-size: 18px;
}
.icon-total       { background: #e8f4f1; color: #2d6b5e; }
.icon-interview   { background: #eff6ff; color: #1d4ed8; }
.icon-shortlisted { background: #fef3c7; color: #92400e; }
.icon-placed      { background: #e0f0ec; color: #2d6b5e; }

.stat-badge { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 20px; }
.badge-positive { background: #e0f0ec; color: #2d6b5e; }
.badge-neutral  { background: #f3f4f6; color: #4b5563; }
.badge-info     { background: #fef3c7; color: #92400e; }

.stat-label { font-size: 12.5px; color: #8a9e9a; font-weight: 500; margin-bottom: 4px; }
.stat-value { font-size: 28px; font-weight: 700; color: #1a2e28; letter-spacing: -.5px; }

/* ─── Card / Table ───────────── */
.card { background: #fff; border-radius: 14px; padding: 22px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.table-card { display: flex; flex-direction: column; }

.table-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.table-title { font-size: 15.5px; font-weight: 700; color: #1a2e28; }
.table-subtitle { font-size: 12.5px; color: #8a9e9a; margin-top: 4px; }

.table-wrapper { overflow-x: auto; border-radius: 10px; border: 1px solid #eff3f2; }

.apps-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 13.5px; }
.apps-table th { background: #f9fdfb; color: #5a7a75; font-weight: 600; padding: 14px 16px; border-bottom: 1.5px solid #eff3f2; white-space: nowrap; }
.apps-table td { padding: 14px 16px; border-bottom: 1px solid #eff3f2; color: #2e3e3b; vertical-align: middle; }
.apps-table tr:last-child td { border-bottom: none; }
.apps-table tr:hover td { background: #fdfdfd; }

.cell-stack { display: flex; flex-direction: column; gap: 2px; }
.primary-text { font-weight: 600; color: #1a2e28; }
.sub-text { font-size: 11px; color: #8a9e9a; }

.drive-cell { max-width: 200px; }
.date-cell  { white-space: nowrap; font-size: 13px; color: #5a7a75; }
.comment-cell { max-width: 200px; font-size: 12.5px; color: #6b7280; }

.text-center { text-align: center; }

/* ─── Status badges ──────────── */
.status-badge {
  display: inline-block;
  font-size: 11.5px; font-weight: 600; padding: 3px 10px;
  border-radius: 12px; white-space: nowrap;
}
.badge-applied     { background: #f3f4f6; color: #4b5563; }
.badge-shortlisted { background: #fef3c7; color: #92400e; }
.badge-interview   { background: #dbeafe; color: #1d4ed8; }
.badge-placed      { background: #e6f4ea; color: #137333; }
.badge-rejected    { background: #fde8e8; color: #9b1c1c; }

/* ─── Empty state ────────────── */
.empty-state { text-align: center; padding: 40px 0 !important; }
.empty-icon { font-size: 36px; margin-bottom: 10px; }
.empty-title { font-size: 15px; font-weight: 700; color: #1a2e28; }
.empty-desc { font-size: 12.5px; color: #8a9e9a; margin-top: 6px; }

/* ─── Action buttons ─────────── */
.action-btns { display: flex; justify-content: center; gap: 6px; flex-wrap: wrap; }

.btn-view {
  background: #fff;
  border: 1.5px solid #cdd8d5;
  color: #3a5c55;
  border-radius: 7px;
  padding: 5px 11px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
  transition: all .15s;
}
.btn-view:hover { background: #f0f5f4; border-color: #4a6e6b; }

/* ─── Modal ──────────────────── */
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,.35);
  display: flex; align-items: center; justify-content: center;
  z-index: 999;
}

.modal {
  background: #fff;
  border-radius: 14px;
  padding: 28px 32px;
  width: 100%; max-width: 460px;
  box-shadow: 0 8px 40px rgba(0,0,0,.18);
}

.modal-header {
  display: flex; align-items: center; gap: 14px;
  border-bottom: 1px solid #eff3f2;
  padding-bottom: 16px; margin-bottom: 18px;
}

.modal-icon {
  width: 44px; height: 44px; border-radius: 10px;
  background: #e8f4f1; color: #2d6b5e;
  font-size: 20px; display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}

.modal-avatar {
  width: 44px; height: 44px; border-radius: 50%;
  background: #faeae7; color: #b94a3b;
  font-size: 20px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}

.modal-title   { font-size: 17px; font-weight: 700; color: #1a2e28; }
.modal-subtitle { font-size: 12.5px; color: #8a9e9a; }

.modal-body { display: flex; flex-direction: column; gap: 12px; }

.info-row { display: flex; gap: 12px; align-items: flex-start; font-size: 13.5px; }
.info-label { min-width: 110px; font-weight: 600; color: #5a7a75; flex-shrink: 0; }
.info-value { color: #2e3e3b; }

.modal-footer { margin-top: 20px; display: flex; justify-content: flex-end; }

.btn-close-modal {
  background: #2d6b5e; color: #fff; border: none;
  border-radius: 8px; padding: 9px 22px;
  font-size: 13px; font-weight: 600; cursor: pointer;
  transition: background .15s;
}
.btn-close-modal:hover { background: #235349; }
</style>
