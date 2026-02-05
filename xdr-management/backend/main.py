from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import asyncio
import random

from app.models import (
    SecurityEvent as SecurityEventSchema,
    SecurityEventCreate, SecurityEventUpdate,
    Incident as IncidentSchema,
    IncidentCreate, IncidentUpdate,
    Asset as AssetSchema,
    AlertRule as AlertRuleSchema,
    AlertRuleUpdate, DashboardStats
)
from app.db_models import SecurityEvent, Incident, Asset, AlertRule, AuditLog
from app.routes.auth import router as auth_router
from app.routes.monitoring import router as monitoring_router
from app.core.security import (
    get_current_active_user,
    require_admin,
    require_analyst,
    require_viewer
)
from app.core.config import settings
from app.core.database import get_db, init_db, SessionLocal
from app.core.init_data import seed_database
from app.core.logging import logger, metrics
from app.middleware.logging import RequestLoggingMiddleware

app = FastAPI(
    title=settings.APP_NAME,
    description="API for XDR Security Operations Platform",
    version=settings.APP_VERSION
)

# Include routers
app.include_router(auth_router)
app.include_router(monitoring_router)

# Add request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        metrics.record_websocket_connect()
        logger.info(f"WebSocket client connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        metrics.record_websocket_disconnect()
        logger.info(f"WebSocket client disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error sending to client: {e}")
                disconnected.append(connection)
        for conn in disconnected:
            if conn in self.active_connections:
                self.active_connections.remove(conn)


manager = ConnectionManager()


# Helper function to log audit
def log_audit(db: Session, user: dict, action: str, resource_type: str, resource_id: str = None, details: dict = None):
    audit = AuditLog(
        user_id=user["id"],
        username=user["username"],
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details
    )
    db.add(audit)
    db.commit()


# Generate random events periodically
async def generate_random_events():
    event_types = ["Malware Detection", "Suspicious Login", "Port Scan", "Data Exfiltration", "Brute Force Attack"]
    sources = ["WORKSTATION-101", "WORKSTATION-102", "SERVER-WEB-01", "SERVER-DB-01", "LAPTOP-HR-05"]
    severities = ["critical", "high", "medium", "low"]

    while True:
        await asyncio.sleep(random.randint(10, 30))

        db = SessionLocal()
        try:
            event_count = db.query(SecurityEvent).count()
            event_type = random.choice(event_types)
            source = random.choice(sources)
            severity = random.choice(severities)

            new_event = SecurityEvent(
                id=f"EVT-{str(event_count + 1).zfill(3)}",
                timestamp=datetime.utcnow(),
                severity=severity,
                type=event_type,
                source=source,
                description=f"Real-time {event_type} detected on {source}",
                status="investigating",
                affected_assets=[source],
                iocs=[],
                mitre=[]
            )

            db.add(new_event)
            db.commit()

            await manager.broadcast({
                "type": "new_event",
                "data": {
                    "id": new_event.id,
                    "timestamp": new_event.timestamp.isoformat() + "Z",
                    "severity": new_event.severity,
                    "type": new_event.type,
                    "source": new_event.source,
                    "description": new_event.description,
                    "status": new_event.status,
                    "affectedAssets": new_event.affected_assets,
                    "iocs": new_event.iocs,
                    "mitre": new_event.mitre
                }
            })

            print(f"Generated new event: {new_event.id} - {event_type}")
        finally:
            db.close()


# ========== Security Events Endpoints ==========

@app.get("/api/events", response_model=List[SecurityEventSchema])
async def get_events(
    severity: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_viewer)
):
    """Get all security events with optional filters"""
    query = db.query(SecurityEvent)

    if severity:
        query = query.filter(SecurityEvent.severity == severity)
    if status:
        query = query.filter(SecurityEvent.status == status)
    if search:
        search_lower = f"%{search.lower()}%"
        query = query.filter(
            (SecurityEvent.type.ilike(search_lower)) |
            (SecurityEvent.source.ilike(search_lower)) |
            (SecurityEvent.description.ilike(search_lower))
        )

    events = query.order_by(SecurityEvent.timestamp.desc()).all()

    return [
        SecurityEventSchema(
            id=e.id,
            timestamp=e.timestamp.isoformat() + "Z",
            severity=e.severity,
            type=e.type,
            source=e.source,
            description=e.description,
            status=e.status,
            affectedAssets=e.affected_assets or [],
            iocs=e.iocs or [],
            mitre=e.mitre or []
        ) for e in events
    ]


