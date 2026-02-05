import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { dashboardAPI } from '../utils/api'
import type { DashboardStats } from '../types'

export const useDashboardStore = defineStore('dashboard', () => {
  // State
  const stats = ref<DashboardStats | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const lastUpdated = ref<Date | null>(null)

  // Getters
  const threatLevel = computed(() => stats.value?.threatLevel || 'unknown')

  const isCritical = computed(() =>
    stats.value?.threatLevel === 'critical' ||
    (stats.value?.criticalEvents || 0) > 0
  )

  const overviewStats = computed(() => {
    if (!stats.value) return null
    return {
      events: stats.value.totalEvents,
      critical: stats.value.criticalEvents,
      incidents: stats.value.activeIncidents,
      assets: stats.value.assetsMonitored
    }
  })

  // Actions
  const fetchStats = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await dashboardAPI.getStats()
      stats.value = response.data
      lastUpdated.value = new Date()
      return response.data
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch dashboard stats'
      console.error('Failed to fetch dashboard stats:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const refreshStats = async () => {
    // Only refresh if more than 30 seconds since last update
    if (lastUpdated.value) {
      const elapsed = Date.now() - lastUpdated.value.getTime()
      if (elapsed < 30000) return stats.value
    }
    return fetchStats()
  }

  return {
    // State
    stats,
    loading,
    error,
    lastUpdated,

    // Getters
    threatLevel,
    isCritical,
    overviewStats,

    // Actions
    fetchStats,
    refreshStats
  }
})
