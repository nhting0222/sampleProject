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
      <div class="user-menu" v-if="authStore.isAuthenticated">
        <div class="user-info" @click="toggleMenu">
          <div class="user-avatar">
            {{ userInitials }}
          </div>
          <div class="user-details">
            <span class="user-name">{{ authStore.user?.full_name }}</span>
            <span class="user-role" :class="authStore.user?.role">{{ authStore.user?.role }}</span>
          </div>
          <svg class="dropdown-icon" :class="{ open: menuOpen }" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </div>
        <div class="dropdown-menu" v-if="menuOpen">
          <div class="menu-item">
            <span class="menu-label">Email</span>
            <span class="menu-value">{{ authStore.user?.email }}</span>
          </div>
          <div class="menu-divider"></div>
          <button class="logout-btn" @click="handleLogout">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
              <polyline points="16 17 21 12 16 7"></polyline>
              <line x1="21" y1="12" x2="9" y2="12"></line>
            </svg>
            Logout
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const currentTime = ref(new Date().toLocaleTimeString())
const threatLevel = ref('high')
const menuOpen = ref(false)

const pageTitle = computed(() => {
  const titles = {
    'Dashboard': '🎯 Security Operations Dashboard',
    'Events': '🚨 Security Events',
    'EventDetail': '🔍 Event Details',
    'Incidents': '📋 Incident Management',
    'IncidentDetail': '🎫 Incident Details',
    'Assets': '💻 Asset Management',
    'Alerts': '⚠️ Alert Rules',
    'Reports': '📄 Security Reports',
    'ThreatMap': '🌍 Threat Map'
  }
  return titles[route.name] || 'XDR Platform'
})

const userInitials = computed(() => {
  const name = authStore.user?.full_name || ''
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
})

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

// Close menu when clicking outside
const handleClickOutside = (e) => {
  if (!e.target.closest('.user-menu')) {
    menuOpen.value = false
  }
}

let interval
onMounted(() => {
  interval = setInterval(() => {
    currentTime.value = new Date().toLocaleTimeString()
  }, 1000)
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  if (interval) clearInterval(interval)
  document.removeEventListener('click', handleClickOutside)
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
  gap: 1.5rem;
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

.user-menu {
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.user-info:hover {
  background: #f3f4f6;
}

.user-avatar {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 0.85rem;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 0.9rem;
  font-weight: 500;
  color: #1f2937;
}

.user-role {
  font-size: 0.75rem;
  text-transform: capitalize;
  padding: 2px 6px;
  border-radius: 4px;
  width: fit-content;
}

.user-role.admin {
  background: rgba(239, 68, 68, 0.1);
  color: #dc2626;
}

.user-role.analyst {
  background: rgba(234, 179, 8, 0.1);
  color: #ca8a04;
}

.user-role.viewer {
  background: rgba(34, 197, 94, 0.1);
  color: #16a34a;
}

.dropdown-icon {
  color: #6b7280;
  transition: transform 0.2s;
}

.dropdown-icon.open {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  min-width: 200px;
  padding: 0.5rem;
  z-index: 1000;
}

.menu-item {
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.menu-label {
  font-size: 0.75rem;
  color: #6b7280;
}

.menu-value {
  font-size: 0.85rem;
  color: #1f2937;
}

.menu-divider {
  height: 1px;
  background: #e5e7eb;
  margin: 0.25rem 0;
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  border: none;
  background: none;
  color: #dc2626;
  font-size: 0.9rem;
  cursor: pointer;
  border-radius: 6px;
  transition: background 0.2s;
}

.logout-btn:hover {
  background: #fee2e2;
}
</style>
