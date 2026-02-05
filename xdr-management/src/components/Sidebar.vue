<template>
  <div>
    <!-- Mobile Menu Button -->
    <button class="mobile-menu-btn" @click="toggleSidebar" v-if="isMobile">
      <span class="hamburger"></span>
    </button>

    <!-- Overlay for mobile -->
    <div class="sidebar-overlay" :class="{ active: isOpen }" @click="closeSidebar" v-if="isMobile"></div>

    <aside class="sidebar" :class="{ open: isOpen }">
      <div class="logo">
        <h1>🛡️ XDR Platform</h1>
        <button class="close-btn" @click="closeSidebar" v-if="isMobile">×</button>
      </div>

      <nav class="nav-menu" @click="handleNavClick">
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useXdrStore } from '../stores/xdr'

const xdrStore = useXdrStore()

const criticalCount = computed(() => xdrStore.criticalEvents.length)
const activeCount = computed(() => xdrStore.activeIncidents.length)

const isOpen = ref(false)
const isMobile = ref(false)

const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
  if (!isMobile.value) {
    isOpen.value = false
  }
}

const toggleSidebar = () => {
  isOpen.value = !isOpen.value
}

const closeSidebar = () => {
  isOpen.value = false
}

const handleNavClick = () => {
  if (isMobile.value) {
    closeSidebar()
  }
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
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

/* Mobile Menu Button */
.mobile-menu-btn {
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 1001;
  background: #1a1d29;
  border: none;
  padding: 0.75rem;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  display: none;
}

.hamburger {
  display: block;
  width: 24px;
  height: 2px;
  background: white;
  position: relative;
}

.hamburger::before,
.hamburger::after {
  content: '';
  position: absolute;
  width: 24px;
  height: 2px;
  background: white;
  left: 0;
}

.hamburger::before {
  top: -8px;
}

.hamburger::after {
  bottom: -8px;
}

.sidebar-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
  opacity: 0;
  transition: opacity 0.3s;
}

.sidebar-overlay.active {
  opacity: 1;
}

.close-btn {
  display: none;
  background: none;
  border: none;
  color: white;
  font-size: 2rem;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

/* Tablet */
@media (max-width: 1024px) {
  .sidebar {
    width: 240px;
  }

  .logo h1 {
    font-size: 1.2rem;
  }

  .nav-item {
    padding: 0.8rem 1.2rem;
  }
}

/* Mobile */
@media (max-width: 768px) {
  .mobile-menu-btn {
    display: block;
  }

  .sidebar {
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    z-index: 1000;
  }

  .sidebar.open {
    transform: translateX(0);
  }

  .sidebar-overlay {
    display: block;
  }

  .logo {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .close-btn {
    display: block;
  }
}
</style>
