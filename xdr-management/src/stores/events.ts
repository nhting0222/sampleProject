import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { eventsAPI } from '../utils/api'
import type { SecurityEvent, SecurityEventCreate, SecurityEventUpdate } from '../types'

export const useEventsStore = defineStore('events', () => {
  // State
  const events = ref<SecurityEvent[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const criticalEvents = computed(() =>
    events.value.filter(e => e.severity === 'critical')
  )

  const eventsByStatus = computed(() => (status: string) =>
    events.value.filter(e => e.status === status)
  )

  const eventCount = computed(() => events.value.length)

  // Actions
  const fetchEvents = async (params: { severity?: string; status?: string; search?: string } = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await eventsAPI.getAll(params)
      events.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch events'
      console.error('Failed to fetch events:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const getEventById = async (id: string): Promise<SecurityEvent> => {
    // Check cache first
    const cachedEvent = events.value.find(e => e.id === id)
    if (cachedEvent) return cachedEvent

    try {
      const response = await eventsAPI.getById(id)
      return response.data
    } catch (err) {
      console.error('Failed to fetch event:', err)
      throw err
    }
  }

  const createEvent = async (data: SecurityEventCreate): Promise<SecurityEvent> => {
    try {
      const response = await eventsAPI.create(data)
      events.value.unshift(response.data)
      return response.data
    } catch (err) {
      console.error('Failed to create event:', err)
      throw err
    }
  }

  const updateEventStatus = async (id: string, status: string): Promise<SecurityEvent> => {
    try {
      const response = await eventsAPI.update(id, { status: status as any })
      const event = events.value.find(e => e.id === id)
      if (event) {
        event.status = status as any
      }
      return response.data
    } catch (err) {
      console.error('Failed to update event:', err)
      throw err
    }
  }

  const deleteEvent = async (id: string): Promise<void> => {
    try {
      await eventsAPI.delete(id)
      events.value = events.value.filter(e => e.id !== id)
    } catch (err) {
      console.error('Failed to delete event:', err)
      throw err
    }
  }

  const addEventFromWebSocket = (event: SecurityEvent) => {
    // Add new event at the beginning
    events.value.unshift(event)
  }

  return {
    // State
    events,
    loading,
    error,

    // Getters
    criticalEvents,
    eventsByStatus,
    eventCount,

    // Actions
    fetchEvents,
    getEventById,
    createEvent,
    updateEventStatus,
    deleteEvent,
    addEventFromWebSocket
  }
})
