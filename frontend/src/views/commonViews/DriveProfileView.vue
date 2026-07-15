<template>
  <div class="admin-layout">
    
    <!-- Sidebar -->
    <Sidebar
      v-model="activeNav"
      :nav-items="navItems"
      logo-img="/Only_logo.png"
      :title="sidebarTitle"
      :subtitle="sidebarSubtitle"
      @logout="handleLogout"
    />

    <!-- Main Content Area -->
    <main class="main-content">
      
      <!-- Custom Animated Toast Notification -->
      <div :class="['toast-alert', { 'toast-show': showToastActive }]">
        <div class="toast-content">
          <i class="bi bi-check-circle-fill toast-success-icon"></i>
          <span class="toast-message">{{ toastMessage }}</span>
        </div>
      </div>

      <!-- Profile Container -->
      <div class="profile-container">
        
        <!-- PROFILE HEADER CARD -->
        <div class="header-card">
          <div class="header-left">
            <div class="avatar-wrapper">
              
              <div class="drive-logo-fallback">
                <i class="bi bi-megaphone"></i>
              </div>
            </div>

            <div class="meta-wrapper">
              <h1 class="profile-name">{{ drive.title }}</h1>
              <span class="profile-handle">{{ drive.company_name }} · {{ drive.company_industry }}</span>

              <!-- Header Badges -->
              <div class="badges-row">
                <span class="profile-badge badge-branch">{{ drive.location }} ({{ drive.workMode }})</span>
                <span :class="['profile-badge', isExpired(drive.deadline) ? 'badge-status-expired' : 'badge-status-active']">
                  {{ isExpired(drive.deadline) ? 'Deadline Expired' : 'Active Drive' }}
                </span>
                <span :class="['profile-badge', drive.approved ? 'badge-status-approved' : 'badge-status-pending']">
                  {{ drive.approved ? 'Approved' : 'Unapproved' }}
                </span>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="header-actions">
            <!-- Student Apply Actions -->
            <template v-if="currentUser?.role === 'student'">
              <span v-if="drive.applied" class="badge-status-applied-large">
                <i class="bi bi-check-circle-fill"></i> Applied
              </span>
              <span v-else-if="isExpired(drive.deadline)" class="badge-disabled-large">
                Closed
              </span>
              <span v-else-if="drive.isBlacklisted" class="badge-disabled-large" title="Account locked by admin.">
                Locked
              </span>
              <button v-else @click="applyToThisDrive" class="btn-apply-large" :disabled="applying">
                <span v-if="applying">Applying...</span>
                <span v-else><i class="bi bi-send-fill"></i> Apply Now</span>
              </button>
            </template>

            <button @click="goBack" class="btn-back" title="Go Back">
              <i class="bi bi-arrow-left"></i> Back
            </button>
          </div>
        </div>

        <!--MAIN CONTENT BODY-->
        <div class="profile-body-grid">
          
          <!--Criteria & Academic Details, Job Details -->
          <div class="body-col-left">
            
            <!-- Criteria & Eligibility Card -->
            <div class="content-card info-card">
              <div class="card-header">
                <i class="bi bi-clipboard-check card-header-icon"></i>
                <h2 class="card-title">Eligibility & Criteria</h2>
              </div>

              <div class="info-rows-grid">
                <div class="info-cell">
                  <span class="cell-label">Academic Eligibility</span>
                  <div class="cell-value">{{ drive.eligibility }}</div>
                </div>

                <div class="info-cell">
                  <span class="cell-label">Eligible Branches</span>
                  <div class="cell-value">{{ drive.branches }}</div>
                </div>

                <div class="info-cell">
                  <span class="cell-label">Target Batch</span>
                  <div class="cell-value">{{ drive.batch }}</div>
                </div>

                <div class="info-cell">
                  <span class="cell-label">Pay Scale (CTC)</span>
                  <div class="cell-value pay-highlight">{{ drive.payScale }}</div>
                </div>
              </div>
            </div>

            <!-- Job Specific Details Card -->
            <div class="content-card info-card">
              <div class="card-header">
                <i class="bi bi-briefcase card-header-icon"></i>
                <h2 class="card-title">Job Specifics</h2>
              </div>

              <div class="info-rows-grid">
                <div class="info-cell">
                  <span class="cell-label">Open Positions</span>
                  <div class="cell-value">{{ drive.positions }} vacancies</div>
                </div>

                <div class="info-cell">
                  <span class="cell-label">Location</span>
                  <div class="cell-value">{{ drive.location }}</div>
                </div>

                <div class="info-cell">
                  <span class="cell-label">Work Mode</span>
                  <div class="cell-value">{{ drive.workMode }}</div>
                </div>

                <div class="info-cell">
                  <span class="cell-label">Application Deadline</span>
                  <div :class="['cell-value', { 'text-danger-txt': isExpired(drive.deadline) }]">
                    {{ formatDate(drive.deadline) }}
                    <span class="expired-inline" v-if="isExpired(drive.deadline)">(Expired)</span>
                  </div>
                </div>
              </div>
            </div>

          </div>

          <!--About and Skills -->
          <div class="body-col-right">
            
            <!-- Description Card -->
            <div class="content-card info-card">
              <div class="card-header">
                <i class="bi bi-info-circle card-header-icon"></i>
                <h2 class="card-title">Job Description</h2>
              </div>
              <div class="drive-description-box">
                <p class="drive-desc-txt">{{ drive.description }}</p>
              </div>
            </div>

            <!-- Process & Required Skills Card -->
            <div class="content-card info-card">
              <div class="card-header">
                <i class="bi bi-list-stars card-header-icon"></i>
                <h2 class="card-title">Requirements & Process</h2>
              </div>

              <div class="info-vertical-stack">
                <div class="info-stack-cell">
                  <span class="cell-label">Skills Required</span>
                  <div class="cell-value-list">{{ drive.skillsRequired }}</div>
                </div>

                <div class="info-stack-cell pt-12">
                  <span class="cell-label">Selection Rounds</span>
                  <div class="cell-value-list">{{ drive.interviewRounds }}</div>
                </div>
              </div>
            </div>

          </div>

        </div>

      </div>
      
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'

