<template>
  <div class="admin-layout">
    <!-- ── Sidebar ─────────────────────────── -->
    <Sidebar
      v-model="activeNav"
      :nav-items="navItems"
      logo-img="/Only_logo.png"
      title="LaunchPad"
      subtitle="Admin Console"
      @logout="handleLogout"
    />

    <!-- ── Main Content ────────────────────── -->
    <main class="main-content">
      <!-- Top Bar -->
      <AdminTopbar
        title="Company Management"
        v-model="searchQuery"
      />

      <!-- Stats Cards (4 Cards) -->
      <section class="stat-cards">
        <div class="stat-card">
          <div class="stat-top">
            <div class="stat-icon total-companies-icon"><i class="bi bi-building"></i></div>
          </div>
          <div class="stat-label">Total Companies</div>
          <div class="stat-value">{{ filteredCompanies.length }}</div>
        </div>

        <div class="stat-card">
          <div class="stat-top">
            <div class="stat-icon approved-icon"><i class="bi bi-patch-check"></i></div>
          </div>
          <div class="stat-label">Approved Companies</div>
          <div class="stat-value">{{ approvedCount }}</div>
        </div>

        <div class="stat-card">
          <div class="stat-top">
            <div class="stat-icon pending-icon"><i class="bi bi-hourglass-split"></i></div>
          </div>
          <div class="stat-label">Unapproved Companies</div>
          <div class="stat-value">{{ unapprovedCount }}</div>
        </div>

        <div class="stat-card">
          <div class="stat-top">
            <div class="stat-icon blacklisted-icon"><i class="bi bi-slash-circle"></i></div>
          </div>
          <div class="stat-label">Blacklisted Companies</div>
          <div class="stat-value">{{ blacklistedCount }}</div>
        </div>
      </section>

      <!-- Table 1: Unapproved Companies -->
      <section class="card table-card">
        <div class="table-header">
          <div class="table-title-group">
            <h2 class="table-title">Unapproved Companies (Pending Approval)</h2>
            <p class="table-subtitle">Review applications and verify companies to authorize job listings.</p>
          </div>
        </div>

        <div class="table-wrapper">
          <table class="companies-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="company in filteredUnapprovedCompanies" :key="company.id">
                <td class="company-name-cell">
                  <div class="name-wrapper">
                    <span class="avatar-fallback">{{ company.name.charAt(0) }}</span>
                    <div class="name-info">
                      <span class="full-name">{{ company.name }}</span>
                      <span class="industry-subtext">{{ company.industry || 'General Industry' }}</span>
                    </div>
                  </div>
                </td>
                <td class="email-cell">{{ company.email }}</td>
                <td class="text-center">
                  <div class="action-buttons-wrapper">
                    <button class="btn-approve" @click="approveCompany(company)">Approve</button>
                    <button class="btn-profile" @click="viewProfile(company)">View Profile</button>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredUnapprovedCompanies.length === 0">
                <td colspan="3" class="empty-state">
                  <div class="empty-title">No pending approvals</div>
                  <p class="empty-description">All registered companies have been reviewed.</p>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Table 2: All Companies (Approved / Registered) -->
      <section class="card table-card">
        <div class="table-header">
          <div class="table-title-group">
            <h2 class="table-title">All Registered Companies</h2>
            <p class="table-subtitle">Monitor corporate access, view detailed profiles, and manage blacklist states.</p>
          </div>
        </div>

        <div class="table-wrapper">
          <table class="companies-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th class="text-center">Profile</th>
                <th class="text-center">Blacklist / Whitelist Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="company in filteredAllCompanies" :key="company.id">
                <td class="company-name-cell">
                  <div class="name-wrapper">
                    <span class="avatar-fallback" :class="{ 'avatar-approved': company.approved }">
                      {{ company.name.charAt(0) }}
                    </span>
                    <div class="name-info">
                      <span class="full-name">{{ company.name }}</span>
                      <span class="industry-subtext">{{ company.industry || 'General Industry' }}</span>
                    </div>
                  </div>
                </td>
                <td class="email-cell">{{ company.email }}</td>
                <td class="text-center">
                  <button class="btn-profile" @click="viewProfile(company)">View Profile</button>
                </td>
                <td class="text-center">
                  <div class="status-toggle-wrapper">
                    <span :class="['status-text-badge', company.isBlacklisted ? 'status-blacklisted' : 'status-whitelisted']">
                      {{ company.isBlacklisted ? 'Blacklisted' : 'Whitelisted' }}
                    </span>
                    <label class="switch">
                      <input 
                        type="checkbox" 
                        :checked="!company.isBlacklisted"
                        @change="toggleBlacklist(company)"
                      />
                      <span class="slider round"></span>
                    </label>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredAllCompanies.length === 0">
                <td colspan="4" class="empty-state">
                  
                  <div class="empty-title">No companies found</div>
                  <p class="empty-description">Try adjusting your search criteria to find registered companies.</p>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Company Profile Modal -->
      <Teleport to="body">
        <div class="modal-overlay" v-if="showProfileModal" @click.self="showProfileModal = false">
          <div class="modal">
            <div class="modal-header">
              <span class="modal-logo-fallback">{{ selectedCompany?.name.charAt(0) }}</span>
              <div>
                <h3 class="modal-title">{{ selectedCompany?.name }}</h3>
                <span class="modal-subtitle">{{ selectedCompany?.industry }}</span>
              </div>
            </div>
            <div class="modal-body">
              <div class="info-row">
                <span class="info-label">Email:</span>
                <span class="info-value">{{ selectedCompany?.email }}</span>
              </div>
              <div class="info-row" v-if="selectedCompany?.website">
                <span class="info-label">Website:</span>
                <a :href="selectedCompany?.website" target="_blank" class="info-value link-style">
                  {{ selectedCompany?.website }}
                </a>
              </div>
              <div class="info-row" v-if="selectedCompany?.headOffice">
                <span class="info-label">Head Office:</span>
                <span class="info-value">{{ selectedCompany?.headOffice }}</span>
              </div>
              <div class="info-row" v-if="selectedCompany?.description">
                <span class="info-label">Description:</span>
                <p class="info-description">{{ selectedCompany?.description }}</p>
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
const activeNav = ref('Companies')
const searchQuery = ref('')
const showProfileModal = ref(false)
const selectedCompany = ref(null)

