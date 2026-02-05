import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '../stores/auth'

// Mock the API
vi.mock('../utils/api', () => ({
  authAPI: {
    login: vi.fn(),
    me: vi.fn(),
    refresh: vi.fn()
  }
}))

import { authAPI } from '../utils/api'

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.getItem.mockReturnValue(null)
    localStorage.setItem.mockClear()
    localStorage.removeItem.mockClear()
  })

  describe('Initial State', () => {
    it('should have null user initially', () => {
      const store = useAuthStore()
      expect(store.user).toBeNull()
    })

    it('should not be authenticated initially', () => {
      const store = useAuthStore()
      expect(store.isAuthenticated).toBe(false)
    })

    it('should not be admin initially', () => {
      const store = useAuthStore()
      expect(store.isAdmin).toBe(false)
    })
  })

  describe('Login', () => {
    it('should login successfully', async () => {
      const mockResponse = {
        data: {
          access_token: 'test-token',
          user: {
            id: 'USR-001',
            username: 'admin',
            email: 'admin@xdr.local',
            full_name: 'System Administrator',
            role: 'admin'
          }
        }
      }
      authAPI.login.mockResolvedValue(mockResponse)

      const store = useAuthStore()
      await store.login('admin', 'admin123')

      expect(store.isAuthenticated).toBe(true)
      expect(store.user.username).toBe('admin')
      expect(store.token).toBe('test-token')
      expect(localStorage.setItem).toHaveBeenCalledWith('xdr_token', 'test-token')
    })

    it('should handle login failure', async () => {
      authAPI.login.mockRejectedValue({
        response: { data: { detail: 'Invalid credentials' } }
      })

      const store = useAuthStore()

      await expect(store.login('admin', 'wrong')).rejects.toBeDefined()
      expect(store.error).toBe('Invalid credentials')
      expect(store.isAuthenticated).toBe(false)
    })
  })

  describe('Logout', () => {
    it('should clear state on logout', async () => {
      const store = useAuthStore()
      store.token = 'test-token'
      store.user = { username: 'admin', role: 'admin' }

      store.logout()

      expect(store.token).toBeNull()
      expect(store.user).toBeNull()
      expect(store.isAuthenticated).toBe(false)
      expect(localStorage.removeItem).toHaveBeenCalledWith('xdr_token')
      expect(localStorage.removeItem).toHaveBeenCalledWith('xdr_user')
    })
  })

  describe('Role Checks', () => {
    it('should identify admin correctly', () => {
      const store = useAuthStore()
      store.user = { role: 'admin' }

      expect(store.isAdmin).toBe(true)
      expect(store.isAnalyst).toBe(true)
    })

    it('should identify analyst correctly', () => {
      const store = useAuthStore()
      store.user = { role: 'analyst' }

      expect(store.isAdmin).toBe(false)
      expect(store.isAnalyst).toBe(true)
    })

    it('should identify viewer correctly', () => {
      const store = useAuthStore()
      store.user = { role: 'viewer' }

      expect(store.isAdmin).toBe(false)
      expect(store.isAnalyst).toBe(false)
    })
  })
})
