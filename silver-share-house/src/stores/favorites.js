import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useFavoritesStore = defineStore('favorites', () => {
  // State
  const favoriteIds = ref([])

  // Load from localStorage on initialization
  const loadFromStorage = () => {
    const stored = localStorage.getItem('silverhouse-favorites')
    if (stored) {
      try {
        favoriteIds.value = JSON.parse(stored)
      } catch (e) {
        console.error('Failed to load favorites:', e)
        favoriteIds.value = []
      }
    }
  }

  // Save to localStorage
  const saveToStorage = () => {
    localStorage.setItem('silverhouse-favorites', JSON.stringify(favoriteIds.value))
  }

  // Getters
  const isFavorite = computed(() => (houseId) => {
    return favoriteIds.value.includes(houseId)
  })

  const favoriteCount = computed(() => favoriteIds.value.length)

  // Actions
  const addFavorite = (houseId) => {
    if (!favoriteIds.value.includes(houseId)) {
      favoriteIds.value.push(houseId)
      saveToStorage()
      return true
    }
    return false
  }

  const removeFavorite = (houseId) => {
    const index = favoriteIds.value.indexOf(houseId)
    if (index > -1) {
      favoriteIds.value.splice(index, 1)
      saveToStorage()
      return true
    }
    return false
  }

  const toggleFavorite = (houseId) => {
    if (isFavorite.value(houseId)) {
      removeFavorite(houseId)
      return false
    } else {
      addFavorite(houseId)
      return true
    }
  }

  const clearFavorites = () => {
    favoriteIds.value = []
    saveToStorage()
  }

  // Initialize
  loadFromStorage()

  return {
    favoriteIds,
    isFavorite,
    favoriteCount,
    addFavorite,
    removeFavorite,
    toggleFavorite,
    clearFavorites
  }
})
