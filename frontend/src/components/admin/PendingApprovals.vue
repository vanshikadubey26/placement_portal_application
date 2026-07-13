<template>
  <section class="card">
    <!-- Header -->
    <div class="card-header">
      <h2 class="card-title">Pending Approvals</h2>
      <div class="card-badges">
        <span class="badge badge-red">{{ companiesCount }} Companies</span>
        <span class="badge badge-teal">{{ drivesCount }} Drives</span>
      </div>
    </div>

    <!-- List -->
    <div class="approval-list">
      <ApprovalItem
        v-for="item in approvals"
        :key="item.name"
        :item="item"
        @primary="$emit('primary', item)"
        @approve="$emit('approve', item)"
      />
    </div>

    <!-- Footer link -->
    <div class="view-all">
      <a href="#" @click.prevent="$emit('view-all')">
        View all {{ totalPending }} pending requests
      </a>
    </div>
  </section>
</template>

<script setup>
import ApprovalItem from './ApprovalItem.vue'

defineProps({
  approvals: {
    type: Array,
    required: true,
  },
  companiesCount: {
    type: Number,
    default: 0,
  },
  drivesCount: {
    type: Number,
    default: 0,
  },
  totalPending: {
    type: Number,
    default: 0,
  },
})

defineEmits(['primary', 'approve', 'view-all'])
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.card {
  background: #fff;
  border-radius: 14px;
  padding: 22px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  font-family: 'Inter', sans-serif;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.card-title {
  font-size: 15.5px;
  font-weight: 700;
  color: #1a2e28;
}

.card-badges { display: flex; gap: 8px; }

.badge {
  font-size: 11.5px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
}

.badge-red  { background: #faeae7; color: #b94a3b; }
.badge-teal { background: #e0f0ec; color: #2d6b5e; }

.approval-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.view-all {
  text-align: center;
  margin-top: 16px;
}

.view-all a {
  font-size: 12.5px;
  color: #4a6e6b;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.15s;
}

.view-all a:hover { color: #b94a3b; }
</style>
