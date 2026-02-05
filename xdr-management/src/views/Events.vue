<template>
  <div class="events">
    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-box">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="🔍 Search events..."
          class="search-input"
        />
      </div>
      <select v-model="severityFilter" class="filter-select">
        <option value="">All Severities</option>
        <option value="critical">Critical</option>
        <option value="high">High</option>
        <option value="medium">Medium</option>
        <option value="low">Low</option>
      </select>
      <select v-model="statusFilter" class="filter-select">
        <option value="">All Status</option>
        <option value="investigating">Investigating</option>
        <option value="monitoring">Monitoring</option>
        <option value="resolved">Resolved</option>
      </select>
    </div>

    <!-- Results -->
    <div class="results-info">
      <span>{{ filteredEvents.length }} events found</span>
    </div>

    <!-- Events Table -->
    <div class="card">
      <table class="events-table">
        <thead>
          <tr>
            <th>Severity</th>
            <th>ID</th>
            <th>Type</th>
            <th>Source</th>
            <th>Description</th>
            <th>Time</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="event in filteredEvents"
            :key="event.id"
            @click="viewDetail(event.id)"
            class="event-row"
          >
            <td>
              <span class="severity-badge" :class="event.severity">
                {{ event.severity }}
              </span>
            </td>
            <td class="event-id">{{ event.id }}</td>
            <td>{{ event.type }}</td>
            <td>{{ event.source }}</td>
            <td class="description">{{ event.description }}</td>
            <td>{{ formatTime(event.timestamp) }}</td>
            <td>
              <span class="status-badge" :class="event.status">
                {{ event.status }}
              </span>
            </td>
            <td>
              <button @click.stop="createIncident(event)" class="btn-action">
                Create Incident
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useXdrStore } from '../stores/xdr'
import dayjs from 'dayjs'

const router = useRouter()
const xdrStore = useXdrStore()

const searchQuery = ref('')
const severityFilter = ref('')
const statusFilter = ref('')

// Load events on mount
onMounted(async () => {
  await xdrStore.fetchEvents()
})

const filteredEvents = computed(() => {
  let result = xdrStore.events

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(e =>
      e.type.toLowerCase().includes(query) ||
      e.source.toLowerCase().includes(query) ||
      e.description.toLowerCase().includes(query)
    )
  }

  if (severityFilter.value) {
    result = result.filter(e => e.severity === severityFilter.value)
  }

  if (statusFilter.value) {
    result = result.filter(e => e.status === statusFilter.value)
  }

  return result
})

const formatTime = (timestamp) => {
  return dayjs(timestamp).format('YYYY-MM-DD HH:mm:ss')
}

const viewDetail = (id) => {
  router.push(`/events/${id}`)
}

const createIncident = async (event) => {
  try {
    const incident = await xdrStore.createIncident({
      title: `${event.type} - ${event.source}`,
      severity: event.severity,
      assignee: 'Unassigned',
      description: event.description,
      affectedSystems: event.affectedAssets.length,
      relatedEvents: [event.id]
    })
    alert(`Incident ${incident.id} created successfully!`)
    router.push(`/incidents/${incident.id}`)
  } catch (error) {
    alert('Failed to create incident')
  }
}
</script>

<style scoped>
.events {
  padding: 2rem;
}

.filters-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.search-box {
  flex: 1;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.95rem;
}

.filter-select {
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: white;
  cursor: pointer;
}

.results-info {
  margin-bottom: 1rem;
  color: #6b7280;
  font-size: 0.9rem;
}

.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
}

.events-table {
  width: 100%;
  border-collapse: collapse;
}

.events-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 2px solid #e5e7eb;
  background: #f9fafb;
}

.events-table td {
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.event-row {
  cursor: pointer;
  transition: background 0.2s;
}

.event-row:hover {
  background: #f9fafb;
}

.event-id {
  font-family: monospace;
  color: #2563eb;
  font-weight: 600;
}

.description {
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.severity-badge {
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

.severity-badge.medium {
  background: #dbeafe;
  color: #1e40af;
}

.severity-badge.low {
  background: #d1fae5;
  color: #065f46;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: capitalize;
}

.status-badge.investigating {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.monitoring {
  background: #dbeafe;
  color: #1e40af;
}

.status-badge.resolved {
  background: #d1fae5;
  color: #065f46;
}

.btn-action {
  padding: 0.5rem 1rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  transition: background 0.2s;
}

.btn-action:hover {
  background: #1d4ed8;
}

/* Responsive */
@media (max-width: 1024px) {
  .events {
    padding: 1.5rem;
  }

  .filters {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .events {
    padding: 1rem;
  }

  .filters {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .filter-group input,
  .filter-group select {
    font-size: 14px;
  }

  .card {
    overflow-x: auto;
  }

  .events-table {
    min-width: 800px;
  }

  .events-table th,
  .events-table td {
    padding: 0.75rem;
    font-size: 0.85rem;
  }

  .severity-badge,
  .status-badge {
    font-size: 0.7rem;
    padding: 0.2rem 0.6rem;
  }

  .btn-action {
    font-size: 0.8rem;
    padding: 0.4rem 0.8rem;
  }
}
</style>
