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

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

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
