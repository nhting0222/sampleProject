from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class SeverityLevel(str, enum.Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


class EventStatus(str, enum.Enum):
    investigating = "investigating"
    monitoring = "monitoring"
    resolved = "resolved"


class IncidentStatus(str, enum.Enum):
    in_progress = "in_progress"
    monitoring = "monitoring"
    resolved = "resolved"


class AssetStatus(str, enum.Enum):
    healthy = "healthy"
    compromised = "compromised"
    investigating = "investigating"


class UserRole(str, enum.Enum):
    admin = "admin"
    analyst = "analyst"
    viewer = "viewer"


# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="viewer")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Security Event Model
class SecurityEvent(Base):
    __tablename__ = "security_events"

    id = Column(String, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    severity = Column(String, nullable=False)
    type = Column(String, nullable=False)
    source = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="investigating")
    affected_assets = Column(JSON, default=list)
    iocs = Column(JSON, default=list)
    mitre = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Incident Model
class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    status = Column(String, default="in_progress")
    assignee = Column(String)
    description = Column(Text)
    affected_systems = Column(Integer, default=0)
    related_events = Column(JSON, default=list)
    timeline = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Asset Model
class Asset(Base):
    __tablename__ = "assets"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    os = Column(String)
    ip = Column(String)
    status = Column(String, default="healthy")
    last_seen = Column(DateTime, default=datetime.utcnow)
    owner = Column(String)
    department = Column(String)
    risk_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Alert Rule Model
class AlertRule(Base):
    __tablename__ = "alert_rules"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    enabled = Column(Boolean, default=True)
    conditions = Column(Text)
    actions = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Audit Log Model
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    username = Column(String, nullable=False)
    action = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    resource_id = Column(String)
    details = Column(JSON)
    ip_address = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
