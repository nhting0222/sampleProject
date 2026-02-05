import axios from 'axios'

// API Base URL
const API_BASE_URL = 'http://127.0.0.1:8000/api'

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - Add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('xdr_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - Handle errors with standardized format
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Log error for debugging
    console.error('API Error:', {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      data: error.response?.data
    })

    // Handle 401 Unauthorized
    if (error.response?.status === 401) {
      localStorage.removeItem('xdr_token')
      localStorage.removeItem('xdr_user')
      // Redirect to login if not already there
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }

    // Handle 403 Forbidden
    if (error.response?.status === 403) {
      console.warn('Permission denied:', error.config?.url)
    }

    return Promise.reject(error)
  }
)

// ========== Auth API ==========

export const authAPI = {
  login: (username, password) => {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)
    return axios.post(`${API_BASE_URL}/auth/login`, formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  },
  loginJson: (username, password) => {
    return axios.post(`${API_BASE_URL}/auth/login/json`, { username, password })
  },
  me: () => {
    return apiClient.get('/auth/me')
  },
  refresh: () => {
    return apiClient.post('/auth/refresh')
  },
  register: (userData) => {
    return apiClient.post('/auth/register', userData)
  },
}

// ========== Events API ==========

export const eventsAPI = {
  getAll: (params = {}) => {
    return apiClient.get('/events', { params })
  },
  getById: (id) => {
    return apiClient.get(`/events/${id}`)
  },
  create: (data) => {
    return apiClient.post('/events', data)
  },
  update: (id, data) => {
    return apiClient.put(`/events/${id}`, data)
  },
  delete: (id) => {
    return apiClient.delete(`/events/${id}`)
  },
}

// ========== Incidents API ==========

export const incidentsAPI = {
  getAll: (params = {}) => {
    return apiClient.get('/incidents', { params })
  },
  getById: (id) => {
    return apiClient.get(`/incidents/${id}`)
  },
  create: (data) => {
    return apiClient.post('/incidents', data)
  },
  update: (id, data) => {
    return apiClient.put(`/incidents/${id}`, data)
  },
}

// ========== Assets API ==========

export const assetsAPI = {
  getAll: (params = {}) => {
    return apiClient.get('/assets', { params })
  },
  getById: (id) => {
    return apiClient.get(`/assets/${id}`)
  },
}

// ========== Alert Rules API ==========

export const alertsAPI = {
  getAll: () => {
    return apiClient.get('/alerts')
  },
  update: (id, data) => {
    return apiClient.put(`/alerts/${id}`, data)
  },
}

// ========== Dashboard API ==========

export const dashboardAPI = {
  getStats: () => {
    return apiClient.get('/dashboard/stats')
  },
}

export default apiClient