@app.get("/api/events/{event_id}", response_model=SecurityEventSchema)
async def get_event(
    event_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_viewer)
):
    """Get a specific security event"""
    event = db.query(SecurityEvent).filter(SecurityEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return SecurityEventSchema(
        id=event.id,
        timestamp=event.timestamp.isoformat() + "Z",
        severity=event.severity,
        type=event.type,
        source=event.source,
        description=event.description,
        status=event.status,
        affectedAssets=event.affected_assets or [],
        iocs=event.iocs or [],
        mitre=event.mitre or []
    )


@app.post("/api/events", response_model=SecurityEventSchema)
async def create_event(
    event: SecurityEventCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_analyst)
):
    """Create a new security event"""
    event_count = db.query(SecurityEvent).count()
    new_id = f"EVT-{str(event_count + 1).zfill(3)}"

    new_event = SecurityEvent(
        id=new_id,
        timestamp=datetime.utcnow(),
        severity=event.severity,
        type=event.type,
        source=event.source,
        description=event.description,
        status="investigating",
        affected_assets=event.affectedAssets,
        iocs=event.iocs,
        mitre=event.mitre
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    log_audit(db, current_user, "create", "event", new_id, {"type": event.type})

    event_data = {
        "id": new_event.id,
        "timestamp": new_event.timestamp.isoformat() + "Z",
        "severity": new_event.severity,
        "type": new_event.type,
        "source": new_event.source,
        "description": new_event.description,
        "status": new_event.status,
        "affectedAssets": new_event.affected_assets or [],
        "iocs": new_event.iocs or [],
        "mitre": new_event.mitre or []
    }

    await manager.broadcast({"type": "new_event", "data": event_data})

    return SecurityEventSchema(**event_data)


@app.put("/api/events/{event_id}", response_model=SecurityEventSchema)
async def update_event(
    event_id: str,
    update: SecurityEventUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_analyst)
):
    """Update a security event"""
    event = db.query(SecurityEvent).filter(SecurityEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if update.status is not None:
        event.status = update.status
    if update.description is not None:
        event.description = update.description

    event.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(event)

    log_audit(db, current_user, "update", "event", event_id)

    return SecurityEventSchema(
        id=event.id,
        timestamp=event.timestamp.isoformat() + "Z",
        severity=event.severity,
        type=event.type,
        source=event.source,
        description=event.description,
        status=event.status,
        affectedAssets=event.affected_assets or [],
        iocs=event.iocs or [],
        mitre=event.mitre or []
    )


@app.delete("/api/events/{event_id}")
async def delete_event(
    event_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """Delete a security event"""
    event = db.query(SecurityEvent).filter(SecurityEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(event)
    db.commit()

    log_audit(db, current_user, "delete", "event", event_id)

    return {"message": "Event deleted successfully"}


# ========== Incidents Endpoints ==========

@app.get("/api/incidents", response_model=List[IncidentSchema])
async def get_incidents(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_viewer)
):
    """Get all incidents"""
    query = db.query(Incident)
    if status:
        query = query.filter(Incident.status == status)

    incidents = query.order_by(Incident.created_at.desc()).all()

    return [
        IncidentSchema(
            id=i.id,
            title=i.title,
            severity=i.severity,
            status=i.status,
            createdAt=i.created_at.isoformat() + "Z",
            updatedAt=i.updated_at.isoformat() + "Z",
            assignee=i.assignee or "",
            description=i.description or "",
            affectedSystems=i.affected_systems or 0,
            relatedEvents=i.related_events or [],
            timeline=i.timeline or []
        ) for i in incidents
    ]


@app.get("/api/incidents/{incident_id}", response_model=IncidentSchema)
async def get_incident(
    incident_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_viewer)
):
    """Get a specific incident"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    return IncidentSchema(
        id=incident.id,
        title=incident.title,
        severity=incident.severity,
        status=incident.status,
        createdAt=incident.created_at.isoformat() + "Z",
        updatedAt=incident.updated_at.isoformat() + "Z",
        assignee=incident.assignee or "",
        description=incident.description or "",
        affectedSystems=incident.affected_systems or 0,
        relatedEvents=incident.related_events or [],
        timeline=incident.timeline or []
    )


@app.post("/api/incidents", response_model=IncidentSchema)
async def create_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_analyst)
):
    """Create a new incident"""
    incident_count = db.query(Incident).count()
    new_id = f"INC-2026-{str(incident_count + 1).zfill(3)}"
    now = datetime.utcnow()

    new_incident = Incident(
        id=new_id,
        title=incident.title,
        severity=incident.severity,
        status="in_progress",
        assignee=incident.assignee,
        description=incident.description,
        affected_systems=incident.affectedSystems,
        related_events=incident.relatedEvents,
        timeline=[{
            "time": now.strftime("%H:%M"),
            "action": "Incident created",
            "user": current_user["username"]
        }],
        created_at=now,
        updated_at=now
    )

    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)

    log_audit(db, current_user, "create", "incident", new_id)

    await manager.broadcast({
        "type": "new_incident",
        "data": {
            "id": new_incident.id,
            "title": new_incident.title,
            "severity": new_incident.severity
        }
    })

    return IncidentSchema(
        id=new_incident.id,
        title=new_incident.title,
        severity=new_incident.severity,
        status=new_incident.status,
        createdAt=new_incident.created_at.isoformat() + "Z",
        updatedAt=new_incident.updated_at.isoformat() + "Z",
        assignee=new_incident.assignee or "",
        description=new_incident.description or "",
        affectedSystems=new_incident.affected_systems or 0,
        relatedEvents=new_incident.related_events or [],
        timeline=new_incident.timeline or []
    )


@app.put("/api/incidents/{incident_id}", response_model=IncidentSchema)
async def update_incident(
    incident_id: str,
    update: IncidentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_analyst)
):
    """Update an incident"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    now = datetime.utcnow()
    timeline = incident.timeline or []

    if update.status is not None:
        incident.status = update.status
        timeline.append({
            "time": now.strftime("%H:%M"),
            "action": f"Status changed to {update.status}",
            "user": current_user["username"]
        })

    if update.assignee is not None:
        incident.assignee = update.assignee
        timeline.append({
            "time": now.strftime("%H:%M"),
            "action": f"Assigned to {update.assignee}",
            "user": current_user["username"]
        })

    incident.timeline = timeline
    incident.updated_at = now
    db.commit()
    db.refresh(incident)

    log_audit(db, current_user, "update", "incident", incident_id)

    return IncidentSchema(
        id=incident.id,
        title=incident.title,
        severity=incident.severity,
        status=incident.status,
        createdAt=incident.created_at.isoformat() + "Z",
        updatedAt=incident.updated_at.isoformat() + "Z",
        assignee=incident.assignee or "",
        description=incident.description or "",
        affectedSystems=incident.affected_systems or 0,
        relatedEvents=incident.related_events or [],
        timeline=incident.timeline or []
    )


# ========== Assets Endpoints ==========

@app.get("/api/assets", response_model=List[AssetSchema])
async def get_assets(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_viewer)
):
    """Get all assets"""
    query = db.query(Asset)
    if status:
        query = query.filter(Asset.status == status)

    assets = query.all()

    return [
        AssetSchema(
            id=a.id,
            name=a.name,
            type=a.type,
            os=a.os or "",
            ip=a.ip or "",
            status=a.status,
            lastSeen=a.last_seen.isoformat() + "Z" if a.last_seen else "",
            owner=a.owner or "",
            department=a.department or "",
            riskScore=a.risk_score or 0
        ) for a in assets
    ]


