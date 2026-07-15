<template>
  <div class="admin-layout">
    <!--Sidebar-->
    <Sidebar
      v-model="activeNav"
      :nav-items="navItems"
      logo-img="/Only_logo.png"
      title="LaunchPad"
      subtitle="Admin Console"
      @logout="handleLogout"
    />

    <!-- Main Content-->
    <main class="main-content">
      <!-- Top Bar -->
      <AdminTopbar
        title="Student Management"
        v-model="searchQuery"
      />

      <!-- Stats Cards (2 Cards only) -->
      <section class="stat-cards">
        <div class="stat-card">
          <div class="stat-top">
            <div class="stat-icon total-students-icon"><i class="bi bi-mortarboard"></i></div>
          </div>
          <div class="stat-label">Total Students</div>
          <div class="stat-value">{{ filteredStudents.length }}</div>
        </div>

        <div class="stat-card">
          <div class="stat-top">
            <div class="stat-icon blacklisted-icon"><i class="bi bi-slash-circle"></i></div>
          </div>
          <div class="stat-label">Blacklisted Students</div>
          <div class="stat-value">{{ blacklistedCount }}</div>
        </div>
      </section>

      <!-- Student Data Table Section -->
      <section class="card table-card">
        <div class="table-header">
          <div class="table-title-group">
            <h2 class="table-title">All Registered Students</h2>
            <p class="table-subtitle">View student details, verify active status and manage blacklist constraints.</p>
          </div>
        </div>

        <div class="table-wrapper">
          <table class="students-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Branch</th>
                <th>Application</th>
                <th class="text-center">Profile</th>
                <th class="text-center">Blacklist / Whitelist Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in filteredStudents" :key="student.id">
                <td class="student-name">
                  <div class="name-wrapper">
                    <span class="avatar-fallback">{{ student.name ? student.name.charAt(0) : 'S' }}</span>
                    <div class="name-info">
                      <span class="full-name">{{ student.name }}</span>
                      <span class="roll-subtext">{{ student.roll_number }}</span>
                    </div>
                  </div>
                </td>
                <td class="email-cell">{{ student.email }}</td>
                <td><span class="badge-branch">{{ student.branch }}</span></td>
                <td>
                  <span class="badge-apps" :class="{ 'has-apps': student.applications && student.applications.length > 0 }">
                    {{ student.applications ? student.applications.length : 0 }} applied
                  </span>
                </td>
                <td class="text-center">
                  <button class="btn-profile" @click="viewProfile(student)">View Profile</button>
                </td>
                <td class="text-center">
                  <div class="status-toggle-wrapper">
                    <span :class="['status-text-badge', student.isBlacklisted ? 'status-blacklisted' : 'status-whitelisted']">
                      {{ student.isBlacklisted ? 'Blacklisted' : 'Whitelisted' }}
                    </span>
                    <!-- Custom Switch Toggle -->
                    <label class="switch">
                      <input 
                        type="checkbox" 
                        :checked="!student.isBlacklisted"
                        @change="toggleStatus(student)"
                      />
                      <span class="slider round"></span>
                    </label>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredStudents.length === 0">
                <td colspan="6" class="empty-state">
                  <div class="empty-title">No students found</div>
                  <p class="empty-description">Try adjusting your search criteria to find registered students.</p>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Student Profile Modal -->
      <Teleport to="body">
        <div class="modal-overlay" v-if="showProfileModal" @click.self="showProfileModal = false">
          <div class="modal">
            <div class="modal-header">
              <span class="modal-logo-fallback">{{ selectedStudent?.name.charAt(0) }}</span>
              <div>
                <h3 class="modal-title">{{ selectedStudent?.name }}</h3>
                <span class="modal-subtitle">Roll Number: {{ selectedStudent?.roll_number || 'N/A' }}</span>
              </div>
            </div>
            <div class="modal-body">
              <div class="info-row">
                <span class="info-label">Email:</span>
                <span class="info-value">{{ selectedStudent?.email || 'N/A' }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">Branch:</span>
                <span class="info-value">{{ selectedStudent?.branch || 'N/A' }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">Year of Study:</span>
                <span class="info-value">{{ selectedStudent?.year_of_study != null ? 'Year ' + selectedStudent.year_of_study : 'N/A' }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">CGPA:</span>
                <span class="info-value">{{ selectedStudent?.cgpa != null ? selectedStudent.cgpa.toFixed(2) : 'N/A' }}</span>
              </div>
              <div class="info-row" v-if="selectedStudent?.resume">
                <span class="info-label">Resume:</span>
                <a :href="selectedStudent?.resume" target="_blank" class="info-value link-style">
                  📄 View Resume PDF
                </a>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn-close" @click="showProfileModal = false">Close</button>
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
const activeNav = ref('Students')
const searchQuery = ref('')
const showProfileModal = ref(false)
const selectedStudent = ref(null)

const students = ref([])
const errorMsg = ref('')
const loading = ref(false)

// Sidebar navigation items
const navItems = [
  { label: 'Dashboard',        icon: '<i class="bi bi-speedometer2"></i>' },
  { label: 'Students',         icon: '<i class="bi bi-people"></i>' },
  { label: 'Companies',        icon: '<i class="bi bi-building"></i>' },
  { label: 'Placement Drives', icon: '<i class="bi bi-megaphone"></i>' },
  { label: 'Applications',     icon: '<i class="bi bi-file-earmark-text"></i>' },
  { label: 'Report',           icon: '<i class="bi bi-file-earmark-bar-graph"></i>' }
]

// Handle routing from generic sidebar
watch(activeNav, (newVal) => {
  if (newVal === 'Dashboard') {
    router.push('/admin/dashboard')
  } else if (newVal === 'Students') {
    router.push('/admin/students')
  } else if (newVal === 'Companies') {
    router.push('/admin/companies')
  } else if (newVal === 'Placement Drives') {
    router.push('/admin/drives')
  } else if (newVal === 'Applications') {
    router.push('/admin/applications')
  } else if (newVal === 'Report') {
    router.push('/admin/reports')
  }
})

// Fetch Student details from API
let searchTimeout = null

watch(searchQuery, (newQuery) => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchStudents(newQuery)
  }, 300)
})

