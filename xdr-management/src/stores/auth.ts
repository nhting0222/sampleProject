import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '../utils/api'
import type { User, UserRole } from '../types'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('xdr_token'))
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isAnalyst = computed(() => ['admin', 'analyst'].includes(user.value?.role || ''))
  const userRole = computed<UserRole | null>(() => user.value?.role || null)

  // Actions
  const login = async (username: string, password: string) => {
    loading.value = true
    error.value = null
    try {
      const response = await authAPI.login(username, password)
      const data = response.data

      token.value = data.access_token
      user.value = data.user
      localStorage.setItem('xdr_token', data.access_token)
      localStorage.setItem('xdr_user', JSON.stringify(data.user))

      return data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Login failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('xdr_token')
    localStorage.removeItem('xdr_user')
  }

  const checkAuth = async (): Promise<boolean> => {
    if (!token.value) return false

    try {
      const response = await authAPI.me()
      user.value = response.data
      return true
    } catch (err) {
      logout()
      return false
    }
  }

  const refreshToken = async (): Promise<boolean> => {
    try {
      const response = await authAPI.refresh()
      token.value = response.data.access_token
      localStorage.setItem('xdr_token', response.data.access_token)
      return true
    } catch (err) {
      logout()
      return false
    }
  }

  // Initialize user from localStorage
  const initializeAuth = () => {
    const storedUser = localStorage.getItem('xdr_user')
    if (storedUser) {
      try {
        user.value = JSON.parse(storedUser) as User
      } catch (e) {
        localStorage.removeItem('xdr_user')
      }
    }
  }

  // Initialize on store creation
  initializeAuth()

  return {
    // State
    user,
    token,
    loading,
    error,

    // Getters
    isAuthenticated,
    isAdmin,
    isAnalyst,
    userRole,

    // Actions
    login,
    logout,
    checkAuth,
    refreshToken,
    initializeAuth
  }
})