@app.get("/api/assets/{asset_id}", response_model=AssetSchema)
async def get_asset(
    asset_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_viewer)
):
    """Get a specific asset"""
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    return AssetSchema(
        id=asset.id,
        name=asset.name,
        type=asset.type,
        os=asset.os or "",
        ip=asset.ip or "",
        status=asset.status,
        lastSeen=asset.last_seen.isoformat() + "Z" if asset.last_seen else "",
        owner=asset.owner or "",
        department=asset.department or "",
        riskScore=asset.risk_score or 0
    )


# ========== Alert Rules Endpoints ==========

@app.get("/api/alerts", response_model=List[AlertRuleSchema])
async def get_alert_rules(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_viewer)
):
    """Get all alert rules"""
    rules = db.query(AlertRule).all()

    return [
        AlertRuleSchema(
            id=r.id,
            name=r.name,
            severity=r.severity,
            enabled=r.enabled,
            conditions=r.conditions or "",
            actions=r.actions or []
        ) for r in rules
    ]


@app.put("/api/alerts/{rule_id}", response_model=AlertRuleSchema)
async def update_alert_rule(
    rule_id: str,
    update: AlertRuleUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """Update an alert rule"""
    rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Alert rule not found")

    if update.enabled is not None:
        rule.enabled = update.enabled

    rule.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(rule)

    log_audit(db, current_user, "update", "alert_rule", rule_id, {"enabled": update.enabled})

    return AlertRuleSchema(
        id=rule.id,
        name=rule.name,
        severity=rule.severity,
        enabled=rule.enabled,
        conditions=rule.conditions or "",
        actions=rule.actions or []
    )


# ========== Dashboard Endpoints ==========

@app.get("/api/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_viewer)
):
    """Get dashboard statistics"""
    total_events = db.query(SecurityEvent).count()
    critical_events = db.query(SecurityEvent).filter(SecurityEvent.severity == "critical").count()
    active_incidents = db.query(Incident).filter(Incident.status == "in_progress").count()
    resolved_today = db.query(SecurityEvent).filter(
        SecurityEvent.status == "resolved",
        SecurityEvent.updated_at >= datetime.utcnow().replace(hour=0, minute=0, second=0)
    ).count()
    assets_monitored = db.query(Asset).count()
    compromised_assets = db.query(Asset).filter(Asset.status == "compromised").count()

    # Determine threat level
    threat_level = "low"
    if critical_events > 3 or compromised_assets > 2:
        threat_level = "critical"
    elif critical_events > 1 or compromised_assets > 0:
        threat_level = "high"
    elif total_events > 10:
        threat_level = "medium"

    return DashboardStats(
        totalEvents=total_events,
        criticalEvents=critical_events,
        activeIncidents=active_incidents,
        resolvedToday=resolved_today,
        assetsMonitored=assets_monitored,
        compromisedAssets=compromised_assets,
        averageResponseTime="15 min",
        threatLevel=threat_level
    )


# ========== WebSocket Endpoint ==========

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time event notifications"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({"type": "pong", "message": "Connection alive"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)


# ========== Root Endpoint ==========

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


# ========== Startup Event ==========

@app.on_event("startup")
async def startup_event():
    """Initialize database and start background tasks"""
    print("Initializing database...")
    init_db()

    # Seed database with initial data
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

    # Start background event generator
    asyncio.create_task(generate_random_events())
    print("Background event generator started")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
