import axios, { AxiosInstance, AxiosResponse } from 'axios'
import type {
  SecurityEvent,
  SecurityEventCreate,
  SecurityEventUpdate,
  Incident,
  IncidentCreate,
  IncidentUpdate,
  Asset,
  AlertRule,
  AlertRuleUpdate,
  DashboardStats,
  LoginResponse,
  User
} from '../types'

// API Base URL
const API_BASE_URL = 'http://127.0.0.1:8000/api'

// Create axios instance
const apiClient: AxiosInstance = axios.create({
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

interface AuthAPI {
  login: (username: string, password: string) => Promise<AxiosResponse<LoginResponse>>
  loginJson: (username: string, password: string) => Promise<AxiosResponse<LoginResponse>>
  me: () => Promise<AxiosResponse<User>>
  refresh: () => Promise<AxiosResponse<LoginResponse>>
  register: (userData: Partial<User> & { password: string }) => Promise<AxiosResponse<User>>
}

export const authAPI: AuthAPI = {
  login: (username: string, password: string) => {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)
    return axios.post<LoginResponse>(`${API_BASE_URL}/auth/login`, formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  },
  loginJson: (username: string, password: string) => {
    return axios.post<LoginResponse>(`${API_BASE_URL}/auth/login/json`, { username, password })
  },
  me: () => {
    return apiClient.get<User>('/auth/me')
  },
  refresh: () => {
    return apiClient.post<LoginResponse>('/auth/refresh')
  },
  register: (userData) => {
    return apiClient.post<User>('/auth/register', userData)
  },
}

// ========== Events API ==========

interface EventsParams {
  severity?: string
  status?: string
  search?: string
}

interface EventsAPI {
  getAll: (params?: EventsParams) => Promise<AxiosResponse<SecurityEvent[]>>
  getById: (id: string) => Promise<AxiosResponse<SecurityEvent>>
  create: (data: SecurityEventCreate) => Promise<AxiosResponse<SecurityEvent>>
  update: (id: string, data: SecurityEventUpdate) => Promise<AxiosResponse<SecurityEvent>>
  delete: (id: string) => Promise<AxiosResponse<{ message: string }>>
}

export const eventsAPI: EventsAPI = {
  getAll: (params = {}) => {
    return apiClient.get<SecurityEvent[]>('/events', { params })
  },
  getById: (id: string) => {
    return apiClient.get<SecurityEvent>(`/events/${id}`)
  },
  create: (data: SecurityEventCreate) => {
    return apiClient.post<SecurityEvent>('/events', data)
  },
  update: (id: string, data: SecurityEventUpdate) => {
    return apiClient.put<SecurityEvent>(`/events/${id}`, data)
  },
  delete: (id: string) => {
    return apiClient.delete<{ message: string }>(`/events/${id}`)
  },
}

// ========== Incidents API ==========

interface IncidentsParams {
  status?: string
}

interface IncidentsAPI {
  getAll: (params?: IncidentsParams) => Promise<AxiosResponse<Incident[]>>
  getById: (id: string) => Promise<AxiosResponse<Incident>>
  create: (data: IncidentCreate) => Promise<AxiosResponse<Incident>>
  update: (id: string, data: IncidentUpdate) => Promise<AxiosResponse<Incident>>
}

export const incidentsAPI: IncidentsAPI = {
  getAll: (params = {}) => {
    return apiClient.get<Incident[]>('/incidents', { params })
  },
  getById: (id: string) => {
    return apiClient.get<Incident>(`/incidents/${id}`)
  },
  create: (data: IncidentCreate) => {
    return apiClient.post<Incident>('/incidents', data)
  },
  update: (id: string, data: IncidentUpdate) => {
    return apiClient.put<Incident>(`/incidents/${id}`, data)
  },
}

// ========== Assets API ==========

interface AssetsParams {
  status?: string
}

interface AssetsAPI {
  getAll: (params?: AssetsParams) => Promise<AxiosResponse<Asset[]>>
  getById: (id: string) => Promise<AxiosResponse<Asset>>
}

export const assetsAPI: AssetsAPI = {
  getAll: (params = {}) => {
    return apiClient.get<Asset[]>('/assets', { params })
  },
  getById: (id: string) => {
    return apiClient.get<Asset>(`/assets/${id}`)
  },
}

// ========== Alert Rules API ==========

interface AlertsAPI {
  getAll: () => Promise<AxiosResponse<AlertRule[]>>
  update: (id: string, data: AlertRuleUpdate) => Promise<AxiosResponse<AlertRule>>
}

export const alertsAPI: AlertsAPI = {
  getAll: () => {
    return apiClient.get<AlertRule[]>('/alerts')
  },
  update: (id: string, data: AlertRuleUpdate) => {
    return apiClient.put<AlertRule>(`/alerts/${id}`, data)
  },
}

// ========== Dashboard API ==========

interface DashboardAPI {
  getStats: () => Promise<AxiosResponse<DashboardStats>>
}

export const dashboardAPI: DashboardAPI = {
  getStats: () => {
    return apiClient.get<DashboardStats>('/dashboard/stats')
  },
}

export default apiClient
