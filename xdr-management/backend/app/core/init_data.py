from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
import random

from app.db_models import User, SecurityEvent, Incident, Asset, AlertRule

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def init_users(db: Session):
    """Initialize default users"""
    users = [
        {
            "id": "USR-001",
            "username": "admin",
            "email": "admin@xdr.local",
            "full_name": "System Administrator",
            "hashed_password": pwd_context.hash("admin123"),
            "role": "admin",
            "is_active": True
        },
        {
            "id": "USR-002",
            "username": "analyst",
            "email": "analyst@xdr.local",
            "full_name": "Security Analyst",
            "hashed_password": pwd_context.hash("analyst123"),
            "role": "analyst",
            "is_active": True
        },
        {
            "id": "USR-003",
            "username": "viewer",
            "email": "viewer@xdr.local",
            "full_name": "Security Viewer",
            "hashed_password": pwd_context.hash("viewer123"),
            "role": "viewer",
            "is_active": True
        }
    ]

    for user_data in users:
        existing = db.query(User).filter(User.username == user_data["username"]).first()
        if not existing:
            db.add(User(**user_data))

    db.commit()


def init_events(db: Session):
    """Initialize sample security events"""
    events = [
        {
            "id": "EVT-001",
            "severity": "critical",
            "type": "Malware Detection",
            "source": "WORKSTATION-101",
            "description": "Ransomware variant detected on workstation. Immediate containment required.",
            "status": "investigating",
            "affected_assets": ["WORKSTATION-101", "SERVER-FILE-01"],
            "iocs": ["malware.exe", "192.168.1.100", "evil-domain.com"],
            "mitre": ["T1486", "T1566"]
        },
        {
            "id": "EVT-002",
            "severity": "high",
            "type": "Suspicious Login",
            "source": "SERVER-AD-01",
            "description": "Multiple failed login attempts followed by successful authentication from unusual location.",
            "status": "monitoring",
            "affected_assets": ["SERVER-AD-01"],
            "iocs": ["185.220.101.45"],
            "mitre": ["T1110", "T1078"]
        },
        {
            "id": "EVT-003",
            "severity": "medium",
            "type": "Port Scan",
            "source": "FIREWALL-01",
            "description": "External port scanning activity detected targeting multiple internal hosts.",
            "status": "resolved",
            "affected_assets": ["FIREWALL-01"],
            "iocs": ["45.33.32.156"],
            "mitre": ["T1046"]
        },
        {
            "id": "EVT-004",
            "severity": "critical",
            "type": "Data Exfiltration",
            "source": "SERVER-DB-01",
            "description": "Large data transfer detected to unknown external IP address.",
            "status": "investigating",
            "affected_assets": ["SERVER-DB-01"],
            "iocs": ["192.168.1.50", "suspicious-upload.net"],
            "mitre": ["T1041", "T1567"]
        },
        {
            "id": "EVT-005",
            "severity": "high",
            "type": "Privilege Escalation",
            "source": "SERVER-WEB-01",
            "description": "Unexpected privilege escalation detected on web server.",
            "status": "investigating",
            "affected_assets": ["SERVER-WEB-01"],
            "iocs": ["exploit.sh"],
            "mitre": ["T1068", "T1548"]
        }
    ]

    for i, event_data in enumerate(events):
        existing = db.query(SecurityEvent).filter(SecurityEvent.id == event_data["id"]).first()
        if not existing:
            event_data["timestamp"] = datetime.utcnow() - timedelta(hours=i*2)
            db.add(SecurityEvent(**event_data))

    db.commit()


def init_incidents(db: Session):
    """Initialize sample incidents"""
    incidents = [
        {
            "id": "INC-2026-001",
            "title": "Ransomware Attack - Critical Systems",
            "severity": "critical",
            "status": "in_progress",
            "assignee": "John Smith",
            "description": "Active ransomware incident affecting multiple critical systems.",
            "affected_systems": 5,
            "related_events": ["EVT-001"],
            "timeline": [
                {"time": "09:15", "action": "Initial detection", "user": "System"},
                {"time": "09:20", "action": "Incident created", "user": "SOC Analyst"},
                {"time": "09:30", "action": "Containment initiated", "user": "John Smith"}
            ]
        },
        {
            "id": "INC-2026-002",
            "title": "Unauthorized Access Attempt",
            "severity": "high",
            "status": "monitoring",
            "assignee": "Jane Doe",
            "description": "Suspicious authentication activity detected from foreign IP.",
            "affected_systems": 2,
            "related_events": ["EVT-002"],
            "timeline": [
                {"time": "14:00", "action": "Alert triggered", "user": "System"},
                {"time": "14:15", "action": "Investigation started", "user": "Jane Doe"}
            ]
        },
        {
            "id": "INC-2026-003",
            "title": "Data Breach Investigation",
            "severity": "critical",
            "status": "in_progress",
            "assignee": "Mike Johnson",
            "description": "Potential data exfiltration from database server.",
            "affected_systems": 3,
            "related_events": ["EVT-004"],
            "timeline": [
                {"time": "11:00", "action": "Anomaly detected", "user": "System"},
                {"time": "11:30", "action": "Forensic analysis initiated", "user": "Mike Johnson"}
            ]
        }
    ]

    for incident_data in incidents:
        existing = db.query(Incident).filter(Incident.id == incident_data["id"]).first()
        if not existing:
            db.add(Incident(**incident_data))

    db.commit()