// Fetch Student details from API
async function fetchStudents(q = '') {
  loading.value = true
  try {
    const token = localStorage.getItem('access_token')
    const url = q 
      ? `http://localhost:5555/admin/students/search?q=${encodeURIComponent(q)}` 
      : 'http://localhost:5555/admin/all-students'
      
    const res = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    if (!res.ok) {
      errorMsg.value = 'Failed to load students.'
      return
    }
    const data = await res.json()
    students.value = data
  } catch (err) {
    errorMsg.value = 'Network error. Please try again.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchStudents()
})

// Computed Properties
const filteredStudents = computed(() => {
  return students.value
})

const blacklistedCount = computed(() => {
  return filteredStudents.value.filter(s => s.isBlacklisted).length
})

async function toggleStatus(student) {
  try {
    const token = localStorage.getItem('access_token')
    const res = await fetch(`http://localhost:5555/admin/student/blacklist/${student.user_id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    if (res.ok) {
      student.isBlacklisted = !student.isBlacklisted
    } else {
      console.error('Failed to toggle blacklist status')
    }
  } catch (err) {
    console.error('Error toggling blacklist status:', err)
  }
}

function viewProfile(student) {
  router.push(`/student/profile/${student.user_id}`)
}

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

* {
  font-family: 'Inter', sans-serif;
  box-sizing: border-box;
}

/*Layout*/
.admin-layout {
  display: flex;
  height: 100vh;
  background: #f5f5f0;
  overflow: hidden;
}

/*Main Content*/
.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 28px 28px 40px;
  display: flex;
  flex-direction: column;
  gap: 22px;
}

/*Stat Cards*/
.stat-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  transition: box-shadow 0.2s, transform 0.2s;
}

.stat-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.10);
  transform: translateY(-2px);
}

.stat-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.total-students-icon { background: #e8f4f1; color: #2d6b5e; }
.blacklisted-icon { background: #fdf2f2; color: #e02424; }

.stat-badge {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 20px;
}

.positive-badge { background: #e0f0ec; color: #2d6b5e; }
.neutral-badge { background: #f3f4f6; color: #4b5563; }
.negative-badge { background: #fde8e8; color: #9b1c1c; }

.stat-label {
  font-size: 12.5px;
  color: #8a9e9a;
  font-weight: 500;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1a2e28;
  letter-spacing: -0.5px;
}

/*Card Section*/
.card {
  background: #fff;
  border-radius: 14px;
  padding: 22px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}

.table-card {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-title {
  font-size: 16px;
  font-weight: 700;
  color: #1a2e28;
}

.table-subtitle {
  font-size: 13px;
  color: #8a9e9a;
  margin-top: 4px;
}

/* Table */
.table-wrapper {
  overflow-x: auto;
  border-radius: 10px;
  border: 1px solid #eff3f2;
}

.students-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 13.5px;
}

.students-table th {
  background: #f9fdfb;
  color: #5a7a75;
  font-weight: 600;
  padding: 14px 16px;
  border-bottom: 1.5px solid #eff3f2;
}

.students-table td {
  padding: 14px 16px;
  border-bottom: 1px solid #eff3f2;
  color: #2e3e3b;
  vertical-align: middle;
}

.students-table tr:last-child td {
  border-bottom: none;
}

.students-table tr:hover td {
  background: #fdfdfd;
}

/* Name and Rollwrapper */
.name-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar-fallback {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #e8f4f1;
  color: #2d6b5e;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

.name-info {
  display: flex;
  flex-direction: column;
}

.full-name {
  font-weight: 600;
  color: #1a2e28;
  font-size: 13.5px;
}

.roll-subtext {
  font-size: 11px;
  color: #8a9e9a;
  margin-top: 1px;
}

.email-cell {
  color: #4a6e6b;
  font-size: 13px;
}

/* Branch styling */
.badge-branch {
  background: #f3f4f6;
  color: #374151;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}

/* Applications count badge */
.badge-apps {
  font-size: 12px;
  background: #f3f4f6;
  color: #9ca3af;
  padding: 3px 8px;
  border-radius: 20px;
  font-weight: 500;
}
.badge-apps.has-apps {
  background: #e0f2fe;
  color: #0369a1;
}

/* Profile button */
.btn-profile {
  background: #fff;
  border: 1.5px solid #cdd8d5;
  color: #3a5c55;
  border-radius: 7px;
  padding: 7px 14px;
  font-size: 12.5px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-profile:hover {
  background: #f0f5f4;
  border-color: #4a6e6b;
}

/* Center alignments */
.text-center {
  text-align: center;
}

.status-toggle-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

/* Switch status text badge */
.status-text-badge {
  font-size: 11.5px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 12px;
  min-width: 85px;
  text-align: center;
  transition: all 0.2s ease;
}

.status-whitelisted {
  background: #e6f4ea;
  color: #137333;
}

.status-blacklisted {
  background: #fce8e6;
  color: #c5221f;
}

/*Toggle Switch Styling*/
.switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 22px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #e5e7eb;
  transition: .3s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .3s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
}

/* When checked (i.e. Whitelisted / Active status) */
input:checked + .slider {
  background-color: #10b981;
}

input:focus + .slider {
  box-shadow: 0 0 1px #10b981;
}

input:checked + .slider:before {
  transform: translateX(22px);
}

.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}

/*Empty state*/
.empty-state {
  text-align: center;
  padding: 48px 0 !important;
}


.empty-title {
  font-size: 16px;
  font-weight: 700;
  color: #1a2e28;
}

.empty-description {
  font-size: 13px;
  color: #8a9e9a;
  margin-top: 6px;
}

/*Student Profile Modal*/
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal {
  background: #fff;
  border-radius: 14px;
  padding: 28px 32px;
  width: 100%;
  max-width: 440px;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.18);
  font-family: 'Inter', sans-serif;
}

.modal-header {
  display: flex;
  align-items: center;
  gap: 14px;
  border-bottom: 1px solid #eff3f2;
  padding-bottom: 16px;
  margin-bottom: 18px;
}

.modal-logo-fallback {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: #e8f4f1;
  color: #2d6b5e;
  font-size: 20px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-title {
  font-size: 17px;
  font-weight: 700;
  color: #1a2e28;
}

.modal-subtitle {
  font-size: 12px;
  color: #8a9e9a;
  display: block;
  margin-top: 2px;
}

.modal-body {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.info-row {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 12px;
  font-weight: 600;
  color: #8a9e9a;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 13.5px;
  color: #2e3e3b;
}

.link-style {
  color: #2d6b5e;
  text-decoration: none;
  font-weight: 500;
}
.link-style:hover {
  text-decoration: underline;
}

.modal-footer {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
}

.btn-close {
  background: #253a35;
  color: white;
  border: none;
  border-radius: 7px;
  padding: 8px 20px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}

.btn-close:hover {
  background: #1b2a26;
}

/* Scrollbar styling */
.main-content::-webkit-scrollbar {
  width: 6px;
}
.main-content::-webkit-scrollbar-track {
  background: #f0f4f3;
}
.main-content::-webkit-scrollbar-thumb {
  background: #c0d4d0;
  border-radius: 4px;
}
</style>
