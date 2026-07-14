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
      <AdminTopbar title="Placement Drives" v-model="searchQuery" />

      <!-- Stat Cards -->
      <section class="stat-cards">
        <div class="stat-card">
          <div class="stat-top">
            <div class="stat-icon icon-total"><i class="bi bi-megaphone"></i></div>
          </div>
          <div class="stat-label">All Drives</div>
          <div class="stat-value">{{ drives.length }}</div>
        </div>

        <div class="stat-card">
          <div class="stat-top">
            <div class="stat-icon icon-active"><i class="bi bi-check-circle"></i></div>
          </div>
          <div class="stat-label">Active Drives</div>
          <div class="stat-value">{{ activeDrivesCount }}</div>
        </div>

        <div class="stat-card">
          <div class="stat-top">
            <div class="stat-icon icon-completed"><i class="bi bi-flag-fill"></i></div>
          </div>
          <div class="stat-label">Completed Drives</div>
          <div class="stat-value">{{ completedDrivesCount }}</div>
        </div>
      </section>

      <!-- Unapproved Drives Table -->
      <section class="card table-card">
        <div class="table-header">
          <div class="table-title-group">
            <h2 class="table-title">Unapproved Placement Drives (Pending Approval)</h2>
            <p class="table-subtitle">Review and verify placement drives before they go live for students.</p>
          </div>
        </div>

        <div class="table-wrapper">
          <table class="drives-table">
            <thead>
              <tr>
                <th>Drive Title</th>
                <th>Company</th>
                <th>Location / Mode</th>
                <th>Pay Scale</th>
                <th>Positions</th>
                <th>Deadline</th>
                <th class="text-center">Status</th>
                <th class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="drive in filteredUnapprovedDrives" :key="drive.id">
                <td class="drive-title-cell">
                  <div class="drive-info">
                    <span class="drive-title-text">{{ drive.title }}</span>
                    <span class="drive-sub-text">{{ drive.branches }}</span>
                  </div>
                </td>
                <td>
                  <div class="drive-info">
                    <span class="company-name">{{ drive.company_name }}</span>
                    <span class="drive-sub-text">{{ drive.company_industry }}</span>
                  </div>
                </td>
                <td>
                  <div class="drive-info">
                    <span>{{ drive.location || '—' }}</span>
                    <span class="drive-sub-text">{{ drive.workMode }}</span>
                  </div>
                </td>
                <td class="pay-cell">{{ drive.payScale || '—' }}</td>
                <td class="text-center positions-cell">{{ drive.positions ?? '—' }}</td>
                <td class="date-cell" :class="{ 'text-danger': isExpired(drive.deadline) }">
                  {{ formatDate(drive.deadline) }}
                  <span class="expired-tag" v-if="isExpired(drive.deadline)">Expired</span>
                </td>
                <td class="text-center">
                  <span class="status-badge badge-unapproved">
                    Unapproved
                  </span>
                </td>
                <td class="text-center">
                  <div class="action-buttons-wrapper">
                    <button class="btn-approve" @click="toggleApproval(drive)">
                      Approve
                    </button>
                    <button class="btn-details" @click="viewDetails(drive)">View</button>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredUnapprovedDrives.length === 0">
                <td colspan="8" class="empty-state">
                  <div class="empty-title">No pending approvals</div>
                  <p class="empty-desc">All placement drives have been reviewed and approved.</p>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Approved Drives Table -->
      <section class="card table-card">
        <div class="table-header">
          <div class="table-title-group">
            <h2 class="table-title">Approved Placement Drives</h2>
            <p class="table-subtitle">Monitor and manage all approved corporate placement drives.</p>
          </div>
        </div>

        <div class="table-wrapper">
          <table class="drives-table">
            <thead>
              <tr>
                <th>Drive Title</th>
                <th>Company</th>
                <th>Location / Mode</th>
                <th>Pay Scale</th>
                <th>Positions</th>
                <th>Deadline</th>
                <th class="text-center">Status</th>
                <th class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="drive in filteredApprovedDrives" :key="drive.id">
                <td class="drive-title-cell">
                  <div class="drive-info">
                    <span class="drive-title-text">{{ drive.title }}</span>
                    <span class="drive-sub-text">{{ drive.branches }}</span>
                  </div>
                </td>
                <td>
                  <div class="drive-info">
                    <span class="company-name">{{ drive.company_name }}</span>
                    <span class="drive-sub-text">{{ drive.company_industry }}</span>
                  </div>
                </td>
                <td>
                  <div class="drive-info">
                    <span>{{ drive.location || '—' }}</span>
                    <span class="drive-sub-text">{{ drive.workMode }}</span>
                  </div>
                </td>
                <td class="pay-cell">{{ drive.payScale || '—' }}</td>
                <td class="text-center positions-cell">{{ drive.positions ?? '—' }}</td>
                <td class="date-cell" :class="{ 'text-danger': isExpired(drive.deadline) }">
                  {{ formatDate(drive.deadline) }}
                  <span class="expired-tag" v-if="isExpired(drive.deadline)">Expired</span>
                </td>
                <td class="text-center">
                  <span class="status-badge badge-approved">
                    Approved
                  </span>
                </td>
                <td class="text-center">
                  <div class="action-buttons-wrapper">
                    <button class="btn-unapprove" @click="toggleApproval(drive)">
                      Unapprove
                    </button>
                    <button class="btn-details" @click="viewDetails(drive)">View</button>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredApprovedDrives.length === 0">
                <td colspan="8" class="empty-state">
                  <div class="empty-title">No approved drives found</div>
                  <p class="empty-desc">Try adjusting your search criteria or approve pending drives.</p>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Drive Details Modal -->
      <Teleport to="body">
        <div class="modal-overlay" v-if="showModal" @click.self="showModal = false">
          <div class="modal">
            <div class="modal-header">
              <span class="modal-icon"><i class="bi bi-megaphone"></i></span>
              <div>
                <h3 class="modal-title">{{ selectedDrive?.title }}</h3>
                <span class="modal-subtitle">{{ selectedDrive?.company_name }} · {{ selectedDrive?.company_industry }}</span>
              </div>
            </div>
            <div class="modal-body">
              <div class="info-row"><span class="info-label">Status</span><span :class="['status-badge', selectedDrive?.approved ? 'badge-approved' : 'badge-unapproved']">{{ selectedDrive?.approved ? 'Approved' : 'Unapproved' }}</span></div>
              <div class="info-row"><span class="info-label">Deadline</span><span class="info-value" :class="{ 'text-danger': isExpired(selectedDrive?.deadline) }">{{ formatDate(selectedDrive?.deadline) }}<span v-if="isExpired(selectedDrive?.deadline)"> (Expired)</span></span></div>
              <div class="info-row"><span class="info-label">Pay Scale</span><span class="info-value">{{ selectedDrive?.payScale || '—' }}</span></div>
              <div class="info-row"><span class="info-label">Positions</span><span class="info-value">{{ selectedDrive?.positions ?? '—' }}</span></div>
              <div class="info-row"><span class="info-label">Location</span><span class="info-value">{{ selectedDrive?.location || '—' }} ({{ selectedDrive?.workMode }})</span></div>
              <div class="info-row"><span class="info-label">Eligibility</span><span class="info-value">{{ selectedDrive?.eligibility }}</span></div>
              <div class="info-row"><span class="info-label">Batch</span><span class="info-value">{{ selectedDrive?.batch }}</span></div>
              <div class="info-row"><span class="info-label">Branches</span><span class="info-value">{{ selectedDrive?.branches }}</span></div>
              <div class="info-row"><span class="info-label">Skills Required</span><span class="info-value">{{ selectedDrive?.skillsRequired || '—' }}</span></div>
              <div class="info-row"><span class="info-label">Interview Rounds</span><span class="info-value">{{ selectedDrive?.interviewRounds || '—' }}</span></div>
              <div class="info-row" v-if="selectedDrive?.description"><span class="info-label">Description</span><p class="info-desc">{{ selectedDrive?.description }}</p></div>
            </div>
            <div class="modal-footer">
              <button class="btn-close-modal" @click="showModal = false">Close</button>
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
const activeNav = ref('Placement Drives')
const searchQuery = ref('')
const showModal = ref(false)
const selectedDrive = ref(null)
const drives = ref([])

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
  const res = await fetch('http://localhost:5555/admin/all-drives', {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (res.ok) drives.value = await res.json()
})

