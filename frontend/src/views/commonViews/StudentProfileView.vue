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
        
        <!-- ─── PROFILE HEADER CARD ─── -->
        <div class="header-card">
          <div class="header-left">
            <div class="avatar-wrapper">
              <img :src="profile.avatar" alt="Student Profile Picture" class="avatar-img" />
            </div>

            <div class="meta-wrapper">
              <h1 class="profile-name">{{ profile.name }}</h1>
              <span class="profile-handle">@{{ profile.username }}</span>

              <!-- Header Badges -->
              <div class="badges-row">
                <span class="profile-badge badge-branch">{{ profile.branchCode }}</span>
                <span :class="['profile-badge', profile.status === 'Blacklisted' ? 'badge-status-expired' : 'badge-status-active']">
                  {{ profile.status }}
                </span>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="header-actions">
            <button @click="shareProfileLink" class="btn-share" title="Share Profile Link">
              <i class="bi bi-share"></i>
            </button>
          </div>
        </div>

        <!-- ─── MAIN CONTENT BODY (2 COLUMNS) ─── -->
        <div class="profile-body-grid">
          
          <!-- LEFT COLUMN: Personal Info & Academic Details -->
          <div class="body-col-left">
            
            <!-- Personal Information Card -->
            <div class="content-card info-card">
              <div class="card-header">
                <i class="bi bi-person-circle card-header-icon"></i>
                <h2 class="card-title">Personal Information</h2>
              </div>

              <div class="info-rows-grid">
                <div class="info-cell">
                  <span class="cell-label">Full Name</span>
                  <div class="cell-value">{{ profile.name }}</div>
                </div>

                <div class="info-cell">
                  <span class="cell-label">Email Address</span>
                  <div class="cell-value">{{ profile.email }}</div>
                </div>

                <div class="info-cell">
                  <span class="cell-label">Username</span>
                  <div class="cell-value">@{{ profile.username }}</div>
                </div>

                <div class="info-cell">
                  <span class="cell-label">Phone Number</span>
                  <div class="cell-value">{{ profile.phone }}</div>
                </div>
              </div>
            </div>

            <!-- Academic Details Card -->
            <div class="content-card info-card">
              <div class="card-header">
                <i class="bi bi-mortarboard card-header-icon"></i>
                <h2 class="card-title">Academic Details</h2>
              </div>

              <div class="academic-blocks-grid">
                <!-- Roll Number Box -->
                <div class="academic-box">
                  <span class="academic-box-label">Roll Number</span>
                  <div class="academic-box-value">{{ profile.rollNumber }}</div>
                </div>

                <!-- Branch Box -->
                <div class="academic-box">
                  <span class="academic-box-label">Branch</span>
                  <div class="academic-box-value">{{ profile.branch }}</div>
                </div>

                <!-- Year of Study Box -->
                <div class="academic-box">
                  <span class="academic-box-label">Year of Study</span>
                  <div class="academic-box-value">{{ profile.yearOfStudy }}</div>
                </div>

                <!-- CGPA Box -->
                <div class="academic-box cgpa-box">
                  <span class="academic-box-label">CGPA</span>
                  <div class="academic-box-value cgpa-val">
                    {{ profile.cgpa }} <span class="cgpa-denominator">/ {{ profile.cgpaMax }}</span>
                  </div>
                </div>
              </div>
            </div>

          </div>

          <!-- RIGHT COLUMN: Documents & Core Competencies -->
          <div class="body-col-right">
            
            <!-- Documents Card -->
            <div class="content-card info-card">
              <div class="card-header">
                <i class="bi bi-folder card-header-icon"></i>
                <h2 class="card-title">Documents</h2>
              </div>

              <!-- Documents List Container -->
              <div class="documents-list">
                <!-- Individual Document -->
                <div v-for="doc in profile.documents" :key="doc.id" class="doc-row">
                  <div class="doc-details">
                    <div class="doc-icon-box" :class="doc.iconTheme">
                      <i :class="doc.iconClass"></i>
                    </div>
                    <div class="doc-meta">
                      <span class="doc-name">{{ doc.name }}</span>
                      <span class="doc-update-info">{{ doc.statusMessage }}</span>
                    </div>
                  </div>
                  <a :href="doc.url" target="_blank" class="doc-view-action" @click.prevent="viewDoc(doc.name)">
                    View <i class="bi bi-box-arrow-up-right"></i>
                  </a>
                </div>
              </div>
            </div>

            <!-- Core Competencies Card -->
            <div class="content-card info-card">
              <div class="card-header">
                <i class="bi bi-list-stars card-header-icon"></i>
                <h2 class="card-title">Core Competencies</h2>
              </div>

              <div class="competencies-container">
                <div v-for="(comp, idx) in profile.competencies" :key="idx" class="comp-badge">
                  <span>{{ comp }}</span>
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

