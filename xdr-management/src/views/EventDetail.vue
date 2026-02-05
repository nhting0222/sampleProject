<template>
  <div class="event-detail" v-if="event">
    <div class="back-button">
      <router-link to="/events">← Back to Events</router-link>
    </div>

    <div class="detail-header">
      <h2>{{ event.type }}</h2>
      <span class="severity-badge" :class="event.severity">{{ event.severity }}</span>
    </div>

    <div class="detail-grid">
      <div class="card">
        <h3>Event Information</h3>
        <div class="info-row">
          <span class="label">Event ID:</span>
          <span class="value">{{ event.id }}</span>
        </div>
        <div class="info-row">
          <span class="label">Timestamp:</span>
          <span class="value">{{ event.timestamp }}</span>
        </div>
        <div class="info-row">
          <span class="label">Source:</span>
          <span class="value">{{ event.source }}</span>
        </div>
        <div class="info-row">
          <span class="label">Status:</span>
          <span class="status-badge" :class="event.status">{{ event.status }}</span>
        </div>
        <div class="info-row">
          <span class="label">Description:</span>
          <span class="value">{{ event.description }}</span>
        </div>
      </div>

      <div class="card">
        <h3>Indicators of Compromise (IOCs)</h3>
        <ul class="ioc-list">
          <li v-for="ioc in event.iocs" :key="ioc">{{ ioc }}</li>
        </ul>
      </div>

      <div class="card">
        <h3>MITRE ATT&CK</h3>
        <ul class="mitre-list">
          <li v-for="technique in event.mitre" :key="technique">{{ technique }}</li>
        </ul>
      </div>

      <div class="card">
        <h3>Affected Assets</h3>
        <ul class="asset-list">
          <li v-for="asset in event.affectedAssets" :key="asset">{{ asset }}</li>
        </ul>
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
const event = ref(null)

onMounted(async () => {
  try {
    event.value = await xdrStore.getEventById(route.params.id)
  } catch (error) {
    console.error('Failed to load event:', error)
  }
})
</script>

<style scoped>
.event-detail {
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
  grid-template-columns: repeat(2, 1fr);
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
  color: #1f2937;
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

.value {
  color: #1f2937;
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

.ioc-list, .mitre-list, .asset-list {
  list-style: none;
  padding: 0;
}

.ioc-list li, .mitre-list li, .asset-list li {
  padding: 0.5rem;
  background: #f9fafb;
  margin-bottom: 0.5rem;
  border-radius: 6px;
  font-family: monospace;
}
</style>
