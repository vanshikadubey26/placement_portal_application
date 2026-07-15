<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <RouterView />
</template>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* Global PWA / Responsive Overrides */
@media (max-width: 768px) {
  /* Main layouts content spacing */
  .main-content {
    padding: 72px 16px 30px !important;
    gap: 16px !important;
  }

  /* Headers / Topbars */
  .topbar, .report-header, .header-card {
    flex-direction: column !important;
    align-items: flex-start !important;
    gap: 12px !important;
  }

  .topbar-actions, .header-right, .header-actions {
    width: 100% !important;
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    justify-content: flex-start !important;
  }

  /* Buttons in actions row */
  .topbar-actions button, .header-actions button, .btn-export, .btn-primary-custom {
    flex: 1 1 auto !important;
    justify-content: center !important;
  }

  /* Grids to single column */
  .stats-grid, 
  .dashboard-grid, 
  .profile-body-grid, 
  .info-rows-grid, 
  .academic-blocks-grid, 
  .form-grid {
    grid-template-columns: 1fr !important;
    gap: 16px !important;
  }

  /* Table responsive wrappers */
  .table-wrapper {
    overflow-x: auto !important;
    width: 100% !important;
    -webkit-overflow-scrolling: touch;
    border: 1px solid rgba(0, 0, 0, 0.05);
    border-radius: 8px;
  }

  table {
    width: 100% !important;
    min-width: 650px !important; /* Ensure table elements are readable and don't shrink */
  }

  /* Cards responsiveness */
  .card, .content-card, .table-card, .report-card {
    padding: 16px !important;
  }
}
</style>