const companies = ref([])

// ── Sidebar nav ──────────────────────────────
const navItems = [
  { label: 'Dashboard',        icon: '' },
  { label: 'Students',         icon: '' },
  { label: 'Companies',        icon: '' },
  { label: 'Placement Drives', icon: '' },
  { label: 'Applications',     icon: '' },
]

watch(activeNav, (newVal) => {
  if (newVal === 'Dashboard')        router.push('/admin/dashboard')
  else if (newVal === 'Students')         router.push('/admin/students')
  else if (newVal === 'Companies')        router.push('/admin/companies')
  else if (newVal === 'Placement Drives') router.push('/admin/drives')
  else if (newVal === 'Applications')     router.push('/admin/applications')
})

// ── Fetch from API ───────────────────────────
let searchTimeout = null

watch(searchQuery, (newQuery) => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchCompanies(newQuery)
  }, 300)
})

async function fetchCompanies(q = '') {
  try {
    const token = localStorage.getItem('access_token')
    const url = q 
      ? `http://localhost:5555/admin/companies/search?q=${encodeURIComponent(q)}` 
      : 'http://localhost:5555/admin/all-companies'
      
    const res = await fetch(url, {
      headers: { Authorization: `Bearer ${token}` },
    })
    if (res.ok) companies.value = await res.json()
  } catch (err) {
    console.error('Error fetching companies:', err)
  }
}

onMounted(() => {
  fetchCompanies()
})

// ── Computed ─────────────────────────────────
const filteredCompanies = computed(() => {
  return companies.value
})

const filteredUnapprovedCompanies = computed(() =>
  filteredCompanies.value.filter(c => !c.approved)
)

const filteredAllCompanies = computed(() =>
  filteredCompanies.value.filter(c => c.approved)
)

const approvedCount   = computed(() => companies.value.filter(c =>  c.approved).length)
const unapprovedCount = computed(() => companies.value.filter(c => !c.approved).length)
const blacklistedCount = computed(() => companies.value.filter(c => c.isBlacklisted).length)

// ── Methods ──────────────────────────────────
async function approveCompany(company) {
  try {
    const token = localStorage.getItem('access_token')
    const res = await fetch(`http://localhost:5555/admin/company/approve/${company.id}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token}` },
    })
    if (res.ok) {
      company.approved = !company.approved
    } else {
      console.error('Failed to approve company')
    }
  } catch (err) {
    console.error('Error approving company:', err)
  }
}

