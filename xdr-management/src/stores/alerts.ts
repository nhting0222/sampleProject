import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { alertsAPI } from '../utils/api'
import type { AlertRule } from '../types'

export const useAlertsStore = defineStore('alerts', () => {
  // State
  const rules = ref<AlertRule[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const enabledRules = computed(() =>
    rules.value.filter(r => r.enabled)
  )

  const disabledRules = computed(() =>
    rules.value.filter(r => !r.enabled)
  )

  const ruleCount = computed(() => rules.value.length)

  const rulesBySeverity = computed(() => (severity: string) =>
    rules.value.filter(r => r.severity === severity)
  )

  // Actions
  const fetchAlertRules = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await alertsAPI.getAll()
      rules.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch alert rules'
      console.error('Failed to fetch alert rules:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateAlertRule = async (id: string, data: { enabled?: boolean }): Promise<AlertRule> => {
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

  const toggleRule = async (id: string): Promise<AlertRule> => {
    const rule = rules.value.find(r => r.id === id)
    if (!rule) throw new Error('Rule not found')

    return updateAlertRule(id, { enabled: !rule.enabled })
  }

  return {
    // State
    rules,
    loading,
    error,

    // Getters
    enabledRules,
    disabledRules,
    ruleCount,
    rulesBySeverity,

    // Actions
    fetchAlertRules,
    updateAlertRule,
    toggleRule
  }
})
