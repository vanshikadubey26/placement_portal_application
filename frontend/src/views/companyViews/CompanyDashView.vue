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
          <h1 class="topbar-title">Dashboard Overview</h1>
          <p class="topbar-subtitle">LaunchPad Corporate Dashboard</p>
        </div>
      </header>

      <!-- Stats Cards -->
      <section class="metrics-grid">
        <div class="metric-card">
          <div class="metric-top">
            <div class="metric-icon drives-icon"><i class="bi bi-megaphone"></i></div>
          </div>
          <div class="metric-label">Active Drives</div>
          <div class="metric-value">{{ drivesCount }}</div>
        </div>
        <div class="metric-card">
          <div class="metric-top">
            <div class="metric-icon applicants-icon"><i class="bi bi-people"></i></div>
          </div>
          <div class="metric-label">Total Applicants</div>
          <div class="metric-value">{{ applications.length }}</div>
        </div>
        <div class="metric-card">
          <div class="metric-top">
            <div class="metric-icon shortlisted-icon"><i class="bi bi-patch-check"></i></div>
          </div>
          <div class="metric-label">Shortlisted Candidates</div>
          <div class="metric-value">{{ shortlistedCount }}</div>
        </div>
        <div class="metric-card">
          <div class="metric-top">
            <div class="metric-icon selection-icon"><i class="bi bi-graph-up-arrow"></i></div>
          </div>
          <div class="metric-label">Selection Rate</div>
          <div class="metric-value">{{ selectionRate }}%</div>
        </div>
      </section>



    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'

const router = useRouter()
const activeNav = ref('Dashboard')

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

// Mock Drives Count
const drivesCount = ref(2)

// Mock Applications Data
const applications = ref([
  {
    id: 101,
    studentName: 'Amit Sharma',
    rollNumber: 'CS22B104',
    branch: 'CSE',
    driveTitle: 'Graduate Engineer Trainee',
    cgpa: 8.42,
    status: 'Applied'
  },
  {
    id: 102,
    studentName: 'Priyansh Patel',
    rollNumber: 'IT22B205',
    branch: 'IT',
    driveTitle: 'Graduate Engineer Trainee',
    cgpa: 9.15,
    status: 'Shortlisted'
  },
  {
    id: 103,
    studentName: 'Sneha Rao',
    rollNumber: 'CS22B118',
    branch: 'CSE',
    driveTitle: 'Cloud DevOps Intern',
    cgpa: 7.85,
    status: 'Applied'
  }
])

// Mock Interviews Data
const interviews = ref([
  {
    id: 201,
    studentName: 'Priyansh Patel',
    driveTitle: 'Graduate Engineer Trainee',
    scheduled_at: '2026-07-20T10:30:00',
    mode: 'Remote',
    meeting_link: 'https://meet.google.com/abc-defg-hij'
  }
])

// Computeds
const shortlistedCount = computed(() => {
  return applications.value.filter(app => app.status === 'Shortlisted').length
})

const selectionRate = computed(() => {
  if (applications.value.length === 0) return 0
  return Math.round((shortlistedCount.value / applications.value.length) * 100)
})

// Load user data on mount
onMounted(() => {
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
})

// Methods
function getStatusClass(status) {
  if (status === 'Shortlisted') return 'badge-approved'
  if (status === 'Rejected') return 'badge-unapproved'
  return 'badge-applied'
}

function formatDateTime(dateTimeStr) {
  if (!dateTimeStr) return '—'
  return new Date(dateTimeStr).toLocaleDateString('en-IN', {
    day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit'
  })
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

/* ── Metrics Grid ──────────────── */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.metric-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0,0,0,.06);
  transition: box-shadow .2s, transform .2s;
}

.metric-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,.1);
  transform: translateY(-2px);
}

.metric-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.metric-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.drives-icon { background: #e8f4f1; color: #2d6b5e; }
.applicants-icon { background: #e0f0ec; color: #2d6b5e; }
.shortlisted-icon { background: #e0f2fe; color: #0369a1; }
.selection-icon { background: #fef3c7; color: #92400e; }

.metric-label {
  font-size: 12.5px;
  color: #8a9e9a;
  font-weight: 500;
  margin-bottom: 4px;
}

.metric-value {
  font-size: 28px;
  font-weight: 700;
  color: #1a2e28;
  letter-spacing: -.5px;
}

/* ── Dash Split Grid ───────────── */
.dash-split-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

/* ── Cards & Tables ────────────── */
.card {
  background: #fff;
  border-radius: 14px;
  padding: 22px;
  box-shadow: 0 1px 4px rgba(0,0,0,.06);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-title {
  font-size: 15px;
  font-weight: 700;
  color: #1a2e28;
  margin: 0;
}

.btn-text-link {
  background: none;
  border: none;
  color: #2d6b5e;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
}
.btn-text-link:hover {
  text-decoration: underline;
}

.table-wrapper {
  overflow-x: auto;
  border-radius: 10px;
  border: 1px solid #eff3f2;
}

.dashboard-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 13px;
}

.dashboard-table th {
  background: #f9fdfb;
  color: #5a7a75;
  font-weight: 600;
  padding: 12px 14px;
  border-bottom: 1.5px solid #eff3f2;
}

.dashboard-table td {
  padding: 12px 14px;
  border-bottom: 1px solid #eff3f2;
  color: #2e3e3b;
  vertical-align: middle;
}

.dashboard-table tr:last-child td {
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

.work-mode-badge {
  font-size: 10.5px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
}
.work-mode-badge.remote { background: #e0f2fe; color: #0369a1; }
.work-mode-badge.hybrid { background: #fef3c7; color: #92400e; }
.work-mode-badge.on-site { background: #e6f4ea; color: #137333; }

.empty-state {
  text-align: center;
  padding: 40px 0 !important;
  color: #8a9e9a;
  font-size: 13.5px;
}
</style>
