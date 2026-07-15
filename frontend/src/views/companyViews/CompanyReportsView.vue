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
      <!-- Top Bar / Header with Month Selector -->
      <header class="report-header">
        <div class="header-left">
          <span class="report-header-subtitle">RECRUITMENT</span>
          <h1 class="report-header-title">Corporate Reports</h1>
        </div>
        <div class="header-right">
          <label for="month-select" class="month-label">Select Month:</label>
          <input 
            type="month" 
            id="month-select" 
            v-model="selectedMonth" 
            class="month-input" 
            @change="loadMonthlyData"
          />
        </div>
      </header>

      <!-- Monthly Summary Stats Grid -->
      <section class="stats-grid">
        <div class="stat-box orange-accent">
          <span class="stat-icon"><i class="bi bi-megaphone"></i></span>
          <div class="stat-info">
            <span class="stat-lbl">Drives Created</span>
            <span class="stat-val">{{ monthlyTotals.drives }}</span>
          </div>
        </div>
        <div class="stat-box sienna-accent">
          <span class="stat-icon"><i class="bi bi-file-earmark-text"></i></span>
          <div class="stat-info">
            <span class="stat-lbl">Applications Received</span>
            <span class="stat-val">{{ monthlyTotals.applications }}</span>
          </div>
        </div>
        <div class="stat-box dark-accent">
          <span class="stat-icon"><i class="bi bi-calendar-event"></i></span>
          <div class="stat-info">
            <span class="stat-lbl">Interviews Scheduled</span>
            <span class="stat-val">{{ monthlyTotals.interviews }}</span>
          </div>
        </div>
      </section>

      <!-- Corporate Reports Chart Card -->
      <section class="report-card">
        <div class="report-card-header">
          <div>
            <h2 class="report-card-title">Recruitment Activity Trends</h2>
            <p class="report-card-subtitle">Activity breakdown from the 1st to the 31st for {{ formattedMonth }}</p>
          </div>
          <button @click="exportReport" class="btn-export">
            <i class="bi bi-file-earmark-arrow-down-fill"></i> Export Monthly Activity
          </button>
        </div>

        <!-- Chart Canvas -->
        <div class="chart-container">
          <canvas ref="chartRef"></canvas>
        </div>
      </section>
    </main>

  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import Chart from 'chart.js/auto'

const router = useRouter()
const activeNav = ref('Report')

// Get default current month (YYYY-MM)
const getTodayMonth = () => {
  const d = new Date()
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  return `${year}-${month}`
}

const selectedMonth = ref(getTodayMonth())
const chartRef = ref(null)
let chartInstance = null

const navItems = [
  { label: 'Dashboard',    icon: '<i class="bi bi-speedometer2"></i>' },
  { label: 'Drives',       icon: '<i class="bi bi-megaphone"></i>' },
  { label: 'Applications', icon: '<i class="bi bi-file-earmark-text"></i>' },
  { label: 'Shortlisted',  icon: '<i class="bi bi-patch-check"></i>' },
  { label: 'Interviews',   icon: '<i class="bi bi-calendar-event"></i>' },
  { label: 'Report',       icon: '<i class="bi bi-file-earmark-bar-graph"></i>' },
  { label: 'Profile',      icon: '<i class="bi bi-building"></i>' }
]

// Daily lists loaded from backend
const rawData = ref({
  labels: [],
  drives: [],
  applications: [],
  interviews: []
})

// Calculate totals from daily breakdown
const monthlyTotals = computed(() => {
  const sum = (arr) => (arr || []).reduce((a, b) => a + b, 0)
  return {
    drives: sum(rawData.value.drives),
    applications: sum(rawData.value.applications),
    interviews: sum(rawData.value.interviews)
  }
})

const formattedMonth = computed(() => {
  if (!selectedMonth.value) return ''
  const [year, month] = selectedMonth.value.split('-')
  const date = new Date(year, parseInt(month) - 1, 1)
  return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
})

