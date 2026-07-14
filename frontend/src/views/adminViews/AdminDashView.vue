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

    <!-- Main Content  -->
    <main class="main-content">
      <AdminTopbar
        title="Dashboard Overview"
        v-model="globalSearch"
        :notif-count="3"
        user-name="Admin"
        @notifications="handleNotifications"
        @settings="handleSettings"
      />

      <!-- Stat Cards -->
      <StatCardsGrid :stats="stats" />

      <!-- Body Grid -->
      <div class="bottom-grid">    
      </div>
    </main>

  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar            from '@/components/Sidebar.vue'
import AdminTopbar        from '@/components/admin/AdminTopbar.vue'
import StatCardsGrid      from '@/components/admin/StatCardsGrid.vue'
// import PendingApprovals   from '@/components/admin/PendingApprovals.vue'

const router = useRouter()

// ── State ───────────────────────────────────
const activeNav     = ref('Dashboard')

watch(activeNav, (newVal) => {
  if (newVal === 'Students') {
    router.push('/admin/students')
  } else if (newVal === 'Companies') {
    router.push('/admin/companies')
  } else if (newVal === 'Placement Drives') {
    router.push('/admin/drives')
  } else if (newVal === 'Applications') {
    router.push('/admin/applications')
  } else if (newVal === 'Dashboard') {
    router.push('/admin/dashboard')
  }
})
const globalSearch  = ref('')
const companySearch = ref('')
const studentSearch = ref('')

const navItems = [
  { label: 'Dashboard',        icon: '' },
  { label: 'Students',         icon: '' },
  { label: 'Companies',        icon: '' },
  { label: 'Placement Drives', icon: '' },
  { label: 'Applications',     icon: '' },
]

//  Data 
const stats = ref([
  {
    label: 'Total Students',
    value: '0',
    icon: '<i class="bi bi-mortarboard"></i>',
    iconBg: '#e8f4f1',
    iconColor: '#2d6b5e',
    badge: 'Live',
    badgeColor: '#2d6b5e',
  },
  {
    label: 'Total Companies',
    value: '0',
    icon: '<i class="bi bi-building"></i>',
    iconBg: '#faeae7',
    iconColor: '#b94a3b',
    badge: 'Live',
    badgeColor: '#b94a3b',
  },
  {
    label: 'Job Postings',
    value: '0',
    icon: '<i class="bi bi-megaphone"></i>',
    iconBg: '#e8f4f1',
    iconColor: '#2d6b5e',
    badge: 'Live',
    badgeColor: '#2d6b5e',
  },
  {
    label: 'Total Applications',
    value: '0',
    icon: '<i class="bi bi-file-earmark-text"></i>',
    iconBg: '#f0f4f4',
    iconColor: '#4a6e6b',
    badge: 'Live',
    badgeColor: '#2d6b5e',
  },
])

onMounted(async () => {
  try {
    const token = localStorage.getItem('access_token')
    const res = await fetch('http://localhost:5555/admin/stats', {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (res.ok) {
      const data = await res.json()
      stats.value[0].value = String(data.total_students)
      stats.value[1].value = String(data.total_companies)
      stats.value[2].value = String(data.total_job_postings)
      stats.value[3].value = String(data.total_applications)
    }
  } catch (err) {
    console.error('Failed to fetch admin stats:', err)
  }
})


const pendingApprovals = [
  {
    name: 'NexusTech Solutions',
    meta: 'Industry: Cloud Infrastructure • Applied 2h ago',
    icon: '🏢',
    primaryBtn: 'View Details',
  },
  {
    name: 'Senior Frontend Architect',
    meta: 'By GlobalLink Systems • 12 Vacancies • Drive Date: Oct 12',
    icon: '🚀',
    primaryBtn: 'Review',
  },
  {
    name: 'Precision Manufacturing Ltd.',
    meta: 'Industry: Industrial Automation • Applied 1d ago',
    icon: '🏭',
    primaryBtn: 'Reject',
  },
]

const chartData = [
  { label: 'W1',  height: 60,  value: 45,  color: '#c8d3d2' },
  { label: 'W2',  height: 100, value: 80,  color: '#4a6e6b' },
  { label: 'W3',  height: 140, value: 120, color: '#b94a3b' },
  { label: 'W4',  height: 80,  value: 65,  color: '#c8d3d2' },
  { label: 'W5',  height: 110, value: 95,  color: '#4a6e6b' },
  { label: 'W6',  height: 120, value: 100, color: '#c8d3d2' },
  { label: 'W7',  height: 160, value: 140, color: '#b94a3b' },
  { label: 'W8',  height: 70,  value: 55,  color: '#4a6e6b' },
  { label: 'W9',  height: 50,  value: 35,  color: '#c8d3d2' },
  { label: 'W10', height: 90,  value: 75,  color: '#b94a3b' },
]

const deadlines = [
  { month: 'OCT', day: '05', title: 'FinTech Summit Applications',  sub: 'Closing in 12 hours' },
  { month: 'OCT', day: '08', title: 'Data Science Mock Interview',  sub: 'Auditorium C • 10:00 AM' },
  { month: 'OCT', day: '12', title: 'GlobalLink On-Campus Drive',   sub: 'Technical Round 1' },
]

// ── Handlers ────────────────────────────────
function handlePrimary(item)       { alert(`Action: ${item.primaryBtn} → ${item.name}`) }
function handleApprove(item)       { alert(`Approved: ${item.name}`) }
function handleViewAll()           { alert('Navigate to all pending requests') }
function handleExport()            { alert('Exporting data…') }
function handleCalendar()          { alert('Open full calendar') }
function handleNotifications()     { alert('Open notifications panel') }
function handleSettings()          { alert('Open settings') }
async function handleLogout() {
  try {
    const token = localStorage.getItem('access_token')
    await fetch('http://localhost:5555/api/auth/logout', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
  } catch (err) {
    console.error('Logout API error:', err)
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

/* Layout */
.admin-layout {
  display: flex;
  height: 100vh;
  background: #f5f5f0;
  overflow: hidden;
}

/* Main area */
.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 28px 28px 40px;
  display: flex;
  flex-direction: column;
  gap: 22px;
}

/* Bottom two-column grid */
.bottom-grid {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 20px;
  align-items: start;
}

.left-col,
.right-col {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Post drive btn styled for placement in slot */
.post-drive-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: #b94a3b;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 11px 0;
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 12px;
  transition: background 0.18s, transform 0.15s;
  width: 100%;
}

.post-drive-btn:hover {
  background: #a03a2c;
  transform: translateY(-1px);
}

/* Scrollbar */
.main-content::-webkit-scrollbar        { width: 6px; }
.main-content::-webkit-scrollbar-track  { background: #f0f4f3; }
.main-content::-webkit-scrollbar-thumb  { background: #c0d4d0; border-radius: 4px; }
</style>