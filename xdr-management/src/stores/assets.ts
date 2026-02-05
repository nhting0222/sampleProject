import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { assetsAPI } from '../utils/api'
import type { Asset } from '../types'

export const useAssetsStore = defineStore('assets', () => {
  // State
  const assets = ref<Asset[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const compromisedAssets = computed(() =>
    assets.value.filter(a => a.status === 'compromised')
  )

  const healthyAssets = computed(() =>
    assets.value.filter(a => a.status === 'healthy')
  )

  const assetCount = computed(() => assets.value.length)

  const highRiskAssets = computed(() =>
    assets.value.filter(a => a.riskScore >= 70)
  )

  const assetsByDepartment = computed(() => {
    const grouped: Record<string, Asset[]> = {}
    assets.value.forEach(asset => {
      if (!grouped[asset.department]) {
        grouped[asset.department] = []
      }
      grouped[asset.department].push(asset)
    })
    return grouped
  })

  // Actions
  const fetchAssets = async (params: { status?: string } = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await assetsAPI.getAll(params)
      assets.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch assets'
      console.error('Failed to fetch assets:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const getAssetById = async (id: string): Promise<Asset> => {
    // Check cache first
    const cachedAsset = assets.value.find(a => a.id === id)
    if (cachedAsset) return cachedAsset

    try {
      const response = await assetsAPI.getById(id)
      return response.data
    } catch (err) {
      console.error('Failed to fetch asset:', err)
      throw err
    }
  }

  return {
    // State
    assets,
    loading,
    error,

    // Getters
    compromisedAssets,
    healthyAssets,
    assetCount,
    highRiskAssets,
    assetsByDepartment,

    // Actions
    fetchAssets,
    getAssetById
  }
})
