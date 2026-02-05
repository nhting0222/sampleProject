// ========== Enums ==========

export type SeverityLevel = 'critical' | 'high' | 'medium' | 'low'
export type EventStatus = 'investigating' | 'monitoring' | 'resolved'
export type IncidentStatus = 'in_progress' | 'monitoring' | 'resolved'
export type AssetStatus = 'healthy' | 'compromised' | 'investigating'
export type UserRole = 'admin' | 'analyst' | 'viewer'

// ========== Security Event ==========

export interface SecurityEvent {
  id: string
  timestamp: string
  severity: SeverityLevel
  type: string
  source: string
  description: string
  status: EventStatus
  affectedAssets: string[]
  iocs: string[]
  mitre: string[]
}

export interface SecurityEventCreate {
  type: string
  source: string
  description: string
  severity: SeverityLevel
  affectedAssets?: string[]
  iocs?: string[]
  mitre?: string[]
}

export interface SecurityEventUpdate {
  status?: EventStatus
  description?: string
}

// ========== Incident ==========

export interface TimelineEntry {
  time: string
  action: string
  user: string
}

export interface Incident {
  id: string
  title: string
  severity: SeverityLevel
  status: IncidentStatus
  createdAt: string
  updatedAt: string
  assignee: string
  description: string
  affectedSystems: number
  relatedEvents: string[]
  timeline: TimelineEntry[]
}

export interface IncidentCreate {
  title: string
  severity: SeverityLevel
  assignee: string
  description: string
  affectedSystems: number
  relatedEvents?: string[]
}

export interface IncidentUpdate {
  status?: IncidentStatus
  assignee?: string
}

// ========== Asset ==========

export interface Asset {
  id: string
  name: string
  type: string
  os: string
  ip: string
  status: AssetStatus
  lastSeen: string
  owner: string
  department: string
  riskScore: number
}

// ========== Alert Rule ==========

export interface AlertRule {
  id: string
  name: string
  severity: SeverityLevel
  enabled: boolean
  conditions: string
  actions: string[]
}

export interface AlertRuleUpdate {
  enabled?: boolean
}

// ========== Dashboard ==========

export interface DashboardStats {
  totalEvents: number
  criticalEvents: number
  activeIncidents: number
  resolvedToday: number
  assetsMonitored: number
  compromisedAssets: number
  averageResponseTime: string
  threatLevel: string
}

// ========== User & Auth ==========

export interface User {
  id: string
  username: string
  email: string
  full_name: string
  role: UserRole
  is_active?: boolean
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

export interface AuthState {
  user: User | null
  token: string | null
  loading: boolean
  error: string | null
}

// ========== API Response ==========

export interface ApiError {
  code: string
  message: string
  details?: Record<string, unknown>
}

export interface ApiErrorResponse {
  success: false
  error: ApiError
  timestamp: string
}

// ========== Toast ==========

export type ToastType = 'success' | 'error' | 'warning' | 'info'

export interface Toast {
  id: number
  message: string
  type: ToastType
  timestamp: number
}

// ========== WebSocket ==========

export interface WebSocketMessage {
  type: 'new_event' | 'new_incident' | 'event_updated' | 'pong'
  data?: SecurityEvent | Incident | Record<string, unknown>
  message?: string
}
