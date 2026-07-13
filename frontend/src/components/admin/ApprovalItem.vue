<template>
  <div class="approval-item">
    <!-- Icon -->
    <div class="approval-icon">
      <span v-html="item.icon"></span>
    </div>

    <!-- Info -->
    <div class="approval-info">
      <div class="approval-name">{{ item.name }}</div>
      <div class="approval-meta">{{ item.meta }}</div>
    </div>

    <!-- Actions -->
    <div class="approval-actions">
      <button class="btn-secondary" @click="$emit('primary', item)">
        {{ item.primaryBtn }}
      </button>
      <button class="btn-danger" @click="$emit('approve', item)">Approve</button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    required: true,
    /**
     * Expected shape:
     * { name: string, meta: string, icon: string, primaryBtn: string }
     */
  },
})

defineEmits(['primary', 'approve'])
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.approval-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px;
  border: 1px solid #eff3f2;
  border-radius: 10px;
  transition: background 0.15s;
  font-family: 'Inter', sans-serif;
}

.approval-item:hover { background: #f9fdfb; }

.approval-icon {
  width: 40px;
  height: 40px;
  background: #f0f5f4;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.approval-info {
  flex: 1;
  min-width: 0;
}

.approval-name {
  font-size: 13.5px;
  font-weight: 600;
  color: #1a2e28;
}

.approval-meta {
  font-size: 11.5px;
  color: #8a9e9a;
  margin-top: 2px;
}

.approval-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.btn-secondary {
  background: #fff;
  border: 1.5px solid #cdd8d5;
  color: #3a5c55;
  border-radius: 7px;
  padding: 7px 14px;
  font-size: 12.5px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s;
  white-space: nowrap;
}

.btn-secondary:hover {
  background: #f0f5f4;
  border-color: #4a6e6b;
}

.btn-danger {
  background: #b94a3b;
  color: #fff;
  border: none;
  border-radius: 7px;
  padding: 7px 16px;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, transform 0.15s;
  white-space: nowrap;
}

.btn-danger:hover {
  background: #a03a2c;
  transform: translateY(-1px);
}
</style>