watch(activeNav, (newVal) => {
  if (newVal === 'Dashboard') {
    router.push('/company/dashboard')
  } else if (newVal === 'Profile') {
    const userJson = localStorage.getItem('user')
    if (userJson) {
      const u = JSON.parse(userJson)
      router.push(`/company/profile/${u.id}`)
    } else {
      router.push('/company/dashboard')
    }
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

const loadMonthlyData = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const res = await fetch(`http://localhost:5555/api/company/reports/monthly?month=${selectedMonth.value}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (res.ok) {
      const data = await res.json()
      rawData.value = data
      renderChart()
    }
  } catch (err) {
    console.error('Failed to fetch corporate monthly reports:', err)
  }
}

const renderChart = () => {
  if (!chartRef.value) return
  const ctx = chartRef.value.getContext('2d')
  
  if (chartInstance) {
    chartInstance.destroy()
  }

  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: rawData.value.labels,
      datasets: [
        {
          label: 'Drives Created',
          data: rawData.value.drives,
          borderColor: '#e07a5f',
          backgroundColor: 'rgba(224, 122, 95, 0.08)',
          borderWidth: 2,
          pointBackgroundColor: '#e07a5f',
          tension: 0.3,
          fill: true
        },
        {
          label: 'Applications Received',
          data: rawData.value.applications,
          borderColor: '#b94a3b',
          backgroundColor: 'rgba(185, 74, 59, 0.08)',
          borderWidth: 2,
          pointBackgroundColor: '#b94a3b',
          tension: 0.3,
          fill: true
        },
        {
          label: 'Interviews Scheduled',
          data: rawData.value.interviews,
          borderColor: '#253a35',
          backgroundColor: 'rgba(37, 58, 53, 0.08)',
          borderWidth: 2,
          pointBackgroundColor: '#253a35',
          tension: 0.3,
          fill: true
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            boxWidth: 12,
            font: { family: 'Inter', size: 12 }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(0, 0, 0, 0.04)'
          },
          ticks: {
            stepSize: 1,
            precision: 0
          }
        },
        x: {
          grid: {
            display: false
          }
        }
      }
    }
  })
}

function exportReport() {
  let iframe = document.getElementById('print-iframe');
  if (!iframe) {
    iframe = document.createElement('iframe');
    iframe.id = 'print-iframe';
    iframe.style.position = 'fixed';
    iframe.style.right = '0';
    iframe.style.bottom = '0';
    iframe.style.width = '0';
    iframe.style.height = '0';
    iframe.style.border = 'none';
    document.body.appendChild(iframe);
  }

  const htmlContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Corporate Recruitment Report - ${selectedMonth.value}</title>
      <style>
        body { font-family: 'Inter', sans-serif; padding: 40px; color: #27231E; background: #ffffff; }
        h1 { font-size: 24px; color: #b94a3b; border-bottom: 2px solid #b94a3b; padding-bottom: 10px; margin-top: 0; }
        .meta { margin-bottom: 30px; font-size: 14px; color: #666; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #fdf0ea; color: #b94a3b; font-weight: 700; }
        tr:nth-child(even) { background-color: #fafafa; }
        .summary { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 30px; }
        .summary-card { background: #fafafa; border: 1px solid #ddd; padding: 15px; border-radius: 8px; }
        .summary-label { font-size: 11px; color: #888; text-transform: uppercase; font-weight: 600; }
        .summary-value { font-size: 20px; font-weight: bold; color: #27231E; margin-top: 5px; }
      </style>
    </head>
    <body>
      <h1>LaunchPad Corporate Recruitment Report</h1>
      <div class="meta">
        <p><strong>Reporting Period:</strong> ${formattedMonth.value}</p>
        <p><strong>Generated On:</strong> ${new Date().toLocaleString()}</p>
      </div>
      
      <div class="summary">
        <div class="summary-card">
          <div class="summary-label">Drives Created</div>
          <div class="summary-value">${monthlyTotals.value.drives}</div>
        </div>
        <div class="summary-card">
          <div class="summary-label">Applications Received</div>
          <div class="summary-value">${monthlyTotals.value.applications}</div>
        </div>
        <div class="summary-card">
          <div class="summary-label">Interviews Scheduled</div>
          <div class="summary-value">${monthlyTotals.value.interviews}</div>
        </div>
      </div>

      <table>
        <thead>
          <tr>
            <th>Day</th>
            <th>Drives Created</th>
            <th>Applications Received</th>
            <th>Interviews Scheduled</th>
          </tr>
        </thead>
        <tbody>
          ${rawData.value.labels.map((label, idx) => `
            <tr>
              <td><strong>${label}</strong></td>
              <td>${rawData.value.drives[idx] || 0}</td>
              <td>${rawData.value.applications[idx] || 0}</td>
              <td>${rawData.value.interviews[idx] || 0}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </body>
    </html>
  `;

  const doc = iframe.contentDocument || iframe.contentWindow.document;
  doc.open();
  doc.write(htmlContent);
  doc.close();

  setTimeout(() => {
    iframe.contentWindow.focus();
    iframe.contentWindow.print();
  }, 500);
}

onMounted(() => {
  loadMonthlyData()
})

async function handleLogout() {
  try {
    const token = localStorage.getItem('access_token')
    await fetch('http://localhost:5555/api/auth/logout', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` }
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

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 4px;
}

.report-header-subtitle {
  font-size: 11px;
  font-weight: 800;
  color: #b94a3b;
  letter-spacing: 1px;
}

.report-header-title {
  font-size: 28px;
  font-weight: 700;
  color: #27231E;
  margin: 4px 0 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.month-label {
  font-size: 13.5px;
  font-weight: 600;
  color: #495057;
}

.month-input {
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 13.5px;
  font-weight: 600;
  color: #b94a3b;
  outline: none;
  background: #ffffff;
  cursor: pointer;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.stat-box {
  background: #ffffff;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 14px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
  border: 1px solid rgba(0, 0, 0, 0.04);
}

.stat-icon {
  width: 42px;
  height: 42px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.sienna-accent .stat-icon { background: #faeae7; color: #b94a3b; }
.orange-accent .stat-icon { background: #fdf0ea; color: #e07a5f; }
.dark-accent .stat-icon { background: #e9ecef; color: #253a35; }

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-lbl {
  font-size: 11px;
  font-weight: 600;
  color: #8c8985;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-val {
  font-size: 20px;
  font-weight: 700;
  color: #27231E;
  margin-top: 2px;
}

/* Report Card & Chart styling */
.report-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(0, 0, 0, 0.05);
  flex: 1;
  display: flex;
  flex-direction: column;
}

.report-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.report-card-title {
  font-size: 20px;
  font-weight: 700;
  color: #27231E;
  margin: 0;
}

.report-card-subtitle {
  font-size: 13px;
  color: #8c8985;
  margin: 4px 0 0;
}

.btn-export {
  background: #b94a3b;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 13.5px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background 0.15s;
}
.btn-export:hover {
  background: #a03a2c;
}

.chart-container {
  flex: 1;
  min-height: 380px;
  position: relative;
}
</style>
