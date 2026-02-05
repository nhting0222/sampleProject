<template>
  <header class="header">
    <div class="header-left">
      <h2>{{ pageTitle }}</h2>
    </div>
    <div class="header-right">
      <div class="threat-level" :class="`level-${threatLevel}`">
        <span class="icon">🔥</span>
        <span>Threat Level: <strong>{{ threatLevel.toUpperCase() }}</strong></span>
      </div>
      <div class="last-update">
        Last updated: {{ currentTime }}
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const currentTime = ref(new Date().toLocaleTimeString())
const threatLevel = ref('high')

const pageTitle = computed(() => {
  const titles = {
    'Dashboard': '🎯 Security Operations Dashboard',
    'Events': '🚨 Security Events',
    'EventDetail': '🔍 Event Details',
    'Incidents': '📋 Incident Management',
    'IncidentDetail': '🎫 Incident Details',
    'Assets': '💻 Asset Management',
    'Alerts': '⚠️ Alert Rules',
    'Reports': '📄 Security Reports'
  }
  return titles[route.name] || 'XDR Platform'
})

let interval
onMounted(() => {
  interval = setInterval(() => {
    currentTime.value = new Date().toLocaleTimeString()
  }, 1000)
})

onUnmounted(() => {
  if (interval) clearInterval(interval)
})
</script>

<style scoped>
.header {
  height: 70px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left h2 {
  font-size: 1.4rem;
  margin: 0;
  color: #1f2937;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.threat-level {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
}

.threat-level.level-critical {
  background: #fee2e2;
  color: #991b1b;
}

.threat-level.level-high {
  background: #fef3c7;
  color: #92400e;
}

.threat-level.level-medium {
  background: #dbeafe;
  color: #1e40af;
}

.threat-level.level-low {
  background: #d1fae5;
  color: #065f46;
}

.last-update {
  font-size: 0.85rem;
  color: #6b7280;
}
</style>