// Student Profile Reactive State
const profile = reactive({
  name: 'Alex Rivera',
  username: 'alex_rivera_2024',
  email: 'alex.rivera@university.edu',
  phone: '+1 (555) 123-4567',
  avatar: '/alex_rivera_profile.png',
  branchCode: 'Computer Science',
  status: 'Active Placement',
  rollNumber: 'CS2024-042',
  branch: 'CS & Engineering',
  yearOfStudy: 'Final Year',
  cgpa: '9.2',
  cgpaMax: '10.0',
  competencies: ['React.js', 'Tailwind CSS', 'Python', 'System Design', 'Agile'],
  documents: [
    {
      id: 'resume',
      name: 'Resume',
      statusMessage: 'Last updated 2 days ago',
      iconClass: 'bi bi-file-earmark-text-fill',
      iconTheme: 'theme-pdf',
      url: '#'
    },
    {
      id: 'transcript',
      name: 'Academic Transcript',
      statusMessage: 'Verified by Dean',
      iconClass: 'bi bi-file-earmark-check-fill',
      iconTheme: 'theme-transcript',
      url: '#'
    }
  ]
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
        activeNav.value = 'Students'
      } else if (currentUser.value.role === 'student') {
        activeNav.value = 'Profile'
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

  const routeUserId = route.params.userid
  const loggedInStudentId = currentUser.value?.id

  // If we are looking at another student profile (e.g. dynamic userid param doesn't match login)
  if (routeUserId && String(routeUserId) !== String(loggedInStudentId)) {
    try {
      const token = localStorage.getItem('access_token')
      const res = await fetch('http://localhost:5555/admin/all-students', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (res.ok) {
        const allStudents = await res.json()
        const matchedStudent = allStudents.find(s => String(s.user_id) === String(routeUserId) || String(s.id) === String(routeUserId))
        if (matchedStudent) {
          profile.name = matchedStudent.name || 'Student'
          profile.email = matchedStudent.email || ''
          profile.phone = '+1 (555) 123-4567'
          profile.rollNumber = matchedStudent.roll_number || 'N/A'
          profile.branch = matchedStudent.branch || 'N/A'
          profile.yearOfStudy = matchedStudent.year_of_study != null ? `Year ${matchedStudent.year_of_study}` : 'N/A'
          profile.cgpa = matchedStudent.cgpa != null ? String(matchedStudent.cgpa) : 'N/A'
          profile.username = matchedStudent.email ? matchedStudent.email.split('@')[0] : 'student'
          
          if (matchedStudent.resume) {
            const resumeIdx = profile.documents.findIndex(d => d.id === 'resume')
            if (resumeIdx !== -1) {
              profile.documents[resumeIdx].url = matchedStudent.resume
              profile.documents[resumeIdx].statusMessage = 'Verified PDF resume'
            } else {
              profile.documents.push({
                id: 'resume',
                name: 'Resume',
                statusMessage: 'Verified PDF resume',
                iconClass: 'bi bi-file-earmark-text-fill',
                iconTheme: 'theme-pdf',
                url: matchedStudent.resume
              })
            }
          }
          profile.branchCode = matchedStudent.branch || 'Computer Science'
          profile.status = matchedStudent.isBlacklisted ? 'Blacklisted' : 'Active Placement'
        } else {
          triggerToast('Student profile not found.')
        }
      } else {
        triggerToast('Failed to fetch student details from server.')
      }
    } catch (err) {
      console.error('Error fetching student details:', err)
      triggerToast('Error loading student profile data.')
    }
  } else {
    // Viewing own student profile
    if (currentUser.value) {
      if (currentUser.value.name) profile.name = currentUser.value.name
      if (currentUser.value.username) profile.username = currentUser.value.username
      if (currentUser.value.email) profile.email = currentUser.value.email
    }

    // Load custom frontend profile modifications if they exist locally
    const localSavedData = localStorage.getItem('student_profile_data')
    if (localSavedData) {
      try {
        const parsedData = JSON.parse(localSavedData)
        Object.assign(profile, parsedData)
      } catch (e) {
        console.error('Failed to parse locally saved profile details:', e)
      }
    }
  }
})

// Share profile link helper
const shareProfileLink = () => {
  const dummyUrl = `${window.location.origin}/student/profile/${profile.username}`
  navigator.clipboard.writeText(dummyUrl).then(() => {
    triggerToast('Profile link copied to clipboard!')
  }).catch(() => {
    triggerToast('Clipboard copy failed.')
  })
}

// Simulated doc review click
const viewDoc = (docName) => {
  triggerToast(`Opening: ${docName}...`)
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

/* ────────────────────────────────────────────────────────
   ─── HEADER CARD STYLING ───
──────────────────────────────────────────────────────── */
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

/* Avatar container */
.avatar-wrapper {
  position: relative;
  width: 120px;
  height: 120px;
}

.avatar-img {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 16px;
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
  font-size: 26px;
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
}

.profile-badge {
  padding: 4px 12px;
  border-radius: 100px;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
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

/* Header actions */
.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-share {
  background-color: #ffffff;
  border: 1px solid #ced4da;
  color: #495057;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 15px;
  transition: all 0.2s ease;
}

.btn-share:hover {
  background-color: #f8f9fa;
  color: #27231E;
  border-color: #adb5bd;
  transform: translateY(-1px);
}

.btn-share:active {
  transform: translateY(0);
}

/* ────────────────────────────────────────────────────────
   ─── MAIN SECTION BODY STYLING ───
──────────────────────────────────────────────────────── */
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

/* ────────────────────────────────────────────────────────
   ─── PERSONAL INFORMATION CARD ───
──────────────────────────────────────────────────────── */
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

/* ────────────────────────────────────────────────────────
   ─── ACADEMIC DETAILS CARD ───
──────────────────────────────────────────────────────── */
.academic-blocks-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.academic-box {
  background-color: #FAF4F0; /* Soft warm light cream block */
  border-radius: 8px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 12px;
  border: 1px solid rgba(224, 122, 95, 0.05);
  transition: transform 0.25s, box-shadow 0.25s;
}

.academic-box:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(224, 122, 95, 0.08);
}

.academic-box-label {
  font-size: 11.5px;
  font-weight: 600;
  text-transform: capitalize;
  color: #8c8985;
  letter-spacing: 0.2px;
}

.academic-box-value {
  font-size: 15px;
  font-weight: 700;
  color: #3A5253;
  line-height: 1.3;
}

.cgpa-val {
  color: #8e3b2e; /* Reddish theme tone for CGPA */
}

.cgpa-denominator {
  font-size: 12.5px;
  font-weight: 500;
  color: #8c8985;
}

/* ────────────────────────────────────────────────────────
   ─── DOCUMENTS CARD STYLING ───
──────────────────────────────────────────────────────── */
.documents-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.doc-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #ffffff;
  border: 1px solid #f1ece8;
  border-radius: 12px;
  padding: 16px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.doc-row:hover {
  border-color: rgba(129, 178, 154, 0.4);
  box-shadow: 0 3px 10px rgba(0,0,0,0.02);
}

.doc-details {
  display: flex;
  align-items: center;
  gap: 16px;
}

.doc-icon-box {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.theme-pdf {
  background-color: #fce8e6;
  color: #c53929;
}

.theme-transcript {
  background-color: #e6f4f3;
  color: #00796b;
}

.theme-word {
  background-color: #e8f0fe;
  color: #1a73e8;
}

.theme-other {
  background-color: #f1f3f4;
  color: #5f6368;
}

.doc-meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.doc-name {
  font-size: 14.5px;
  font-weight: 700;
  color: #27231E;
}

.doc-update-info {
  font-size: 11.5px;
  color: #8c8985;
}

.doc-view-action {
  font-size: 13px;
  font-weight: 600;
  color: #2d6b5e;
  text-decoration: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  border-radius: 6px;
  transition: all 0.2s;
}

.doc-view-action:hover {
  background-color: #e8f4f1;
  color: #1b443b;
}

/* ────────────────────────────────────────────────────────
   ─── CORE COMPETENCIES CARD ───
──────────────────────────────────────────────────────── */
.competencies-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.comp-badge {
  background-color: #FAF4F0;
  border: 1px solid rgba(224, 122, 95, 0.1);
  border-radius: 100px;
  padding: 6px 14px;
  font-size: 13px;
  font-weight: 500;
  color: #8e3b2e;
  display: inline-flex;
  align-items: center;
  transition: all 0.2s ease;
}

.comp-badge:hover {
  transform: scale(1.02);
}

/* ────────────────────────────────────────────────────────
   ─── RESPONSIVE RULES ───
──────────────────────────────────────────────────────── */
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

  .academic-blocks-grid {
    grid-template-columns: repeat(2, 1fr);
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

  .academic-blocks-grid {
    grid-template-columns: 1fr;
  }
}
</style>
