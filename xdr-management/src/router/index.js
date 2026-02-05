import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Events from '../views/Events.vue'
import EventDetail from '../views/EventDetail.vue'
import Incidents from '../views/Incidents.vue'
import IncidentDetail from '../views/IncidentDetail.vue'
import Assets from '../views/Assets.vue'
import Alerts from '../views/Alerts.vue'
import Reports from '../views/Reports.vue'
import ThreatMap from '../views/ThreatMap.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/events',
    name: 'Events',
    component: Events
  },
  {
    path: '/events/:id',
    name: 'EventDetail',
    component: EventDetail
  },
  {
    path: '/incidents',
    name: 'Incidents',
    component: Incidents
  },
  {
    path: '/incidents/:id',
    name: 'IncidentDetail',
    component: IncidentDetail
  },
  {
    path: '/assets',
    name: 'Assets',
    component: Assets
  },
  {
    path: '/alerts',
    name: 'Alerts',
    component: Alerts
  },
  {
    path: '/reports',
    name: 'Reports',
    component: Reports
  },
  {
    path: '/threat-map',
    name: 'ThreatMap',
    component: ThreatMap
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
