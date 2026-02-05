import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Dashboard from '../views/Dashboard.vue'
import Events from '../views/Events.vue'
import EventDetail from '../views/EventDetail.vue'
import Incidents from '../views/Incidents.vue'
import IncidentDetail from '../views/IncidentDetail.vue'
import Assets from '../views/Assets.vue'
import Alerts from '../views/Alerts.vue'
import Reports from '../views/Reports.vue'
import ThreatMap from '../views/ThreatMap.vue'
import Login from '../views/Login.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/events',
    name: 'Events',
    component: Events,
    meta: { requiresAuth: true }
  },
  {
    path: '/events/:id',
    name: 'EventDetail',
    component: EventDetail,
    meta: { requiresAuth: true }
  },
  {
    path: '/incidents',
    name: 'Incidents',
    component: Incidents,
    meta: { requiresAuth: true }
  },
  {
    path: '/incidents/:id',
    name: 'IncidentDetail',
    component: IncidentDetail,
    meta: { requiresAuth: true }
  },
  {
    path: '/assets',
    name: 'Assets',
    component: Assets,
    meta: { requiresAuth: true }
  },
  {
    path: '/alerts',
    name: 'Alerts',
    component: Alerts,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/reports',
    name: 'Reports',
    component: Reports,
    meta: { requiresAuth: true }
  },
  {
    path: '/threat-map',
    name: 'ThreatMap',
    component: ThreatMap,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }

  // Check if route requires admin role
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next({ name: 'Dashboard' })
    return
  }

  // Redirect to dashboard if already authenticated and trying to access login
  if (to.name === 'Login' && authStore.isAuthenticated) {
    next({ name: 'Dashboard' })
    return
  }

  next()
})

export default router
