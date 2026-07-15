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
          <h1 class="topbar-title">My Applications</h1>
          <p class="topbar-subtitle">Track your application history and scheduled interviews</p>
        </div>
        <div style="display: flex; gap: 12px; align-items: center;">
          <div class="search-box">
            <i class="bi bi-search search-icon"></i>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search by drive or company..."
              class="search-input"
            />
            <button v-if="searchQuery" class="search-clear" @click="searchQuery = ''">
              <i class="bi bi-x"></i>
            </button>
          </div>
          <button @click="triggerExport" class="btn-export" style="background: #2d6b5e; color: white; border: none; border-radius: 8px; padding: 10px 16px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 8px; font-size: 13.5px; height: 42px;">
            <i class="bi bi-file-earmark-arrow-down"></i> Export Applications (CSV)
          </button>
        </div>
      </header>

      <!-- Toast Alert -->
      <div v-if="toastMessage" :class="['toast-alert', toastType === 'error' ? 'error' : 'success']">
        <i :class="toastType === 'error' ? 'bi bi-exclamation-circle' : 'bi bi-check-circle'"></i>
        {{ toastMessage }}
      </div>

      <div class="dashboard-body">
        
        <!-- Tab navigation inside view -->
        <div class="tabs-header mb-4">
          <button :class="['tab-btn', { active: activeTab === 'applications' }]" @click="activeTab = 'applications'">
            <i class="bi bi-file-earmark-text"></i> Application History ({{ filteredApplications.length }})
          </button>
          <button :class="['tab-btn', { active: activeTab === 'interviews' }]" @click="activeTab = 'interviews'">
            <i class="bi bi-calendar2-check"></i> Interview Schedules ({{ filteredInterviews.length }})
          </button>
        </div>

        <div v-if="loading" class="empty-state">Loading details...</div>

        <div v-else>
          <!-- Applications Tab View -->
          <div v-if="activeTab === 'applications'" class="table-wrapper">
            <table class="applications-table">
              <thead>
                <tr>
                  <th style="width: 40px;"></th>
                  <th>Placement Drive</th>
                  <th>Company</th>
                  <th>Applied On</th>
                  <th>Last Update</th>
                  <th class="text-center">Status</th>
                </tr>
              </thead>
              <tbody>
                <template v-for="app in filteredApplications" :key="app.id">
                  <tr class="clickable-row" @click="toggleExpand(app.id)">
                    <td class="text-center font-bold" style="width: 40px; cursor: pointer;">
                      <i :class="['bi', expandedAppId === app.id ? 'bi-chevron-down' : 'bi-chevron-right']"></i>
                    </td>
                    <td class="font-bold">{{ app.driveTitle }}</td>
                    <td class="company-text"><i class="bi bi-building"></i> {{ app.companyName }}</td>
                    <td>{{ formatDate(app.appliedAt) }}</td>
                    <td>{{ formatDate(app.updatedAt) }}</td>
                    <td class="text-center">
                      <span :class="['status-badge', getStatusClass(app.status)]">
                        {{ app.status }}
                      </span>
                    </td>
                  </tr>

                  <!-- Expandable Detail Row -->
                  <tr v-if="expandedAppId === app.id" class="detail-expanded-row">
                    <td colspan="7">
                      <div class="expanded-card">
                        <div class="status-summary-box mb-4">
                          <i class="bi bi-info-circle-fill info-icon"></i>
                          <div class="summary-text">
                            <strong>Status Update:</strong> {{ getDetailedStatusInfo(app.status).message }}
                          </div>
                        </div>

                        <!-- Stepper Timeline -->
                        <div class="application-stepper">
                          <!-- Step 1: Applied -->
                          <div :class="['step-item', { active: getDetailedStatusInfo(app.status).currentStep >= 1 }]">
                            <div class="step-circle"><i class="bi bi-file-earmark-check-fill"></i></div>
                            <div class="step-label">Applied</div>
                            <div class="step-date">{{ formatDate(app.appliedAt) }}</div>
                          </div>
                          
                          <div :class="['step-line', { active: getDetailedStatusInfo(app.status).currentStep >= 2 }]"></div>

                          <!-- Step 2: Shortlisted / Rejected -->
                          <div :class="['step-item', { 
                            active: getDetailedStatusInfo(app.status).currentStep >= 2,
                            rejected: getDetailedStatusInfo(app.status).isRejected 
                          }]">
                            <div class="step-circle">
                              <i v-if="getDetailedStatusInfo(app.status).isRejected" class="bi bi-x-circle-fill"></i>
                              <i v-else class="bi bi-person-check-fill"></i>
                            </div>
                            <div class="step-label">{{ getDetailedStatusInfo(app.status).isRejected ? 'Rejected' : 'Shortlisted' }}</div>
                            <div class="step-date" v-if="getDetailedStatusInfo(app.status).currentStep >= 2">{{ formatDate(app.updatedAt) }}</div>
                          </div>

                          <div :class="['step-line', { 
                            active: getDetailedStatusInfo(app.status).currentStep >= 3,
                            hidden: getDetailedStatusInfo(app.status).isRejected
                          }]"></div>

                          <!-- Step 3: Interview Scheduled -->
                          <div :class="['step-item', { 
                            active: getDetailedStatusInfo(app.status).currentStep >= 3,
                            hidden: getDetailedStatusInfo(app.status).isRejected 
                          }]">
                            <div class="step-circle"><i class="bi bi-calendar2-check-fill"></i></div>
                            <div class="step-label">Interview</div>
                          </div>

                          <div :class="['step-line', { 
                            active: getDetailedStatusInfo(app.status).currentStep >= 4,
                            hidden: getDetailedStatusInfo(app.status).isRejected
                          }]"></div>

                          <!-- Step 4: Job Offered / Selected -->
                          <div :class="['step-item', { 
                            active: getDetailedStatusInfo(app.status).currentStep >= 4,
                            hidden: getDetailedStatusInfo(app.status).isRejected 
                          }]">
                            <div class="step-circle"><i class="bi bi-trophy-fill"></i></div>
                            <div class="step-label">Decision</div>
                          </div>
                        </div>

                        <!-- Recruiter Feedback Card -->
                        <div v-if="app.comment" class="feedback-card mt-4">
                          <div class="feedback-header">
                            <i class="bi bi-chat-right-text-fill feedback-icon"></i>
                            <span>Recruiter Feedback & Comments</span>
                          </div>
                          <div class="feedback-body">
                            {{ app.comment }}
                          </div>
                        </div>
                      </div>
                    </td>
                  </tr>
                </template>
                <tr v-if="filteredApplications.length === 0">
                  <td colspan="7" class="empty-state">
                    <i class="bi bi-file-earmark-text" style="font-size:32px;display:block;margin-bottom:8px;color:#8a9e9a;"></i>
                    {{ searchQuery ? 'No applications match your search.' : 'You have not applied to any drives yet.' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Interviews Tab View -->
          <div v-if="activeTab === 'interviews'" class="interviews-grid">
            <div v-for="iv in filteredInterviews" :key="iv.id" class="interview-card">
              <div class="iv-card-header">
                <div>
                  <h3 class="iv-title">{{ iv.driveTitle }}</h3>
                  <span class="iv-company"><i class="bi bi-building"></i> {{ iv.companyName }}</span>
                </div>
                <span class="badge-mode-online">{{ iv.mode }}</span>
              </div>

              <div class="iv-card-body">
                <div class="iv-detail"><i class="bi bi-calendar-event"></i> <span><strong>Date & Time:</strong> {{ formatDateTime(iv.scheduled_at) }}</span></div>
                <div v-if="iv.meeting_link" class="iv-detail mt-2">
                  <i class="bi bi-link-45deg"></i>
                  <span>
                    <strong>Meeting Link:</strong> 
                    <a :href="iv.meeting_link" target="_blank" class="meet-link">Join Meeting <i class="bi bi-box-arrow-up-right"></i></a>
                  </span>
                </div>
                <div v-else-if="iv.location" class="iv-detail mt-2">
                  <i class="bi bi-geo-alt"></i>
                  <span><strong>Location:</strong> {{ iv.location }}</span>
                </div>
              </div>

              <!-- Offer Action -->
              <div v-if="iv.application_status === 'Job Offered' || iv.application_status === 'Offer Accepted'" class="iv-card-actions mt-3 pt-2" style="border-top: 1px dashed #eff3f2; display: flex; justify-content: flex-end;">
                <button class="btn-view-offer" @click="openOfferLetter(iv)">
                  <i class="bi bi-file-earmark-medical"></i> View Offer Letter
                </button>
              </div>
            </div>

            <div v-if="filteredInterviews.length === 0" class="empty-state w-full">
              <i class="bi bi-calendar-x" style="font-size:36px;display:block;margin-bottom:12px;color:#8a9e9a;"></i>
              {{ searchQuery ? 'No interviews match your search.' : 'No interviews scheduled yet.' }}
            </div>
          </div>
        </div>

      </div>
    </main>

    <!-- Offer Letter Modal -->
    <div class="modal-overlay" v-if="showOfferModal" @click.self="showOfferModal = false">
      <div class="offer-letter-modal">
        <div class="offer-letter-content">
          <div class="offer-header">
            <img src="/Only_logo.png" class="offer-logo" alt="LaunchPad Logo" />
            <div class="offer-company-info">
              <h2>{{ selectedOffer?.companyName }}</h2>
              <p>Corporate Recruitment Division</p>
            </div>
          </div>
          
          <div class="offer-body">
            <h3>Letter of Employment Offer</h3>
            <p class="offer-date">Date: {{ new Date().toLocaleDateString('en-IN') }}</p>
            
            <p>Dear Candidate,</p>
            
            <p>
              Following your recent interviews and evaluations for the placement drive <strong>{{ selectedOffer?.driveTitle }}</strong>, 
              we are absolutely delighted to offer you employment at <strong>{{ selectedOffer?.companyName }}</strong>.
            </p>
            
            <table class="offer-details-table">
              <tr>
                <td><strong>Position/Role:</strong></td>
                <td>{{ selectedOffer?.driveTitle }}</td>
              </tr>
              <tr>
                <td><strong>Company:</strong></td>
                <td>{{ selectedOffer?.companyName }}</td>
              </tr>
              <tr>
                <td><strong>Employment Status:</strong></td>
                <td>Full-time</td>
              </tr>
            </table>
            
            <p>
              We are excited about the prospect of you joining our team and look forward to your valuable contributions 
              towards our organization's growth.
            </p>
            
            <p>Sincerely,</p>
            <p class="signature">
              <strong>Recruitment Team</strong><br>
              {{ selectedOffer?.companyName }}
            </p>
          </div>

          <div class="offer-footer">
            <div v-if="selectedOffer?.application_status === 'Offer Accepted'" class="accepted-message mb-3">
              <i class="bi bi-check-circle-fill"></i> You have accepted this job offer.
            </div>
            <div class="offer-actions">
              <button class="btn-print" @click="printOfferLetter">
                <i class="bi bi-printer"></i> Print / Download
              </button>
              <button class="btn-decline" @click="showOfferModal = false">Close</button>
              <button v-if="selectedOffer?.application_status !== 'Offer Accepted'" class="btn-accept" @click="acceptJobOffer(selectedOffer)">
                <span v-if="acceptingOffer">Accepting...</span>
                <span v-else>Accept Offer</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'

const router = useRouter()
const activeNav = ref('Applications')
const activeTab = ref('applications')

const navItems = [
  { label: 'Dashboard', icon: '<i class="bi bi-speedometer2"></i>' },
  { label: 'Drives',    icon: '<i class="bi bi-megaphone"></i>' },
  { label: 'Applications', icon: '<i class="bi bi-file-earmark-text"></i>' },
  { label: 'Profile',   icon: '<i class="bi bi-person-bounding-box"></i>' }
]

watch(activeNav, (newVal) => {
  if (newVal === 'Dashboard') {
    router.push('/student/dashboard')
  } else if (newVal === 'Drives') {
    router.push('/student/drives')
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

const applications = ref([])
const interviews = ref([])
const loading = ref(false)
const toastMessage = ref('')
const toastType = ref('success')
const searchQuery = ref('')

const filteredApplications = computed(() => {
  if (!searchQuery.value.trim()) return applications.value
  const q = searchQuery.value.toLowerCase()
  return applications.value.filter(a =>
    (a.driveTitle && a.driveTitle.toLowerCase().includes(q)) ||
    (a.companyName && a.companyName.toLowerCase().includes(q)) ||
    (a.status && a.status.toLowerCase().includes(q))
  )
})

const filteredInterviews = computed(() => {
  if (!searchQuery.value.trim()) return interviews.value
  const q = searchQuery.value.toLowerCase()
  return interviews.value.filter(iv =>
    (iv.driveTitle && iv.driveTitle.toLowerCase().includes(q)) ||
    (iv.companyName && iv.companyName.toLowerCase().includes(q)) ||
    (iv.mode && iv.mode.toLowerCase().includes(q))
  )
})

function showToast(msg, type = 'success') {
  toastMessage.value = msg
  toastType.value = type
  setTimeout(() => { toastMessage.value = '' }, 3500)
}

const triggerExport = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) return
  try {
    const res = await fetch('http://localhost:5555/api/student/export/applications', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await res.json()
    if (res.ok) {
      showToast(data.message || 'Export triggered successfully!')
      if (data.task_id) {
        pollExportStatus(data.task_id)
      }
    } else {
      showToast(data.message || 'Failed to trigger export.', 'error')
    }
  } catch (err) {
    showToast('Cannot connect to server to trigger export.', 'error')
  }
}

const pollExportStatus = (taskId) => {
  const interval = setInterval(async () => {
    try {
      const res = await fetch(`http://localhost:5555/api/common/task/${taskId}/status`)
      if (res.ok) {
        const data = await res.json()
        if (data.status === 'SUCCESS') {
          clearInterval(interval)
          showToast('Applications export ready! Downloading now...')
          
          // Trigger browser file download
          const link = document.createElement('a')
          link.href = `http://localhost:5555/static/exports/${data.result}`
          link.setAttribute('download', data.result)
          document.body.appendChild(link)
          link.click()
          document.body.removeChild(link)
        } else if (data.status === 'FAILURE') {
          clearInterval(interval)
          showToast('Failed to export CSV file.', 'error')
        }
      }
    } catch (err) {
      clearInterval(interval)
      console.error(err)
    }
  }, 1500)
}

function handleLogout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user')
  router.push('/login')
}

async function fetchApplicationsAndInterviews() {
  const token = localStorage.getItem('access_token')
  if (!token) return

  loading.value = true
  try {
    const appsRes = await fetch('http://localhost:5555/api/student/applications', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (appsRes.ok) {
      applications.value = await appsRes.json()
    }

    const ivRes = await fetch('http://localhost:5555/api/student/interviews', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (ivRes.ok) {
      interviews.value = await ivRes.json()
    }
  } catch {
    showToast('Failed to fetch data.', 'error')
  } finally {
    loading.value = false
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('en-IN', {
    day: 'numeric', month: 'short', year: 'numeric'
  })
}

function formatDateTime(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('en-IN', {
    day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit'
  })
}

function getStatusClass(status) {
  if (!status) return 'badge-applied'
  const s = status.toLowerCase()
  if (s === 'shortlisted') return 'badge-shortlisted'
  if (s === 'interview scheduled') return 'badge-interview'
  if (s === 'rejected') return 'badge-rejected'
  if (s === 'selected') return 'badge-selected'
  if (s === 'offer accepted') return 'badge-selected'
  if (s === 'job offered') return 'badge-offered'
  return 'badge-applied'
}

const expandedAppId = ref(null)

function toggleExpand(appId) {
  if (expandedAppId.value === appId) {
    expandedAppId.value = null
  } else {
    expandedAppId.value = appId
  }
}

function getDetailedStatusInfo(status) {
  const s = status ? status.toLowerCase() : ''
  if (s === 'shortlisted') {
    return {
      message: 'Great news! You have been shortlisted by the recruiter. They are reviewing candidate profiles and scheduling interview panels.',
      currentStep: 2,
      isRejected: false
    }
  } else if (s === 'interview scheduled') {
    return {
      message: 'Your interview has been scheduled! Check the "Interview Schedules" tab for the meeting link, date, time, and location details.',
      currentStep: 3,
      isRejected: false
    }
  } else if (s === 'rejected') {
    return {
      message: 'The recruiter has updated your application status. Unfortunately, you were not selected for this drive. Keep trying, new opportunities open up daily!',
      currentStep: 2,
      isRejected: true
    }
  } else if (s === 'job offered') {
    return {
      message: 'Congratulations! You have received a job offer. Go to the "Interview Schedules" tab to view and accept your offer letter.',
      currentStep: 4,
      isRejected: false
    }
  } else if (s === 'offer accepted') {
    return {
      message: 'Job Offer Accepted! You have officially accepted the offer. Congratulations on your new job!',
      currentStep: 4,
      isRejected: false
    }
  } else if (s === 'selected') {
    return {
      message: 'Congratulations! You have been selected for this position.',
      currentStep: 4,
      isRejected: false
    }
  }
  // Default is 'applied'
  return {
    message: 'Your application has been received. The company recruitment team is currently reviewing profiles and will update your status soon.',
    currentStep: 1,
    isRejected: false
  }
}

const showOfferModal = ref(false)
const selectedOffer = ref(null)
const acceptingOffer = ref(false)

function openOfferLetter(interview) {
  selectedOffer.value = interview
  showOfferModal.value = true
}

async function acceptJobOffer(offer) {
  const token = localStorage.getItem('access_token')
  if (!token) return
  
  acceptingOffer.value = true
  try {
    const res = await fetch(`http://localhost:5555/api/student/application/${offer.application_id}/accept-offer`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    const data = await res.json()
    if (!res.ok) {
      showToast(data.message || 'Failed to accept offer.', 'error')
      return
    }
    showToast('Job offer accepted successfully!')
    offer.application_status = 'Offer Accepted'
    
    const appItem = applications.value.find(a => a.id === offer.application_id)
    if (appItem) {
      appItem.status = 'Offer Accepted'
    }
  } catch {
    showToast('Network error while accepting offer.', 'error')
  } finally {
    acceptingOffer.value = false
  }
}

function printOfferLetter() {
  const modalContent = document.querySelector('.offer-letter-content').innerHTML;
  const printWindow = window.open('', '_blank');
  printWindow.document.write(`
    <html>
      <head>
        <title>Offer Letter - LaunchPad</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
        <style>
          body { font-family: 'Inter', sans-serif; padding: 40px; color: #2e3e3b; }
          .offer-header { display: flex; align-items: center; gap: 16px; border-bottom: 2px solid #eff3f2; padding-bottom: 16px; margin-bottom: 20px; }
          .offer-logo { height: 48px; }
          .offer-company-info h2 { font-size: 18px; font-weight: 700; color: #1a2e28; margin: 0; }
          .offer-company-info p { font-size: 12px; color: #8a9e9a; margin: 2px 0 0; }
          .offer-body h3 { font-size: 16px; font-weight: 700; color: #1a2e28; text-align: center; margin-bottom: 16px; text-transform: uppercase; }
          .offer-date { font-size: 12.5px; color: #5a7a75; }
          .offer-body p { font-size: 13px; line-height: 1.6; margin-bottom: 16px; }
          .offer-details-table { width: 100%; border-collapse: collapse; margin: 16px 0; border: 1px solid #eff3f2; }
          .offer-details-table td { padding: 10px 14px; font-size: 13px; border: 1px solid #eff3f2; }
          .offer-details-table td:first-child { width: 140px; color: #5a7a75; font-weight: bold; }
          .signature { margin-top: 24px; font-size: 13px; }
          .offer-footer { display: none; }
        </style>
      </head>
      <body>
        <div class="offer-letter-content">
          ${modalContent}
        </div>
        <script>
          window.onload = function() {
            window.print();
            setTimeout(function() { window.close(); }, 500);
          };
        <\/script>
      </body>
    </html>
  `);
  printWindow.document.close();
}

onMounted(() => {
  fetchApplicationsAndInterviews()
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

.search-box { display: flex; align-items: center; gap: 8px; background: #f4f9f8; border: 1.5px solid #d4e6e1; border-radius: 10px; padding: 8px 14px; min-width: 260px; transition: border-color 0.2s, box-shadow 0.2s; }
.search-box:focus-within { border-color: #2d6b5e; box-shadow: 0 0 0 3px rgba(45,107,94,0.1); }
.search-icon { color: #8a9e9a; font-size: 14px; flex-shrink: 0; }
.search-input { border: none; background: transparent; outline: none; font-size: 13px; color: #1a2e28; width: 100%; font-family: 'Inter', sans-serif; }
.search-input::placeholder { color: #a3b8b4; }
.search-clear { background: none; border: none; cursor: pointer; color: #8a9e9a; padding: 0; display: flex; align-items: center; font-size: 16px; transition: color 0.15s; }
.search-clear:hover { color: #1a2e28; }

.dashboard-body { padding: 24px 28px; }

/* Tabs */
.tabs-header { display: flex; gap: 12px; border-bottom: 1px solid #eff3f2; padding-bottom: 8px; }
.tab-btn { background: none; border: none; font-size: 13.5px; font-weight: 600; color: #8a9e9a; cursor: pointer; padding: 8px 16px; border-radius: 6px; display: inline-flex; align-items: center; gap: 6px; transition: all 0.15s; }
.tab-btn:hover { color: #2d6b5e; background: #e8f4f1; }
.tab-btn.active { color: #2d6b5e; background: #e8f4f1; }

/* Applications Table */
.table-wrapper { background: #fff; border-radius: 12px; border: 1px solid #eff3f2; overflow-x: auto; }
.applications-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; }
.applications-table th { background: #f9fdfb; color: #5a7a75; font-weight: 600; padding: 12px 16px; border-bottom: 1.5px solid #eff3f2; }
.applications-table td { padding: 12px 16px; border-bottom: 1px solid #eff3f2; color: #2e3e3b; vertical-align: middle; }
.applications-table tr:last-child td { border-bottom: none; }
.applications-table tr:hover td { background: #f9fdfb; }

.company-text { color: #4aa897; font-weight: 500; }
.comment-bubble { background: #fef2f2; border: 1px solid #fecaca; color: #b91c1c; padding: 6px 10px; border-radius: 6px; font-size: 11.5px; line-height: 1.4; display: inline-block; }

.status-badge { font-size: 11px; font-weight: 600; padding: 3px 9px; border-radius: 20px; display: inline-block; white-space: nowrap; }
.badge-shortlisted { background: #e0f2fe; color: #0369a1; }
.badge-interview { background: #d1fae5; color: #065f46; }
.badge-rejected { background: #fee2e2; color: #991b1b; }
.badge-selected { background: #dcfce7; color: #14532d; }
.badge-applied { background: #f3f4f6; color: #374151; }
.badge-offered { background: #fef3c7; color: #92400e; }

/* Interviews Grid */
.interviews-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
.w-full { grid-column: 1 / -1; }
.interview-card { background: #fff; border-radius: 12px; border: 1px solid #eff3f2; border-left: 4px solid #6b21a8; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.02); }
.iv-card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
.iv-title { font-size: 14px; font-weight: 700; color: #1a2e28; margin: 0; }
.iv-company { font-size: 12px; color: #8a9e9a; }
.badge-mode-online { font-size: 10.5px; font-weight: 600; padding: 2px 6px; border-radius: 4px; background: #f3e8ff; color: #6b21a8; }

.iv-card-body { font-size: 12px; color: #4b5563; }
.iv-detail { display: flex; align-items: center; gap: 8px; }
.iv-detail i { color: #6b21a8; font-size: 14px; }
.meet-link { color: #6b21a8; font-weight: 600; text-decoration: none; display: inline-flex; align-items: center; gap: 4px; }
.meet-link:hover { text-decoration: underline; }

.empty-state { text-align: center; padding: 48px 0; color: #8a9e9a; font-size: 13.5px; }

/* Toast */
.toast-alert { position: fixed; bottom: 24px; right: 24px; padding: 12px 20px; border-radius: 8px; font-size: 13px; font-weight: 500; color: #fff; z-index: 9999; box-shadow: 0 4px 16px rgba(0,0,0,0.15); display: flex; align-items: center; gap: 8px; }
.toast-alert.success { background: #2d6b5e; }
.toast-alert.error { background: #dc2626; }

/* View Offer Button */
.btn-view-offer { background: #2d6b5e; color: #fff; border: none; border-radius: 6px; padding: 6px 12px; font-size: 11px; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 5px; transition: background 0.15s; }
.btn-view-offer:hover { background: #235349; }

/* Modal overlays and standard offer letter layout */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.4); display: flex; align-items: center; justify-content: center; z-index: 999; }
.offer-letter-modal { background: #fff; border-radius: 12px; padding: 32px; width: 100%; max-width: 550px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); max-height: 90vh; overflow-y: auto; font-family: 'Inter', sans-serif; }
.offer-header { display: flex; align-items: center; gap: 16px; border-bottom: 2px solid #eff3f2; padding-bottom: 16px; margin-bottom: 20px; }
.offer-logo { height: 48px; object-fit: contain; }
.offer-company-info h2 { font-size: 18px; font-weight: 700; color: #1a2e28; margin: 0; }
.offer-company-info p { font-size: 12px; color: #8a9e9a; margin: 2px 0 0; }
.offer-body h3 { font-size: 16px; font-weight: 700; color: #1a2e28; text-align: center; margin-bottom: 16px; text-transform: uppercase; letter-spacing: 0.5px; }
.offer-date { font-size: 12.5px; color: #5a7a75; margin-bottom: 16px; }
.offer-body p { font-size: 13px; color: #2e3e3b; line-height: 1.6; margin-bottom: 16px; }
.offer-details-table { width: 100%; border-collapse: collapse; margin: 16px 0; background: #f9fdfb; border-radius: 8px; border: 1px solid #eff3f2; }
.offer-details-table td { padding: 10px 14px; font-size: 13px; color: #2e3e3b; }
.offer-details-table td:first-child { width: 140px; color: #5a7a75; }
.signature { margin-top: 24px; font-size: 13px; color: #2e3e3b; line-height: 1.5; }
.offer-footer { border-top: 1px solid #eff3f2; padding-top: 16px; margin-top: 24px; }
.offer-actions { display: flex; justify-content: flex-end; gap: 12px; }
.btn-decline { background: #f3f4f6; color: #4b5563; border: 1px solid #d1d5db; border-radius: 6px; padding: 8px 16px; font-size: 12px; font-weight: 600; cursor: pointer; transition: background 0.15s; }
.btn-decline:hover { background: #e5e7eb; }
.btn-accept { background: #2d6b5e; color: #fff; border: none; border-radius: 6px; padding: 8px 18px; font-size: 12px; font-weight: 600; cursor: pointer; transition: background 0.15s; }
.btn-accept:hover { background: #235349; }
.accepted-message { display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 13px; font-weight: 600; color: #137333; background: #e6f4ea; padding: 10px; border-radius: 6px; }
.accepted-message.mb-3 { margin-bottom: 12px; }

.btn-print { background: #f3f4f6; color: #1e3a8a; border: 1px solid #bfdbfe; border-radius: 6px; padding: 8px 16px; font-size: 12px; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; transition: background 0.15s; margin-right: auto; }
.btn-print:hover { background: #dbeafe; }

/* Expandable row and stepper styles */
.clickable-row { cursor: pointer; transition: background 0.15s; }
.clickable-row:hover { background: #fafdfc !important; }
.detail-expanded-row { background: #fafdfc; }
.expanded-card { padding: 20px 24px; border-left: 4px solid #2d6b5e; background: #fff; margin: 4px 16px 16px; border-radius: 8px; box-shadow: inset 0 1px 3px rgba(0,0,0,0.02), 0 2px 8px rgba(0,0,0,0.02); }

.status-summary-box { display: flex; align-items: flex-start; gap: 10px; background: #e8f4f1; padding: 12px 16px; border-radius: 8px; border: 1px solid #d3eae4; }
.status-summary-box .info-icon { color: #2d6b5e; font-size: 16px; margin-top: 1px; }
.status-summary-box .summary-text { font-size: 12.5px; color: #235349; line-height: 1.5; }

.application-stepper { display: flex; align-items: center; justify-content: space-between; margin: 24px 0 16px; padding: 0 10px; }
.step-item { display: flex; flex-direction: column; align-items: center; position: relative; z-index: 1; flex-shrink: 0; min-width: 80px; }
.step-circle { width: 34px; height: 34px; border-radius: 50%; background: #f3f4f6; border: 2.5px solid #e5e7eb; color: #9ca3af; display: flex; align-items: center; justify-content: center; font-size: 14px; transition: all 0.25s; }
.step-label { font-size: 11.5px; font-weight: 600; color: #6b7280; margin-top: 8px; text-align: center; }
.step-date { font-size: 10px; color: #9ca3af; margin-top: 2px; }

.step-line { flex: 1; height: 3.5px; background: #e5e7eb; margin: -18px 8px 0; transition: all 0.25s; position: relative; z-index: 0; top: 9px; }

/* Active & Completed step states */
.step-item.active .step-circle { background: #2d6b5e; border-color: #2d6b5e; color: #fff; box-shadow: 0 0 0 4px rgba(45, 107, 94, 0.15); }
.step-item.active .step-label { color: #2d6b5e; }
.step-item.active .step-date { color: #8a9e9a; }
.step-line.active { background: #2d6b5e; }

/* Rejected step states */
.step-item.active.rejected .step-circle { background: #dc2626; border-color: #dc2626; color: #fff; box-shadow: 0 0 0 4px rgba(220, 38, 38, 0.15); }
.step-item.active.rejected .step-label { color: #dc2626; }
.step-line.hidden, .step-item.hidden { display: none !important; }

/* Feedback Card */
.feedback-card { background: #fffdf9; border: 1px solid #fef3c7; border-radius: 8px; padding: 14px 16px; }
.feedback-header { display: flex; align-items: center; gap: 8px; font-size: 12.5px; font-weight: 700; color: #92400e; margin-bottom: 8px; }
.feedback-icon { font-size: 15px; color: #b45309; }
.feedback-body { font-size: 12.5px; color: #78350f; line-height: 1.5; white-space: pre-line; }
</style>
