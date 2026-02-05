from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class SeverityLevel(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"

class EventStatus(str, Enum):
    investigating = "investigating"
    monitoring = "monitoring"
    resolved = "resolved"

class IncidentStatus(str, Enum):
    in_progress = "in_progress"
    monitoring = "monitoring"
    resolved = "resolved"

class AssetStatus(str, Enum):
    healthy = "healthy"
    compromised = "compromised"
    investigating = "investigating"

class SecurityEvent(BaseModel):
    id: str
    timestamp: str
    severity: SeverityLevel
    type: str
    source: str
    description: str
    status: EventStatus
    affectedAssets: List[str]
    iocs: List[str]
    mitre: List[str]

class SecurityEventCreate(BaseModel):
    type: str
    source: str
    description: str
    severity: SeverityLevel
    affectedAssets: List[str] = []
    iocs: List[str] = []
    mitre: List[str] = []

class SecurityEventUpdate(BaseModel):
    status: Optional[EventStatus] = None
    description: Optional[str] = None

class TimelineEntry(BaseModel):
    time: str
    action: str
    user: str

class Incident(BaseModel):
    id: str
    title: str
    severity: SeverityLevel
    status: IncidentStatus
    createdAt: str
    updatedAt: str
    assignee: str
    description: str
    affectedSystems: int
    relatedEvents: List[str]
    timeline: List[TimelineEntry]

class IncidentCreate(BaseModel):
    title: str
    severity: SeverityLevel
    assignee: str
    description: str
    affectedSystems: int
    relatedEvents: List[str] = []

class IncidentUpdate(BaseModel):
    status: Optional[IncidentStatus] = None
    assignee: Optional[str] = None

class Asset(BaseModel):
    id: str
    name: str
    type: str
    os: str
    ip: str
    status: AssetStatus
    lastSeen: str
    owner: str
    department: str
    riskScore: int

class AlertRule(BaseModel):
    id: str
    name: str
    severity: SeverityLevel
    enabled: bool
    conditions: str
    actions: List[str]

class AlertRuleUpdate(BaseModel):
    enabled: Optional[bool] = None

class DashboardStats(BaseModel):
    totalEvents: int
    criticalEvents: int
    activeIncidents: int
    resolvedToday: int
    assetsMonitored: int
    compromisedAssets: int
    averageResponseTime: str
    threatLevel: str