def init_assets(db: Session):
    """Initialize sample assets"""
    assets = [
        {
            "id": "AST-001",
            "name": "WORKSTATION-101",
            "type": "Workstation",
            "os": "Windows 11",
            "ip": "192.168.1.101",
            "status": "compromised",
            "owner": "John Doe",
            "department": "Engineering",
            "risk_score": 95
        },
        {
            "id": "AST-002",
            "name": "SERVER-WEB-01",
            "type": "Server",
            "os": "Ubuntu 22.04",
            "ip": "192.168.1.10",
            "status": "investigating",
            "owner": "IT Team",
            "department": "IT",
            "risk_score": 75
        },
        {
            "id": "AST-003",
            "name": "SERVER-DB-01",
            "type": "Server",
            "os": "CentOS 8",
            "ip": "192.168.1.20",
            "status": "compromised",
            "owner": "DBA Team",
            "department": "IT",
            "risk_score": 90
        },
        {
            "id": "AST-004",
            "name": "SERVER-AD-01",
            "type": "Server",
            "os": "Windows Server 2022",
            "ip": "192.168.1.5",
            "status": "healthy",
            "owner": "IT Team",
            "department": "IT",
            "risk_score": 30
        },
        {
            "id": "AST-005",
            "name": "FIREWALL-01",
            "type": "Network",
            "os": "FortiOS",
            "ip": "192.168.1.1",
            "status": "healthy",
            "owner": "Network Team",
            "department": "IT",
            "risk_score": 15
        },
        {
            "id": "AST-006",
            "name": "LAPTOP-HR-05",
            "type": "Laptop",
            "os": "Windows 11",
            "ip": "192.168.1.150",
            "status": "healthy",
            "owner": "HR Manager",
            "department": "HR",
            "risk_score": 25
        }
    ]

    for asset_data in assets:
        existing = db.query(Asset).filter(Asset.id == asset_data["id"]).first()
        if not existing:
            db.add(Asset(**asset_data))

    db.commit()


def init_alert_rules(db: Session):
    """Initialize sample alert rules"""
    rules = [
        {
            "id": "RULE-001",
            "name": "Critical Malware Detection",
            "severity": "critical",
            "enabled": True,
            "conditions": "malware_detected AND severity=critical",
            "actions": ["notify_soc", "isolate_host", "create_incident"]
        },
        {
            "id": "RULE-002",
            "name": "Brute Force Attack",
            "severity": "high",
            "enabled": True,
            "conditions": "failed_logins > 5 AND time_window < 5min",
            "actions": ["notify_soc", "block_ip"]
        },
        {
            "id": "RULE-003",
            "name": "Data Exfiltration Alert",
            "severity": "critical",
            "enabled": True,
            "conditions": "data_transfer > 1GB AND destination=external",
            "actions": ["notify_soc", "block_transfer", "create_incident"]
        },
        {
            "id": "RULE-004",
            "name": "Suspicious Port Scan",
            "severity": "medium",
            "enabled": True,
            "conditions": "port_scan_detected AND source=external",
            "actions": ["log_event", "notify_soc"]
        },
        {
            "id": "RULE-005",
            "name": "Privilege Escalation",
            "severity": "high",
            "enabled": False,
            "conditions": "privilege_change AND user!=admin",
            "actions": ["notify_soc", "create_alert"]
        }
    ]

    for rule_data in rules:
        existing = db.query(AlertRule).filter(AlertRule.id == rule_data["id"]).first()
        if not existing:
            db.add(AlertRule(**rule_data))

    db.commit()


def seed_database(db: Session):
    """Seed database with initial data"""
    print("Seeding database...")
    init_users(db)
    init_events(db)
    init_incidents(db)
    init_assets(db)
    init_alert_rules(db)
    print("Database seeded successfully!")
