// Security Events
export const securityEvents = [
  {
    id: 'EVT-001',
    timestamp: '2026-02-05T10:30:15Z',
    severity: 'critical',
    type: 'Malware Detected',
    source: 'Endpoint-WKS-042',
    description: 'Ransomware activity detected on Windows workstation',
    status: 'investigating',
    affectedAssets: ['WKS-042', 'FILE-SERVER-01'],
    iocs: ['hash:a3f5d...', 'ip:185.220.101.45'],
    mitre: ['T1486 - Data Encrypted for Impact']
  },
  {
    id: 'EVT-002',
    timestamp: '2026-02-05T10:15:42Z',
    severity: 'high',
    type: 'Suspicious Login',
    source: 'DC-SERVER-01',
    description: 'Multiple failed login attempts from unusual location',
    status: 'resolved',
    affectedAssets: ['DC-SERVER-01'],
    iocs: ['ip:203.0.113.42', 'user:admin'],
    mitre: ['T1110 - Brute Force']
  },
  {
    id: 'EVT-003',
    timestamp: '2026-02-05T09:45:20Z',
    severity: 'medium',
    type: 'Unusual Network Traffic',
    source: 'FW-EDGE-01',
    description: 'Large data exfiltration attempt detected',
    status: 'monitoring',
    affectedAssets: ['FW-EDGE-01', 'WKS-089'],
    iocs: ['ip:192.0.2.123', 'domain:suspicious-site.com'],
    mitre: ['T1048 - Exfiltration Over Alternative Protocol']
  },
  {
    id: 'EVT-004',
    timestamp: '2026-02-05T09:20:10Z',
    severity: 'low',
    type: 'Policy Violation',
    source: 'WKS-101',
    description: 'Unauthorized software installation attempt',
    status: 'resolved',
    affectedAssets: ['WKS-101'],
    iocs: [],
    mitre: []
  },
  {
    id: 'EVT-005',
    timestamp: '2026-02-05T08:55:33Z',
    severity: 'critical',
    type: 'Command & Control',
    source: 'WKS-067',
    description: 'C2 beacon communication detected',
    status: 'investigating',
    affectedAssets: ['WKS-067'],
    iocs: ['ip:198.51.100.77', 'domain:c2-server.malicious'],
    mitre: ['T1071 - Application Layer Protocol']
  }
]

// Incidents
export const incidents = [
  {
    id: 'INC-2026-001',
    title: 'Ransomware Outbreak - Finance Department',
    severity: 'critical',
    status: 'in_progress',
    createdAt: '2026-02-05T10:30:00Z',
    updatedAt: '2026-02-05T11:45:00Z',
    assignee: 'John Smith',
    description: 'Multiple endpoints in finance department affected by ransomware',
    affectedSystems: 12,
    relatedEvents: ['EVT-001', 'EVT-005'],
    timeline: [
      { time: '10:30', action: 'Incident created', user: 'System' },
      { time: '10:35', action: 'Assigned to John Smith', user: 'Manager' },
      { time: '10:40', action: 'Isolated affected systems', user: 'John Smith' },
      { time: '11:15', action: 'Initiated forensic analysis', user: 'John Smith' }
    ]
  },
  {
    id: 'INC-2026-002',
    title: 'Brute Force Attack - Domain Controller',
    severity: 'high',
    status: 'resolved',
    createdAt: '2026-02-05T10:15:00Z',
    updatedAt: '2026-02-05T10:50:00Z',
    assignee: 'Sarah Johnson',
    description: 'Multiple failed login attempts detected on domain controller',
    affectedSystems: 1,
    relatedEvents: ['EVT-002'],
    timeline: [
      { time: '10:15', action: 'Incident created', user: 'System' },
      { time: '10:17', action: 'Blocked source IP', user: 'Sarah Johnson' },
      { time: '10:30', action: 'Verified no compromise', user: 'Sarah Johnson' },
      { time: '10:50', action: 'Incident closed', user: 'Sarah Johnson' }
    ]
  },
  {
    id: 'INC-2026-003',
    title: 'Data Exfiltration Attempt',
    severity: 'medium',
    status: 'monitoring',
    createdAt: '2026-02-05T09:45:00Z',
    updatedAt: '2026-02-05T09:50:00Z',
    assignee: 'Mike Chen',
    description: 'Unusual outbound traffic pattern detected',
    affectedSystems: 1,
    relatedEvents: ['EVT-003'],
    timeline: [
      { time: '09:45', action: 'Incident created', user: 'System' },
      { time: '09:47', action: 'Monitoring traffic patterns', user: 'Mike Chen' }
    ]
  }
]