// ── Computed ──────────────────────────────────
const filteredDrives = computed(() => {
  if (!searchQuery.value) return drives.value
  const q = searchQuery.value.toLowerCase()
  return drives.value.filter(d =>
    d.title.toLowerCase().includes(q) ||
    (d.company_name && d.company_name.toLowerCase().includes(q)) ||
    (d.location && d.location.toLowerCase().includes(q))
  )
})

const filteredUnapprovedDrives = computed(() =>
  filteredDrives.value.filter(d => !d.approved)
)

const filteredApprovedDrives = computed(() =>
  filteredDrives.value.filter(d => d.approved)
)

const activeDrivesCount = computed(() =>
  drives.value.filter(d => d.approved && !isExpired(d.deadline)).length
)

const completedDrivesCount = computed(() =>
  drives.value.filter(d => isExpired(d.deadline)).length
)

// ── Methods ───────────────────────────────────
function viewDetails(drive) {
  router.push(`/drive/profile/${drive.id}`)
}

async function toggleApproval(drive) {
  try {
    const token = localStorage.getItem('access_token')
    const res = await fetch(`http://localhost:5555/admin/drive/approve/${drive.id}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token}` },
    })
    if (res.ok) {
      const data = await res.json()
      drive.approved = data.approved
    } else {
      console.error('Failed to toggle drive approval')
    }
  } catch (err) {
    console.error('Error toggling drive approval:', err)
  }
}

