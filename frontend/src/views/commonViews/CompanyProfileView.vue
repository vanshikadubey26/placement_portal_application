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
              <!-- Corporate Office Logo Fallback Icon -->
              <div class="company-logo-fallback">
                <i class="bi bi-building"></i>
              </div>
            </div>

            <div class="meta-wrapper">
              <h1 class="profile-name">{{ profile.name }}</h1>
              <span class="profile-handle">@{{ profile.username }}</span>

              <!-- Header Badges -->
              <div class="badges-row">
                <span class="profile-badge badge-branch">{{ profile.industry }}</span>
                <span :class="['profile-badge', profile.approved ? 'badge-status-active' : 'badge-status-pending']">
                  {{ profile.approved ? 'Verified Partner' : 'Pending Review' }}
                </span>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="header-actions">
            <button @click="goBack" class="btn-back" title="Go Back">
              <i class="bi bi-arrow-left"></i> Back
            </button>
          </div>
        </div>

        <!-- ─── MAIN CONTENT BODY (2 COLUMNS) ─── -->
        <div class="profile-body-grid">
          
          <!-- LEFT COLUMN: Corporate Information & POC Details -->
          <div class="body-col-left">
            
            <!-- Company Information Card -->
            <div class="content-card info-card">
              <div class="card-header">
                <i class="bi bi-building card-header-icon"></i>
                <h2 class="card-title">Corporate Information</h2>
              </div>

              <div class="info-rows-grid">
                <div class="info-cell">
                  <span class="cell-label">Industry Sector</span>
                  <div class="cell-value">{{ profile.industry }}</div>
                </div>

                <div class="info-cell">
                  <span class="cell-label">Head Office</span>
                  <div class="cell-value">{{ profile.headOffice }}</div>
                </div>

                <div class="info-cell">
                  <span class="cell-label">Corporate Scale</span>
                  <div class="cell-value">{{ profile.scale }}</div>
                </div>

                <div class="info-cell">
                  <span class="cell-label">Website URL</span>
                  <div class="cell-value">
                    <a :href="profile.website" target="_blank" class="company-link">
                      {{ profile.website }} <i class="bi bi-box-arrow-up-right"></i>
                    </a>
                  </div>
                </div>
              </div>
            </div>

            <!-- Point of Contact (POC) Card -->
            <div class="content-card info-card">
              <div class="card-header">
                <i class="bi bi-person-badge-fill card-header-icon"></i>
                <h2 class="card-title">Corporate Representative (POC)</h2>
              </div>

              <div class="info-rows-grid">
                <div class="info-cell">
                  <span class="cell-label">Representative Name</span>
                  <div class="cell-value">{{ profile.pocName }}</div>
                </div>

                <div class="info-cell">
                  <span class="cell-label">POC Email</span>
                  <div class="cell-value">{{ profile.pocEmail }}</div>
                </div>

                <div class="info-cell">
                  <span class="cell-label">Official Registry Email</span>
                  <div class="cell-value">{{ profile.email }}</div>
                </div>

                <div class="info-cell">
                  <span class="cell-label">Security Clearance</span>
                  <div class="cell-value">
                    <span :class="['status-text-badge', profile.isBlacklisted ? 'status-blacklisted' : 'status-whitelisted']">
                      {{ profile.isBlacklisted ? 'Blacklisted' : 'Active Account' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

          </div>

          <!-- RIGHT COLUMN: About/Description -->
          <div class="body-col-right">
            
            <!-- About Company Card -->
            <div class="content-card info-card">
              <div class="card-header">
                <i class="bi bi-info-circle card-header-icon"></i>
                <h2 class="card-title">About Company</h2>
              </div>
              <div class="company-description-box">
                <p class="company-desc-txt">{{ profile.description }}</p>
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

// Company Profile Reactive State
const profile = reactive({
  name: 'NexusTech Solutions',
  username: 'nexustech_corp',
  email: 'careers@nexustech.io',
  industry: 'Cloud Infrastructure & Tech',
  approved: true,
  isBlacklisted: false,
  description: 'NexusTech Solutions is a leading provider of virtualized infrastructure, hybrid cloud environments, and secure networking platforms. We specialize in enterprise scale deployment solutions.',
  scale: '1,000 - 5,000 Employees',
  headOffice: 'San Francisco, California',
  website: 'https://nexustech.io',
  pocName: 'Sarah Jenkins',
  pocEmail: 'sjenkins@nexustech.io'
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
        activeNav.value = 'Companies'
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

  const routeCompanyId = route.params.companyid
  
  if (routeCompanyId) {
    try {
      const token = localStorage.getItem('access_token')
      const res = await fetch(`http://localhost:5555/common/company/profile/${routeCompanyId}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (res.ok) {
        const companyData = await res.json()
        profile.name = companyData.name || 'Company'
        profile.email = companyData.email || ''
        profile.industry = companyData.industry || 'Technology Solutions'
        profile.approved = companyData.approved
        profile.isBlacklisted = companyData.isBlacklisted
        profile.username = companyData.username || (companyData.name ? companyData.name.toLowerCase().replace(/[^a-z0-9]/g, '') : 'company')
        profile.website = companyData.website || `https://www.${profile.username}.com`
        profile.pocName = companyData.pocName || 'Talent Acquisition Team'
        profile.pocEmail = companyData.pocEmail || `recruiting@${profile.username}.com`
        profile.headOffice = companyData.headOffice || 'Seattle, Washington'
        profile.scale = companyData.scale || '500 - 1,000 Employees'
        profile.description = companyData.description || `${profile.name} is a leading enterprise in the ${profile.industry} sector. Known for innovation and modern engineering paradigms, they provide industry-recognized software solutions, business operations architecture, and engineering platforms for cloud scale.`
      } else {
        triggerToast('Failed to fetch company details from server.')
      }
    } catch (err) {
      console.error('Error fetching company details:', err)
      triggerToast('Error loading company profile data.')
    }
  } else {
    // If logged in company recruiter, load their details
    if (currentUser.value && currentUser.value.role === 'recruiter') {
      if (currentUser.value.name) profile.name = currentUser.value.name
      if (currentUser.value.username) profile.username = currentUser.value.username
      if (currentUser.value.email) profile.email = currentUser.value.email
    }
  }
})

// Back navigation helper
const goBack = () => {
  router.back()
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

/* Fallback Logo container */
.avatar-wrapper {
  position: relative;
  width: 120px;
  height: 120px;
}

.company-logo-fallback {
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

.company-link {
  color: #2d6b5e;
  text-decoration: none;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.company-link:hover {
  text-decoration: underline;
  color: #1b443b;
}

.status-text-badge {
  font-size: 11.5px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 12px;
  text-align: center;
  display: inline-block;
}

.status-whitelisted {
  background: #e6f4ea;
  color: #137333;
}

.status-blacklisted {
  background: #fce8e6;
  color: #c5221f;
}

/* Description Text */
.company-desc-txt {
  font-size: 14.5px;
  line-height: 1.6;
  color: #495057;
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
</style>