// Assets
export const assets = [
  {
    id: 'WKS-042',
    name: 'Finance-WKS-042',
    type: 'Workstation',
    os: 'Windows 11 Pro',
    ip: '10.0.10.42',
    status: 'compromised',
    lastSeen: '2026-02-05T10:30:00Z',
    owner: 'Jane Doe',
    department: 'Finance',
    riskScore: 95
  },
  {
    id: 'DC-SERVER-01',
    name: 'Primary Domain Controller',
    type: 'Server',
    os: 'Windows Server 2022',
    ip: '10.0.1.10',
    status: 'healthy',
    lastSeen: '2026-02-05T11:00:00Z',
    owner: 'IT Department',
    department: 'IT',
    riskScore: 15
  },
  {
    id: 'WKS-067',
    name: 'HR-WKS-067',
    type: 'Workstation',
    os: 'Windows 10 Pro',
    ip: '10.0.20.67',
    status: 'investigating',
    lastSeen: '2026-02-05T08:55:00Z',
    owner: 'Bob Wilson',
    department: 'HR',
    riskScore: 78
  },
  {
    id: 'FW-EDGE-01',
    name: 'Edge Firewall',
    type: 'Network Device',
    os: 'Fortinet FortiOS',
    ip: '203.0.113.1',
    status: 'healthy',
    lastSeen: '2026-02-05T11:00:00Z',
    owner: 'Network Team',
    department: 'IT',
    riskScore: 10
  },
  {
    id: 'WKS-089',
    name: 'Dev-WKS-089',
    type: 'Workstation',
    os: 'Ubuntu 22.04',
    ip: '10.0.30.89',
    status: 'monitoring',
    lastSeen: '2026-02-05T09:45:00Z',
    owner: 'Alice Smith',
    department: 'Development',
    riskScore: 45
  },
  {
    id: 'WKS-101',
    name: 'Marketing-WKS-101',
    type: 'Workstation',
    os: 'macOS Sonoma',
    ip: '10.0.40.101',
    status: 'healthy',
    lastSeen: '2026-02-05T09:20:00Z',
    owner: 'Chris Lee',
    department: 'Marketing',
    riskScore: 20
  }
]

// Alert Rules
export const alertRules = [
  {
    id: 'RULE-001',
    name: 'Ransomware Detection',
    severity: 'critical',
    enabled: true,
    conditions: 'File encryption activity + Ransom note creation',
    actions: ['isolate_endpoint', 'notify_soc', 'create_incident']
  },
  {
    id: 'RULE-002',
    name: 'Brute Force Detection',
    severity: 'high',
    enabled: true,
    conditions: '>5 failed logins within 5 minutes',
    actions: ['block_ip', 'notify_admin']
  },
  {
    id: 'RULE-003',
    name: 'Data Exfiltration',
    severity: 'high',
    enabled: true,
    conditions: 'Outbound traffic >100MB to unknown destination',
    actions: ['monitor', 'create_event']
  },
  {
    id: 'RULE-004',
    name: 'Malware Signature Match',
    severity: 'critical',
    enabled: true,
    conditions: 'Known malware hash detected',
    actions: ['quarantine_file', 'isolate_endpoint', 'create_incident']
  }
]

// Dashboard Statistics
export const dashboardStats = {
  totalEvents: 1247,
  criticalEvents: 23,
  activeIncidents: 5,
  resolvedToday: 18,
  assetsMonitored: 342,
  compromisedAssets: 3,
  averageResponseTime: '12 mins',
  threatLevel: 'high'
}

// Event Timeline (for charts)
export const eventTimeline = [
  { hour: '00:00', critical: 1, high: 3, medium: 8, low: 15 },
  { hour: '01:00', critical: 0, high: 2, medium: 5, low: 12 },
  { hour: '02:00', critical: 0, high: 1, medium: 4, low: 10 },
  { hour: '03:00', critical: 0, high: 1, medium: 3, low: 8 },
  { hour: '04:00', critical: 1, high: 2, medium: 5, low: 11 },
  { hour: '05:00', critical: 0, high: 3, medium: 7, low: 14 },
  { hour: '06:00', critical: 2, high: 5, medium: 12, low: 20 },
  { hour: '07:00', critical: 1, high: 4, medium: 10, low: 18 },
  { hour: '08:00', critical: 3, high: 8, medium: 15, low: 25 },
  { hour: '09:00', critical: 2, high: 6, medium: 14, low: 22 },
  { hour: '10:00', critical: 4, high: 9, medium: 18, low: 28 },
  { hour: '11:00', critical: 2, high: 7, medium: 16, low: 24 }
]

// Threat Types Distribution
export const threatTypes = [
  { name: 'Malware', count: 145, percentage: 35 },
  { name: 'Phishing', count: 102, percentage: 25 },
  { name: 'Brute Force', count: 83, percentage: 20 },
  { name: 'Data Exfiltration', count: 62, percentage: 15 },
  { name: 'Other', count: 21, percentage: 5 }
]
