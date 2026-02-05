<template>
  <div class="incidents">
    <div class="card">
      <table class="incidents-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Severity</th>
            <th>Status</th>
            <th>Assignee</th>
            <th>Affected Systems</th>
            <th>Created</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="incident in incidents"
            :key="incident.id"
            @click="viewDetail(incident.id)"
            class="incident-row"
          >
            <td class="incident-id">{{ incident.id }}</td>
            <td>{{ incident.title }}</td>
            <td>
              <span class="severity-badge" :class="incident.severity">
                {{ incident.severity }}
              </span>
            </td>
            <td>
              <span class="status-badge" :class="incident.status">
                {{ incident.status.replace('_', ' ') }}
              </span>
            </td>
            <td>{{ incident.assignee }}</td>
            <td>{{ incident.affectedSystems }}</td>
            <td>{{ formatTime(incident.createdAt) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useXdrStore } from '../stores/xdr'
import dayjs from 'dayjs'

const router = useRouter()
const xdrStore = useXdrStore()

const incidents = computed(() => xdrStore.incidentsList)

// Load incidents on mount
onMounted(async () => {
  await xdrStore.fetchIncidents()
})

const formatTime = (timestamp) => {
  return dayjs(timestamp).format('YYYY-MM-DD HH:mm')
}

const viewDetail = (id) => {
  router.push(`/incidents/${id}`)
}
</script>

<style scoped>
.incidents {
  padding: 2rem;
}

.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
}

.incidents-table {
  width: 100%;
  border-collapse: collapse;
}

.incidents-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 2px solid #e5e7eb;
  background: #f9fafb;
}

.incidents-table td {
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.incident-row {
  cursor: pointer;
  transition: background 0.2s;
}

.incident-row:hover {
  background: #f9fafb;
}

.incident-id {
  font-family: monospace;
  color: #2563eb;
  font-weight: 600;
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

.severity-badge.high {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.in_progress {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.resolved {
  background: #d1fae5;
  color: #065f46;
}
</style>

/* Responsive */
@media (max-width: 1024px) {
  .incidents {
    padding: 1.5rem;
  }
}

@media (max-width: 768px) {
  .incidents {
    padding: 1rem;
  }

  .card {
    overflow-x: auto;
  }

  .incidents-table {
    min-width: 900px;
  }

  .incidents-table th,
  .incidents-table td {
    padding: 0.75rem;
    font-size: 0.85rem;
  }

  .severity-badge,
  .status-badge {
    font-size: 0.7rem;
    padding: 0.2rem 0.6rem;
  }
}
