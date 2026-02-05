<template>
  <div class="incident-detail" v-if="incident">
    <div class="back-button">
      <router-link to="/incidents">← Back to Incidents</router-link>
    </div>

    <div class="detail-header">
      <h2>{{ incident.title }}</h2>
      <span class="severity-badge" :class="incident.severity">{{ incident.severity }}</span>
    </div>

    <div class="detail-grid">
      <div class="card">
        <h3>Incident Information</h3>
        <div class="info-row">
          <span class="label">Incident ID:</span>
          <span class="value">{{ incident.id }}</span>
        </div>
        <div class="info-row">
          <span class="label">Status:</span>
          <span class="status-badge" :class="incident.status">{{ incident.status.replace('_', ' ') }}</span>
        </div>
        <div class="info-row">
          <span class="label">Assignee:</span>
          <span class="value">{{ incident.assignee }}</span>
        </div>
        <div class="info-row">
          <span class="label">Created:</span>
          <span class="value">{{ incident.createdAt }}</span>
        </div>
        <div class="info-row">
          <span class="label">Updated:</span>
          <span class="value">{{ incident.updatedAt }}</span>
        </div>
        <div class="info-row">
          <span class="label">Affected Systems:</span>
          <span class="value">{{ incident.affectedSystems }}</span>
        </div>
      </div>

      <div class="card timeline">
        <h3>Timeline</h3>
        <div class="timeline-list">
          <div v-for="(entry, index) in incident.timeline" :key="index" class="timeline-entry">
            <div class="timeline-time">{{ entry.time }}</div>
            <div class="timeline-action">{{ entry.action }}</div>
            <div class="timeline-user">by {{ entry.user }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useXdrStore } from '../stores/xdr'

const route = useRoute()
const xdrStore = useXdrStore()
const incident = ref(null)

onMounted(async () => {
  try {
    incident.value = await xdrStore.getIncidentById(route.params.id)
  } catch (error) {
    console.error('Failed to load incident:', error)
  }
})
</script>

<style scoped>
.incident-detail {
  padding: 2rem;
  min-height: 100%;
  width: 100%;
  background: #f9fafb;
}

.back-button a {
  color: #2563eb;
  text-decoration: none;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 1.5rem 0;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card h3 {
  margin-top: 0;
  margin-bottom: 1rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.label {
  font-weight: 600;
  color: #6b7280;
}

.timeline-entry {
  padding: 1rem;
  background: #f9fafb;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.timeline-time {
  font-weight: 600;
  color: #2563eb;
}

.timeline-action {
  color: #1f2937;
  margin: 0.25rem 0;
}

.timeline-user {
  font-size: 0.85rem;
  color: #6b7280;
}

.severity-badge, .status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
}

.severity-badge.critical {
  background: #fee2e2;
  color: #991b1b;
}
</style>