// Toast Messaging System
const toastMessage = ref('')
const showToastActive = ref(false)
let toastTimeout = null

const triggerToast = (msg) => {
  toastMessage.value = msg
  showToastActive.value = true
  if (toastTimeout) clearTimeout(toastTimeout)
  toastTimeout = setTimeout(() => {
    showToastActive.value = false
  }, 3500)
}

// Drive Reactive State
const drive = reactive({
  title: 'Graduate Engineer Trainee',
  company_name: 'NexusTech Solutions',
  company_industry: 'Cloud Infrastructure',
  status: 'Approved',
  approved: false,
  deadline: '2026-07-30',
  payScale: '12 LPA',
  positions: 5,
  location: 'Bangalore, India',
  workMode: 'Hybrid',
  eligibility: 'CGPA >= 8.0, CSE/IT students only',
  batch: '2026 Graduating Batch',
  branches: 'CSE, IT, ECE',
  skillsRequired: 'Python, Node.js, SQL, REST APIs',
  interviewRounds: 'Resume Shortlisting -> Online Test -> Technical Round -> HR Round',
  description: 'We are looking for self-driven engineering interns to join our cloud virtualization development squad. You will assist in writing enterprise APIs, database indexing operations, and serverless architectures.',
  applied: false,
  isBlacklisted: false
})

// Route and User Access computed controls
const route = useRoute()
const router = useRouter()
const currentUser = ref(null)

// Sidebar and layout configuration same as AdminDashView
const activeNav = ref('')
const sidebarTitle = ref('LaunchPad')

const sidebarSubtitle = computed(() => {
  if (!currentUser.value) return 'Portal Console'
  if (currentUser.value.role === 'admin') return 'Admin Console'
  if (currentUser.value.role === 'recruiter') return 'Recruiter Console'
  return 'Student Console'
})

const navItems = computed(() => {
  if (!currentUser.value) return []
  if (currentUser.value.role === 'admin') {
    return [
      { label: 'Dashboard',        icon: '' },
      { label: 'Students',         icon: '' },
      { label: 'Companies',        icon: '' },
      { label: 'Placement Drives', icon: '' },
      { label: 'Applications',     icon: '' },
    ]
  } else if (currentUser.value.role === 'recruiter') {
    return [
      { label: 'Dashboard',        icon: '' }
    ]
  } else {
    return [
      { label: 'Dashboard',        icon: '' },
      { label: 'Profile',          icon: '' }
    ]
  }
})

let isInitialized = false

watch(activeNav, (newVal) => {
  if (!isInitialized) return
  if (!currentUser.value) return
  if (currentUser.value.role === 'admin') {
    if (newVal === 'Dashboard') router.push('/admin/dashboard')
    else if (newVal === 'Students') router.push('/admin/students')
    else if (newVal === 'Companies') router.push('/admin/companies')
    else if (newVal === 'Placement Drives') router.push('/admin/drives')
    else if (newVal === 'Applications') router.push('/admin/applications')
  } else if (currentUser.value.role === 'recruiter') {
    if (newVal === 'Dashboard') router.push('/company/dashboard')
  } else {
    if (newVal === 'Dashboard') router.push('/student/dashboard')
    else if (newVal === 'Profile') router.push(`/student/profile/${currentUser.value.id}`)
  }
})

