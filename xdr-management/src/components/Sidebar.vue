<template>
  <aside class="sidebar">
    <div class="logo">
      <h1>🛡️ XDR Platform</h1>
    </div>

    <nav class="nav-menu">
      <router-link to="/" class="nav-item">
        <span class="icon">📊</span>
        <span>Dashboard</span>
      </router-link>
      <router-link to="/events" class="nav-item">
        <span class="icon">🚨</span>
        <span>Security Events</span>
        <span v-if="criticalCount > 0" class="badge">{{ criticalCount }}</span>
      </router-link>
      <router-link to="/incidents" class="nav-item">
        <span class="icon">📋</span>
        <span>Incidents</span>
        <span v-if="activeCount > 0" class="badge warning">{{ activeCount }}</span>
      </router-link>
      <router-link to="/assets" class="nav-item">
        <span class="icon">💻</span>
        <span>Assets</span>
      </router-link>
      <router-link to="/threat-map" class="nav-item">
        <span class="icon">🗺️</span>
        <span>Threat Map</span>
      </router-link>
      <router-link to="/alerts" class="nav-item">
        <span class="icon">⚠️</span>
        <span>Alert Rules</span>
      </router-link>
      <router-link to="/reports" class="nav-item">
        <span class="icon">📄</span>
        <span>Reports</span>
      </router-link>
    </nav>

    <div class="sidebar-footer">
      <div class="user-info">
        <div class="avatar">👤</div>
        <div class="user-details">
          <div class="name">SOC Analyst</div>
          <div class="role">Administrator</div>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useXdrStore } from '../stores/xdr'

const xdrStore = useXdrStore()

const criticalCount = computed(() => xdrStore.criticalEvents.length)
const activeCount = computed(() => xdrStore.activeIncidents.length)
</script>

<style scoped>
.sidebar {
  width: 260px;
  background: #1a1d29;
  color: white;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
}

.logo {
  padding: 1.5rem;
  border-bottom: 1px solid #2a2d3a;
}

.logo h1 {
  font-size: 1.3rem;
  margin: 0;
  font-weight: 700;
}

.nav-menu {
  flex: 1;
  padding: 1rem 0;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 0.9rem 1.5rem;
  color: #a0a8b8;
  text-decoration: none;
  transition: all 0.3s;
  position: relative;
  gap: 0.8rem;
}

.nav-item:hover {
  background: #252835;
  color: white;
}

.nav-item.router-link-active {
  background: #2563eb;
  color: white;
}

.nav-item .icon {
  font-size: 1.3rem;
}

.badge {
  margin-left: auto;
  background: #ef4444;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.badge.warning {
  background: #f59e0b;
}

.sidebar-footer {
  border-top: 1px solid #2a2d3a;
  padding: 1rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #2563eb;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.user-details {
  flex: 1;
}

.name {
  font-weight: 600;
  font-size: 0.9rem;
}

.role {
  font-size: 0.75rem;
  color: #a0a8b8;
}
</style>
