import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { incidentsAPI } from '../utils/api'
import type { Incident, IncidentCreate, IncidentUpdate } from '../types'

export const useIncidentsStore = defineStore('incidents', () => {
  // State
  const incidents = ref<Incident[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const activeIncidents = computed(() =>
    incidents.value.filter(i => i.status === 'in_progress')
  )

  const resolvedIncidents = computed(() =>
    incidents.value.filter(i => i.status === 'resolved')
  )

  const incidentCount = computed(() => incidents.value.length)

  const incidentsBySeverity = computed(() => (severity: string) =>
    incidents.value.filter(i => i.severity === severity)
  )

  // Actions
  const fetchIncidents = async (params: { status?: string } = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await incidentsAPI.getAll(params)
      incidents.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch incidents'
      console.error('Failed to fetch incidents:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const getIncidentById = async (id: string): Promise<Incident> => {
    // Check cache first
    const cachedIncident = incidents.value.find(i => i.id === id)
    if (cachedIncident) return cachedIncident

    try {
      const response = await incidentsAPI.getById(id)
      return response.data
    } catch (err) {
      console.error('Failed to fetch incident:', err)
      throw err
    }
  }

  const createIncident = async (data: IncidentCreate): Promise<Incident> => {
    try {
      const response = await incidentsAPI.create(data)
      incidents.value.unshift(response.data)
      return response.data
    } catch (err) {
      console.error('Failed to create incident:', err)
      throw err
    }
  }

  const updateIncidentStatus = async (id: string, status: string): Promise<Incident> => {
    try {
      const response = await incidentsAPI.update(id, { status: status as any })
      const incident = incidents.value.find(i => i.id === id)
      if (incident) {
        Object.assign(incident, response.data)
      }
      return response.data
    } catch (err) {
      console.error('Failed to update incident:', err)
      throw err
    }
  }

  const assignIncident = async (id: string, assignee: string): Promise<Incident> => {
    try {
      const response = await incidentsAPI.update(id, { assignee })
      const incident = incidents.value.find(i => i.id === id)
      if (incident) {
        incident.assignee = assignee
      }
      return response.data
    } catch (err) {
      console.error('Failed to assign incident:', err)
      throw err
    }
  }

  return {
    // State
    incidents,
    loading,
    error,

    // Getters
    activeIncidents,
    resolvedIncidents,
    incidentCount,
    incidentsBySeverity,

    // Actions
    fetchIncidents,
    getIncidentById,
    createIncident,
    updateIncidentStatus,
    assignIncident
  }
})