function isExpired(deadlineStr) {
  if (!deadlineStr) return false
  return new Date(deadlineStr) < new Date()
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('en-IN', {
    year: 'numeric', month: 'short', day: 'numeric'
  })
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
  grid-template-columns: repeat(3, 1fr);
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
.icon-total     { background: #e8f4f1; color: #2d6b5e; }
.icon-active    { background: #e0f0ec; color: #2d6b5e; }
.icon-completed { background: #f3f4f6; color: #4b5563; }

.stat-badge {
  font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 20px;
}
.badge-positive { background: #e0f0ec; color: #2d6b5e; }
.badge-neutral  { background: #f3f4f6; color: #4b5563; }
.badge-negative { background: #fde8e8; color: #9b1c1c; }

.stat-label { font-size: 12.5px; color: #8a9e9a; font-weight: 500; margin-bottom: 4px; }
.stat-value { font-size: 28px; font-weight: 700; color: #1a2e28; letter-spacing: -.5px; }

/* ─── Card / Table ───────────── */
.card { background: #fff; border-radius: 14px; padding: 22px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.table-card { display: flex; flex-direction: column; }

.table-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.table-title { font-size: 15.5px; font-weight: 700; color: #1a2e28; }
.table-subtitle { font-size: 12.5px; color: #8a9e9a; margin-top: 4px; }

.table-wrapper { overflow-x: auto; border-radius: 10px; border: 1px solid #eff3f2; }

.drives-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 13.5px; }
.drives-table th { background: #f9fdfb; color: #5a7a75; font-weight: 600; padding: 14px 16px; border-bottom: 1.5px solid #eff3f2; }
.drives-table td { padding: 14px 16px; border-bottom: 1px solid #eff3f2; color: #2e3e3b; vertical-align: middle; }
.drives-table tr:last-child td { border-bottom: none; }
.drives-table tr:hover td { background: #fdfdfd; }

.drive-title-cell { min-width: 200px; }
.drive-info { display: flex; flex-direction: column; gap: 2px; }
.drive-title-text { font-weight: 600; color: #1a2e28; }
.company-name { font-weight: 600; color: #1a2e28; }
.drive-sub-text { font-size: 11px; color: #8a9e9a; }

.pay-cell { font-weight: 600; color: #2d6b5e; white-space: nowrap; }
.positions-cell { font-weight: 600; color: #1a2e28; }

.date-cell { white-space: nowrap; font-size: 13px; }
.text-danger { color: #b91c1c !important; }
.expired-tag {
  display: inline-block; margin-left: 5px;
  font-size: 10px; font-weight: 600; padding: 1px 6px;
  background: #fde8e8; color: #9b1c1c; border-radius: 10px;
}

.text-center { text-align: center; }

/* Status badge */
.status-badge {
  font-size: 11.5px; font-weight: 600; padding: 3px 10px;
  border-radius: 12px; white-space: nowrap;
}
.badge-approved   { background: #e6f4ea; color: #137333; }
.badge-unapproved { background: #fef3c7; color: #92400e; }

/* View button */
.btn-details {
  background: #fff;
  border: 1.5px solid #cdd8d5;
  color: #3a5c55;
  border-radius: 7px;
  padding: 6px 14px;
  font-size: 12.5px;
  font-weight: 500;
  cursor: pointer;
  transition: all .15s;
}
.btn-details:hover { background: #f0f5f4; border-color: #4a6e6b; }

.action-buttons-wrapper {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.btn-approve {
  background: #2d6b5e;
  color: white;
  border: none;
  border-radius: 7px;
  padding: 6px 14px;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}
.btn-approve:hover {
  background: #235349;
}

.btn-unapprove {
  background: #fde8e8;
  color: #9b1c1c;
  border: 1.5px solid #f8b4b4;
  border-radius: 7px;
  padding: 6px 14px;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}
.btn-unapprove:hover {
  background: #fbd5d5;
  border-color: #f0a3a3;
}

/* ─── Empty state ────────────── */
.empty-state { text-align: center; padding: 40px 0 !important; }
.empty-title { font-size: 15px; font-weight: 700; color: #1a2e28; }
.empty-desc { font-size: 12.5px; color: #8a9e9a; margin-top: 6px; }

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
  width: 100%; max-width: 520px;
  box-shadow: 0 8px 40px rgba(0,0,0,.18);
  max-height: 90vh;
  overflow-y: auto;
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

.modal-title { font-size: 17px; font-weight: 700; color: #1a2e28; }
.modal-subtitle { font-size: 12.5px; color: #8a9e9a; }

.modal-body { display: flex; flex-direction: column; gap: 12px; }

.info-row {
  display: flex; gap: 12px;
  align-items: flex-start;
  font-size: 13.5px;
}

.info-label {
  min-width: 140px; font-weight: 600; color: #5a7a75; flex-shrink: 0;
}

.info-value { color: #2e3e3b; }

.info-desc {
  margin: 4px 0 0; color: #4a6060; font-size: 13px;
  line-height: 1.6;
}

.modal-footer { margin-top: 20px; display: flex; justify-content: flex-end; }

.btn-close-modal {
  background: #2d6b5e; color: #fff; border: none;
  border-radius: 8px; padding: 9px 22px;
  font-size: 13px; font-weight: 600; cursor: pointer;
  transition: background .15s;
}
.btn-close-modal:hover { background: #235349; }
</style>