async function toggleBlacklist(company) {
  try {
    const token = localStorage.getItem('access_token')
    const res = await fetch(`http://localhost:5555/admin/company/blacklist/${company.id}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token}` },
    })
    if (res.ok) {
      company.isBlacklisted = !company.isBlacklisted
    } else {
      console.error('Failed to toggle company blacklist status')
    }
  } catch (err) {
    console.error('Error blacklisting company:', err)
  }
}

function viewProfile(company) {
  router.push(`/company/profile/${company.id}`)
}

async function handleLogout() {
  try {
    const token = localStorage.getItem('access_token')
    await fetch('http://localhost:5555/api/auth/logout', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
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

/* ─── Loading / Error ─────────────────────── */
.loading-state {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 18px 22px;
  background: #fff;
  border-radius: 12px;
  color: #5a7a75;
  font-size: 13.5px;
  font-weight: 500;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

@keyframes spin { to { transform: rotate(360deg); } }
.spinner {
  width: 18px;
  height: 18px;
  border: 2.5px solid #d1e7e3;
  border-top-color: #2d6b5e;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  flex-shrink: 0;
}

.fetch-error {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 18px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 10px;
  color: #b91c1c;
  font-size: 13px;
  font-weight: 500;
}

/* ─── Layout ──────────────────────────────── */
.admin-layout {
  display: flex;
  height: 100vh;
  background: #f5f5f0;
  overflow: hidden;
}

/* ─── Main Content ────────────────────────── */
.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 28px 28px 40px;
  display: flex;
  flex-direction: column;
  gap: 22px;
}

/* ─── Stat Cards (Grid of 4) ──────────────── */
.stat-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
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

.total-companies-icon { background: #e8f4f1; color: #2d6b5e; }
.approved-icon { background: #e0f0ec; color: #2d6b5e; }
.pending-icon { background: #faeae7; color: #b94a3b; }

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

/* ─── Card Section ────────────────────────── */
.card {
  background: #fff;
  border-radius: 14px;
  padding: 22px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}

.table-card {
  display: flex;
  flex-direction: column;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-title {
  font-size: 15.5px;
  font-weight: 700;
  color: #1a2e28;
}

.table-subtitle {
  font-size: 12.5px;
  color: #8a9e9a;
  margin-top: 4px;
}

/* ─── Table ───────────────────────────────── */
.table-wrapper {
  overflow-x: auto;
  border-radius: 10px;
  border: 1px solid #eff3f2;
}

.companies-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 13.5px;
}

.companies-table th {
  background: #f9fdfb;
  color: #5a7a75;
  font-weight: 600;
  padding: 14px 16px;
  border-bottom: 1.5px solid #eff3f2;
}

.companies-table td {
  padding: 14px 16px;
  border-bottom: 1px solid #eff3f2;
  color: #2e3e3b;
  vertical-align: middle;
}

.companies-table tr:last-child td {
  border-bottom: none;
}

.companies-table tr:hover td {
  background: #fdfdfd;
}

/* Name wrapper info */
.name-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar-fallback {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #faeae7;
  color: #b94a3b;
  font-size: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

.avatar-fallback.avatar-approved {
  background: #e8f4f1;
  color: #2d6b5e;
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

.industry-subtext {
  font-size: 11px;
  color: #8a9e9a;
  margin-top: 1px;
}

.email-cell {
  color: #4a6e6b;
  font-size: 13px;
}

/* Actions wrapper */
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
  padding: 7px 14px;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}

.btn-approve:hover {
  background: #235349;
}

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

/* ─── Toggle Switch Styling ───────────────── */
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

/* ─── Empty state ─────────────────────────── */
.empty-state {
  text-align: center;
  padding: 40px 0 !important;
}


.empty-title {
  font-size: 15px;
  font-weight: 700;
  color: #1a2e28;
}

.empty-description {
  font-size: 12.5px;
  color: #8a9e9a;
  margin-top: 6px;
}

/* ─── Company Profile Modal ───────────────── */
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
  max-width: 480px;
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
  background: #faeae7;
  color: #b94a3b;
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

.info-description {
  font-size: 13px;
  color: #4b5563;
  line-height: 1.5;
  background: #f9fdfb;
  padding: 10px 12px;
  border-radius: 8px;
  border-left: 3px solid #2d6b5e;
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
