import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  eventsAPI,
  incidentsAPI,
  assetsAPI,
  alertsAPI,
  dashboardAPI
} from '../utils/api'

export const useXdrStore = defineStore('xdr', () => {
  // State
  const events = ref([])
  const incidentsList = ref([])
  const assetsList = ref([])
  const rules = ref([])
  const stats = ref({})
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const criticalEvents = computed(() => {
    return events.value.filter(e => e.severity === 'critical')
  })

  const activeIncidents = computed(() => {
    return incidentsList.value.filter(i => i.status === 'in_progress')
  })

  const compromisedAssets = computed(() => {
    return assetsList.value.filter(a => a.status === 'compromised')
  })

  // ========== Events Actions ==========

  const fetchEvents = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await eventsAPI.getAll(params)
      events.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('Failed to fetch events:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const getEventById = async (id) => {
    // Check if event is already in store
    const cachedEvent = events.value.find(e => e.id === id)
    if (cachedEvent) return cachedEvent

    // Fetch from API
    try {
      const response = await eventsAPI.getById(id)
      return response.data
    } catch (err) {
      console.error('Failed to fetch event:', err)
      throw err
    }
  }

  const createEvent = async (data) => {
    try {
      const response = await eventsAPI.create(data)
      events.value.unshift(response.data)
      return response.data
    } catch (err) {
      console.error('Failed to create event:', err)
      throw err
    }
  }

  const updateEventStatus = async (id, status) => {
    try {
      const response = await eventsAPI.update(id, { status })
      const event = events.value.find(e => e.id === id)
      if (event) {
        event.status = status
      }
      return response.data
    } catch (err) {
      console.error('Failed to update event:', err)
      throw err
    }
  }

  const deleteEvent = async (id) => {
    try {
      await eventsAPI.delete(id)
      events.value = events.value.filter(e => e.id !== id)
    } catch (err) {
      console.error('Failed to delete event:', err)
      throw err
    }
  }

  // ========== Incidents Actions ==========

  const fetchIncidents = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await incidentsAPI.getAll(params)
      incidentsList.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('Failed to fetch incidents:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const getIncidentById = async (id) => {
    const cachedIncident = incidentsList.value.find(i => i.id === id)
    if (cachedIncident) return cachedIncident

    try {
      const response = await incidentsAPI.getById(id)
      return response.data
    } catch (err) {
      console.error('Failed to fetch incident:', err)
      throw err
    }
  }

  const createIncident = async (data) => {
    try {
      const response = await incidentsAPI.create(data)
      incidentsList.value.unshift(response.data)
      return response.data
    } catch (err) {
      console.error('Failed to create incident:', err)
      throw err
    }
  }

  const updateIncidentStatus = async (id, status) => {
    try {
      const response = await incidentsAPI.update(id, { status })
      const incident = incidentsList.value.find(i => i.id === id)
      if (incident) {
        Object.assign(incident, response.data)
      }
      return response.data
    } catch (err) {
      console.error('Failed to update incident:', err)
      throw err
    }
  }

  // ========== Assets Actions ==========

  const fetchAssets = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await assetsAPI.getAll(params)
      assetsList.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('Failed to fetch assets:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const getAssetById = async (id) => {
    const cachedAsset = assetsList.value.find(a => a.id === id)
    if (cachedAsset) return cachedAsset

    try {
      const response = await assetsAPI.getById(id)
      return response.data
    } catch (err) {
      console.error('Failed to fetch asset:', err)
      throw err
    }
  }

  // ========== Alert Rules Actions ==========

  const fetchAlertRules = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await alertsAPI.getAll()
      rules.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('Failed to fetch alert rules:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateAlertRule = async (id, data) => {
    try {
      const response = await alertsAPI.update(id, data)
      const rule = rules.value.find(r => r.id === id)
      if (rule) {
        Object.assign(rule, response.data)
      }
      return response.data
    } catch (err) {
      console.error('Failed to update alert rule:', err)
      throw err
    }
  }

  // ========== Dashboard Actions ==========

  const fetchDashboardStats = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await dashboardAPI.getStats()
      stats.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('Failed to fetch dashboard stats:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // ========== Initialize Data ==========

  const initializeData = async () => {
    try {
      await Promise.all([
        fetchEvents(),
        fetchIncidents(),
        fetchAssets(),
        fetchAlertRules(),
        fetchDashboardStats()
      ])
    } catch (err) {
      console.error('Failed to initialize data:', err)
    }
  }

  return {
    // State
    events,
    incidentsList,
    assetsList,
    rules,
    stats,
    loading,
    error,

    // Getters
    criticalEvents,
    activeIncidents,
    compromisedAssets,

    // Events Actions
    fetchEvents,
    getEventById,
    createEvent,
    updateEventStatus,
    deleteEvent,

    // Incidents Actions
    fetchIncidents,
    getIncidentById,
    createIncident,
    updateIncidentStatus,

    // Assets Actions
    fetchAssets,
    getAssetById,

    // Alert Rules Actions
    fetchAlertRules,
    updateAlertRule,

    // Dashboard Actions
    fetchDashboardStats,

    // Initialize
    initializeData
  }
})
