<template>
  <div class="assets">
    <div class="card">
      <table class="assets-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Type</th>
            <th>OS</th>
            <th>IP Address</th>
            <th>Department</th>
            <th>Status</th>
            <th>Risk Score</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="asset in assets" :key="asset.id" class="asset-row">
            <td class="asset-id">{{ asset.id }}</td>
            <td>{{ asset.name }}</td>
            <td>{{ asset.type }}</td>
            <td>{{ asset.os }}</td>
            <td class="ip">{{ asset.ip }}</td>
            <td>{{ asset.department }}</td>
            <td>
              <span class="status-badge" :class="asset.status">{{ asset.status }}</span>
            </td>
            <td>
              <span class="risk-score" :class="getRiskClass(asset.riskScore)">
                {{ asset.riskScore }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useXdrStore } from '../stores/xdr'

const xdrStore = useXdrStore()
const assets = computed(() => xdrStore.assetsList)

// Load assets on mount
onMounted(async () => {
  await xdrStore.fetchAssets()
})

const getRiskClass = (score) => {
  if (score >= 80) return 'critical'
  if (score >= 50) return 'high'
  if (score >= 30) return 'medium'
  return 'low'
}
</script>

<style scoped>
.assets {
  padding: 2rem;
  min-height: 100%;
  width: 100%;
  background: #f9fafb;
}

.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
}

.assets-table {
  width: 100%;
  border-collapse: collapse;
}

.assets-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 2px solid #e5e7eb;
  background: #f9fafb;
}

.assets-table td {
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.asset-row:hover {
  background: #f9fafb;
}

.asset-id {
  font-family: monospace;
  color: #2563eb;
  font-weight: 600;
}

.ip {
  font-family: monospace;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: capitalize;
}

.status-badge.healthy {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.compromised {
  background: #fee2e2;
  color: #991b1b;
}

.status-badge.investigating {
  background: #fef3c7;
  color: #92400e;
}

.risk-score {
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  font-weight: 700;
}

.risk-score.critical {
  background: #fee2e2;
  color: #991b1b;
}

.risk-score.high {
  background: #fef3c7;
  color: #92400e;
}

.risk-score.medium {
  background: #dbeafe;
  color: #1e40af;
}

.risk-score.low {
  background: #d1fae5;
  color: #065f46;
}
</style>

/* Responsive */
@media (max-width: 1024px) {
  .assets {
    padding: 1.5rem;
  }
}

@media (max-width: 768px) {
  .assets {
    padding: 1rem;
  }

  .card {
    overflow-x: auto;
  }

  .assets-table {
    min-width: 1000px;
  }

  .assets-table th,
  .assets-table td {
    padding: 0.75rem;
    font-size: 0.85rem;
  }

  .status-badge {
    font-size: 0.7rem;
    padding: 0.2rem 0.6rem;
  }

  .risk-score {
    padding: 0.4rem 0.6rem;
    font-size: 0.9rem;
  }
}
