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
          <h1 class="topbar-title">Approved Placement Drives</h1>
          <p class="topbar-subtitle">Apply to active placement drives matching your eligibility</p>
        </div>
        <div class="search-box">
          <i class="bi bi-search search-icon"></i>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search by title, company or location..."
            class="search-input"
          />
          <button v-if="searchQuery" class="search-clear" @click="searchQuery = ''">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </header>

      <!-- Toast Alert -->
      <div v-if="toastMessage" :class="['toast-alert', toastType === 'error' ? 'error' : 'success']">
        <i :class="toastType === 'error' ? 'bi bi-exclamation-circle' : 'bi bi-check-circle'"></i>
        {{ toastMessage }}
      </div>

      <div class="dashboard-body">
        <!-- Stat Cards -->
        <section class="stat-cards">
          <div class="stat-card">
            <div class="stat-top">
              <div class="stat-icon icon-active"><i class="bi bi-check-circle"></i></div>
            </div>
            <div class="stat-label">Active Drives</div>
            <div class="stat-value">{{ activeCount }}</div>
          </div>

          <div class="stat-card">
            <div class="stat-top">
              <div class="stat-icon icon-closed"><i class="bi bi-x-circle"></i></div>
            </div>
            <div class="stat-label">Closed Drives</div>
            <div class="stat-value">{{ closedCount }}</div>
          </div>
        </section>

        <div v-if="loading" class="empty-state">Loading placement drives...</div>
        
        <div v-else class="card table-card">
          <div class="table-header">
            <div class="table-title-group">
              <h2 class="table-title">Approved Placement Drives</h2>
              <p class="table-subtitle">View and apply to corporate recruitment drives</p>
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
                  <th class="text-center">Min CGPA</th>
                  <th>Deadline</th>
                  <th class="text-center">Status</th>
                  <th class="text-center">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="drive in filteredDrives" :key="drive.id">
                  <td class="drive-title-cell">
                    <div class="drive-info">
                      <span class="drive-title-text">{{ drive.title }}</span>
                      <span class="drive-sub-text">{{ drive.branches || 'All branches' }}</span>
                    </div>
                  </td>
                  <td>
                    <span class="company-name"><i class="bi bi-building"></i> {{ drive.company_name }}</span>
                  </td>
                  <td>
                    <div class="drive-info">
                      <span>{{ drive.location || '—' }}</span>
                      <span class="drive-sub-text">
                        <span :class="['mode-badge', drive.workMode.toLowerCase().replace(' ', '')]">
                          {{ drive.workMode }}
                        </span>
                      </span>
                    </div>
                  </td>
                  <td class="pay-cell">{{ drive.payScale || '—' }}</td>
                  <td class="text-center positions-cell">{{ drive.eligibility || '—' }}</td>
                  <td class="date-cell">
                    {{ formatDeadline(drive.deadline) }}
                  </td>
                  <td class="text-center">
                    <span :class="['status-badge', drive.isClosed ? 'badge-closed' : 'badge-active']">
                      {{ drive.isClosed ? 'Closed' : 'Active' }}
                    </span>
                  </td>
                  <td class="text-center">
                    <div style="display: flex; gap: 8px; justify-content: center; align-items: center;">
                      <!-- View Button -->
                      <button class="btn-view" @click="viewDrive(drive)">
                        <i class="bi bi-eye"></i> View
                      </button>

                      <!-- Already Applied -->
                      <span v-if="drive.applied" class="badge-status-applied">
                        Applied ({{ drive.applicationStatus }})
                      </span>

                      <!-- Closed -->
                      <span v-else-if="drive.isClosed" class="badge-disabled">
                        Closed
                      </span>

                      <!-- Blacklisted user -->
                      <span v-else-if="isBlacklisted" class="badge-disabled" title="Account locked by admin.">
                        Locked
                      </span>

                      <!-- Apply Button -->
                      <button v-else @click="applyToDrive(drive)" class="btn-apply" :disabled="applyingDriveId === drive.id">
                        <span v-if="applyingDriveId === drive.id">Applying...</span>
                        <span v-else><i class="bi bi-send-fill"></i> Apply</span>
                      </button>
                    </div>
                  </td>
                </tr>
                <tr v-if="filteredDrives.length === 0">
                  <td colspan="8" class="empty-state">
                    <i class="bi bi-megaphone" style="font-size:36px;display:block;margin-bottom:12px;color:#8a9e9a;"></i>
                    {{ searchQuery ? 'No drives match your search.' : 'No approved placement drives found.' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'

const router = useRouter()
const activeNav = ref('Drives')

const navItems = [
  { label: 'Dashboard', icon: '<i class="bi bi-speedometer2"></i>' },
  { label: 'Drives',    icon: '<i class="bi bi-megaphone"></i>' },
  { label: 'Applications', icon: '<i class="bi bi-file-earmark-text"></i>' },
  { label: 'Profile',   icon: '<i class="bi bi-person-bounding-box"></i>' }
]

watch(activeNav, (newVal) => {
  if (newVal === 'Dashboard') {
    router.push('/student/dashboard')
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

const drives = ref([])
const activeCount = ref(0)
const closedCount = ref(0)
const isBlacklisted = ref(false)
const loading = ref(false)
const applyingDriveId = ref(null)
const toastMessage = ref('')
const toastType = ref('success')
const searchQuery = ref('')

const filteredDrives = computed(() => {
  if (!searchQuery.value.trim()) return drives.value
  const q = searchQuery.value.toLowerCase()
  return drives.value.filter(d =>
    (d.title && d.title.toLowerCase().includes(q)) ||
    (d.company_name && d.company_name.toLowerCase().includes(q)) ||
    (d.location && d.location.toLowerCase().includes(q)) ||
    (d.branches && d.branches.toLowerCase().includes(q)) ||
    (d.skillsRequired && d.skillsRequired.toLowerCase().includes(q))
  )
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

async function fetchDrives() {
  const token = localStorage.getItem('access_token')
  if (!token) return

  loading.value = true
  try {
    const statusRes = await fetch('http://localhost:5555/api/student/profile/status', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (statusRes.ok) {
      const statusData = await statusRes.json()
      isBlacklisted.value = statusData.isBlacklisted
    }

    const drivesRes = await fetch('http://localhost:5555/api/student/approved-drives', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (drivesRes.ok) {
      const data = await drivesRes.json()
      drives.value = data.drives || []
      activeCount.value = data.activeCount || 0
      closedCount.value = data.closedCount || 0
    }
  } catch {
    showToast('Failed to fetch drives.', 'error')
  } finally {
    loading.value = false
  }
}

function viewDrive(drive) {
  router.push(`/drive/profile/${drive.id}`)
}

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
    fetchDrives()
  } catch {
    showToast('Network error.', 'error')
  } finally {
    applyingDriveId.value = null
  }
}

function formatDeadline(dateStr) {
  if (!dateStr) return 'No deadline'
  return new Date(dateStr).toLocaleDateString('en-IN', {
    day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
  })
}

onMounted(() => {
  fetchDrives()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

.student-layout { display: flex; min-height: 100vh; background: #f4f9f8; }
.main-content { flex: 1; display: flex; flex-direction: column; overflow-y: auto; }

.topbar { padding: 20px 28px 16px; background: #fff; border-bottom: 1px solid #eff3f2; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; }
.topbar-title { font-size: 20px; font-weight: 700; color: #1a2e28; margin: 0; }
.topbar-subtitle { font-size: 12.5px; color: #8a9e9a; margin-top: 4px; }

.search-box { display: flex; align-items: center; gap: 8px; background: #f4f9f8; border: 1.5px solid #d4e6e1; border-radius: 10px; padding: 8px 14px; min-width: 280px; transition: border-color 0.2s, box-shadow 0.2s; }
.search-box:focus-within { border-color: #2d6b5e; box-shadow: 0 0 0 3px rgba(45,107,94,0.1); }
.search-icon { color: #8a9e9a; font-size: 14px; flex-shrink: 0; }
.search-input { border: none; background: transparent; outline: none; font-size: 13px; color: #1a2e28; width: 100%; font-family: 'Inter', sans-serif; }
.search-input::placeholder { color: #a3b8b4; }
.search-clear { background: none; border: none; cursor: pointer; color: #8a9e9a; padding: 0; display: flex; align-items: center; font-size: 16px; transition: color 0.15s; }
.search-clear:hover { color: #1a2e28; }

.dashboard-body { padding: 24px 28px; }

/* Stat Cards */
.stat-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 24px;
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
.icon-active    { background: #e0f0ec; color: #2d6b5e; }
.icon-closed { background: #fde8e8; color: #9b1c1c; }

.stat-label { font-size: 12.5px; color: #8a9e9a; font-weight: 500; margin-bottom: 4px; }
.stat-value { font-size: 28px; font-weight: 700; color: #1a2e28; letter-spacing: -.5px; }

/* Card / Table */
.card { background: #fff; border-radius: 14px; padding: 22px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.table-card { display: flex; flex-direction: column; }

.table-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.table-title { font-size: 15.5px; font-weight: 700; color: #1a2e28; margin: 0; }
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

.text-center { text-align: center; }

/* Status badge */
.status-badge {
  font-size: 11.5px; font-weight: 600; padding: 3px 10px;
  border-radius: 12px; white-space: nowrap;
}
.badge-active   { background: #e6f4ea; color: #137333; }
.badge-closed { background: #fde8e8; color: #9b1c1c; }

.mode-badge { font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 20px; display: inline-block; margin-top: 4px; }
.mode-badge.onsite { background: #e0f2fe; color: #0369a1; }
.mode-badge.remote { background: #d1fae5; color: #065f46; }
.mode-badge.hybrid { background: #fef3c7; color: #92400e; }

.btn-apply { background: #2d6b5e; color: #fff; border: none; border-radius: 6px; padding: 7px 16px; font-size: 12px; font-weight: 600; cursor: pointer; transition: background 0.15s; }
.btn-apply:hover { background: #235349; }
.badge-status-applied { font-size: 11.5px; font-weight: 600; color: #2d6b5e; background: #e8f4f1; padding: 4px 10px; border-radius: 6px; }
.badge-ineligible { font-size: 11.5px; font-weight: 600; color: #b94a3b; background: #fdf2f2; padding: 4px 10px; border-radius: 6px; cursor: help; }
.badge-disabled { font-size: 11.5px; font-weight: 600; color: #6b7280; background: #f3f4f6; padding: 4px 10px; border-radius: 6px; }

/* View Button */
.btn-view {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  padding: 7px 14px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.btn-view:hover {
  background: #e5e7eb;
}

.empty-state { text-align: center; padding: 48px 0; color: #8a9e9a; font-size: 13.5px; }

/* Toast */
.toast-alert { position: fixed; bottom: 24px; right: 24px; padding: 12px 20px; border-radius: 8px; font-size: 13px; font-weight: 500; color: #fff; z-index: 9999; box-shadow: 0 4px 16px rgba(0,0,0,0.15); display: flex; align-items: center; gap: 8px; }
.toast-alert.success { background: #2d6b5e; }
.toast-alert.error { background: #dc2626; }
</style>