// Logout handler
const handleLogout = async () => {
  try {
    const token = localStorage.getItem('access_token')
    await fetch('http://localhost:5555/api/auth/logout', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
  } catch (err) {
    console.error('Logout error:', err)
  } finally {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    router.push('/login')
  }
}

onMounted(async () => {
  // Load current logged in user info
  const userJson = localStorage.getItem('user')
  if (userJson) {
    try {
      currentUser.value = JSON.parse(userJson)
      // Set active nav highlight
      if (currentUser.value.role === 'admin') {
        activeNav.value = 'Placement Drives'
      } else if (currentUser.value.role === 'student') {
        activeNav.value = ''
      } else if (currentUser.value.role === 'recruiter') {
        activeNav.value = 'Dashboard'
      }
    } catch (e) {
      console.warn('Failed to parse logged-in user:', e)
    }
  }

  // Set isInitialized on next tick to avoid redirection loop during setup
  setTimeout(() => {
    isInitialized = true
  }, 150)

  const routeDriveId = route.params.driveid
  
  if (routeDriveId) {
    try {
      const token = localStorage.getItem('access_token')
      const res = await fetch(`http://localhost:5555/common/drive/profile/${routeDriveId}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (res.ok) {
        const driveData = await res.json()
        drive.title = driveData.title || 'Placement Drive'
        drive.company_name = driveData.company_name || 'Associated Corporate'
        drive.company_industry = driveData.company_industry || 'Information Technology'
        drive.status = driveData.status || 'Pending'
        drive.approved = driveData.approved ?? false
        drive.deadline = driveData.deadline || ''
        drive.payScale = driveData.payScale || 'N/A'
        drive.positions = driveData.positions ?? 0
        drive.location = driveData.location || 'N/A'
        drive.workMode = driveData.workMode || 'On-site'
        drive.eligibility = driveData.eligibility || 'N/A'
        drive.batch = driveData.batch || 'N/A'
        drive.branches = driveData.branches || 'N/A'
        drive.skillsRequired = driveData.skillsRequired || 'N/A'
        drive.interviewRounds = driveData.interviewRounds || 'N/A'
        drive.description = driveData.description || 'No detailed job description provided.'
        drive.applied = driveData.applied ?? false
        drive.isBlacklisted = driveData.isBlacklisted ?? false
      } else {
        triggerToast('Failed to fetch drive details from server.')
      }
    } catch (err) {
      console.error('Error fetching drive details:', err)
      triggerToast('Error loading drive details data.')
    }
  }
})

// Back navigation helper
const goBack = () => {
  router.back()
}

const applying = ref(false)

const applyToThisDrive = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) return
  
  applying.value = true
  try {
    const res = await fetch(`http://localhost:5555/api/student/apply/${route.params.driveid}`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await res.json()
    if (!res.ok) {
      triggerToast(data.message || 'Failed to apply.')
      return
    }
    triggerToast('Successfully applied to placement drive!')
    drive.applied = true
  } catch (err) {
    console.error(err)
    triggerToast('Network error while applying.')
  } finally {
    applying.value = false
  }
}

const isExpired = (deadlineStr) => {
  if (!deadlineStr) return false
  return new Date(deadlineStr) < new Date()
}

const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('en-IN', {
    year: 'numeric', month: 'short', day: 'numeric'
  })
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Layout same as AdminDashView */
.admin-layout {
  display: flex;
  height: 100vh;
  background: #f5f5f0;
  overflow: hidden;
  font-family: 'Inter', system-ui, sans-serif;
  color: var(--brand-dark, #27231E);
  width: 100vw;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 28px 28px 40px;
}

.profile-container {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Custom Success Toast Styling */
.toast-alert {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background-color: #27231E;
  color: #ffffff;
  border-radius: 12px;
  padding: 14px 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  transform: translateY(120px);
  opacity: 0;
  pointer-events: none;
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.3s;
}

.toast-alert.toast-show {
  transform: translateY(0);
  opacity: 1;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.toast-success-icon {
  color: #81B29A;
  font-size: 18px;
}

.toast-message {
  font-size: 14px;
  font-weight: 500;
}


.header-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 24px 32px;
  box-shadow: 0 4px 18px rgba(39, 35, 30, 0.04);
  border: 1px solid rgba(39, 35, 30, 0.05);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  position: relative;
  transition: all 0.3s ease;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

/* Fallback Logo container */
.avatar-wrapper {
  position: relative;
  width: 120px;
  height: 120px;
}

.drive-logo-fallback {
  width: 120px;
  height: 120px;
  border-radius: 16px;
  background-color: #faeae7;
  color: #b94a3b;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.06);
  border: 2px solid #ffffff;
}

/* Profile details (Name, handle, badges) */
.meta-wrapper {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.profile-name {
  font-size: 24px;
  font-weight: 700;
  color: #27231E;
  margin: 0;
  line-height: 1.2;
}

.profile-handle {
  font-size: 14.5px;
  color: #6c757d;
  font-weight: 400;
}

.badges-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  flex-wrap: wrap;
}

.profile-badge {
  padding: 4px 12px;
  border-radius: 100px;
  font-size: 12px;
  font-weight: 600;
}

.badge-branch {
  background-color: #e8f4f1;
  color: #2d6b5e;
}

.badge-status-active {
  background-color: #e6f4ea;
  color: #137333;
}

.badge-status-expired {
  background-color: #fce8e6;
  color: #c5221f;
}

.badge-status-approved {
  background-color: #e6f4ea;
  color: #137333;
}

.badge-status-pending {
  background-color: #fef7e0;
  color: #b06000;
}

/* Header buttons */
.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-back {
  background-color: #ffffff;
  border: 1px solid #ced4da;
  color: #495057;
  padding: 8px 16px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 14.5px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-back:hover {
  background-color: #f8f9fa;
  color: #27231E;
  border-color: #adb5bd;
  transform: translateY(-1px);
}

.btn-back:active {
  transform: translateY(0);
}


.profile-body-grid {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 24px;
  align-items: start;
}

/* Base styling for white cards */
.content-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 28px 32px;
  box-shadow: 0 4px 18px rgba(39, 35, 30, 0.03);
  border: 1px solid rgba(39, 35, 30, 0.04);
  margin-bottom: 24px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid #f3ebe6;
  padding-bottom: 16px;
  margin-bottom: 24px;
}

.card-header-icon {
  font-size: 20px;
  color: #3A5253;
}

.card-title {
  font-size: 18px;
  font-weight: 700;
  color: #27231E;
  margin: 0;
}


.info-rows-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.info-cell {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.cell-label {
  font-size: 12.5px;
  font-weight: 500;
  color: #8c8985;
  text-transform: capitalize;
}

.cell-value {
  font-size: 15px;
  font-weight: 500;
  color: #27231E;
}

.pay-highlight {
  color: #c53929; /* Red highlight CTC */
  font-weight: 700 !important;
}

.text-danger-txt {
  color: #b91c1c;
}

.expired-inline {
  font-size: 11px;
  color: #b91c1c;
  margin-left: 6px;
  font-weight: 600;
}

/* Description Text */
.drive-desc-txt {
  font-size: 14.5px;
  line-height: 1.6;
  color: #495057;
}

/* Vertical info stack for required skills */
.info-vertical-stack {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-stack-cell {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.pt-12 {
  padding-top: 12px;
  border-top: 1px dashed #f3ebe6;
}

.cell-value-list {
  font-size: 14.5px;
  line-height: 1.5;
  color: #27231E;
  font-weight: 500;
}


@media (max-width: 992px) {
  .profile-body-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .content-card {
    padding: 24px;
  }
}

@media (max-width: 768px) {
  .header-card {
    flex-direction: column;
    align-items: flex-start;
    padding: 24px;
  }
  
  .header-actions {
    width: 100%;
    justify-content: flex-end;
    margin-top: 10px;
    border-top: 1px solid #f1f0ee;
    padding-top: 16px;
  }
}

@media (max-width: 576px) {
  .header-left {
    flex-direction: column;
    align-items: center;
    text-align: center;
    width: 100%;
  }

  .badges-row {
    justify-content: center;
  }

  .info-rows-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}

/* Apply / Status Large Badges and Buttons */
.btn-apply-large {
  background: #2d6b5e;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 8px 18px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, transform 0.15s;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.btn-apply-large:hover {
  background: #235349;
  transform: translateY(-1px);
}
.btn-apply-large:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.badge-status-applied-large {
  font-size: 13.5px;
  font-weight: 600;
  color: #2d6b5e;
  background: #e8f4f1;
  padding: 6px 14px;
  border-radius: 8px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 1px solid #c9e6df;
}

.badge-disabled-large {
  font-size: 13.5px;
  font-weight: 600;
  color: #6b7280;
  background: #f3f4f6;
  padding: 6px 14px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}
</style>
