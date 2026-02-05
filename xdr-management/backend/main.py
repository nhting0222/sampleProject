from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime
import asyncio
import json
import random

from app.models import (
    SecurityEvent, SecurityEventCreate, SecurityEventUpdate,
    Incident, IncidentCreate, IncidentUpdate,
    Asset, AlertRule, AlertRuleUpdate, DashboardStats
)
from app.data.mock_data import (
    security_events, incidents, assets, alert_rules, dashboard_stats
)

app = FastAPI(
    title="XDR Management API",
    description="API for XDR Security Operations Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
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
        print(f"Client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Client disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error sending to client: {e}")
                disconnected.append(connection)

        # Remove disconnected clients
        for conn in disconnected:
            if conn in self.active_connections:
                self.active_connections.remove(conn)

manager = ConnectionManager()

# Generate random events periodically
async def generate_random_events():
    """Background task to generate random security events"""
    event_types = ["Malware Detection", "Suspicious Login", "Port Scan", "Data Exfiltration", "Brute Force Attack"]
    sources = ["WORKSTATION-101", "WORKSTATION-102", "SERVER-WEB-01", "SERVER-DB-01", "LAPTOP-HR-05"]
    severities = ["critical", "high", "medium", "low"]

    while True:
        await asyncio.sleep(random.randint(10, 30))  # Generate event every 10-30 seconds

        event_type = random.choice(event_types)
        source = random.choice(sources)
        severity = random.choice(severities)

        new_event = {
            "id": f"EVT-{str(len(security_events) + 1).zfill(3)}",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "severity": severity,
            "type": event_type,
            "source": source,
            "description": f"Real-time {event_type} detected on {source}",
            "status": "investigating",
            "affectedAssets": [source],
            "iocs": [],
            "mitre": []
        }

        security_events.append(new_event)

        # Broadcast to all connected clients
        await manager.broadcast({
            "type": "new_event",
            "data": new_event
        })

        print(f"Generated new event: {new_event['id']} - {event_type}")

# ========== Security Events Endpoints ==========

@app.get("/api/events", response_model=List[SecurityEvent])
async def get_events(
    severity: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None
):
    """Get all security events with optional filters"""
    result = security_events.copy()

    if severity:
        result = [e for e in result if e["severity"] == severity]

    if status:
        result = [e for e in result if e["status"] == status]

    if search:
        search_lower = search.lower()
        result = [
            e for e in result
            if search_lower in e["type"].lower() or
               search_lower in e["source"].lower() or
               search_lower in e["description"].lower()
        ]

    return result

@app.get("/api/events/{event_id}", response_model=SecurityEvent)
async def get_event(event_id: str):
    """Get a specific security event"""
    event = next((e for e in security_events if e["id"] == event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.post("/api/events", response_model=SecurityEvent)
async def create_event(event: SecurityEventCreate):
    """Create a new security event"""
    new_id = f"EVT-{str(len(security_events) + 1).zfill(3)}"
    new_event = {
        "id": new_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "severity": event.severity,
        "type": event.type,
        "source": event.source,
        "description": event.description,
        "status": "investigating",
        "affectedAssets": event.affectedAssets,
        "iocs": event.iocs,
        "mitre": event.mitre
    }
    security_events.append(new_event)

    # Broadcast new event to all connected clients
    await manager.broadcast({
        "type": "new_event",
        "data": new_event
    })

    return new_event

@app.put("/api/events/{event_id}", response_model=SecurityEvent)
async def update_event(event_id: str, update: SecurityEventUpdate):
    """Update a security event"""
    event = next((e for e in security_events if e["id"] == event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if update.status is not None:
        event["status"] = update.status
    if update.description is not None:
        event["description"] = update.description

    return event

@app.delete("/api/events/{event_id}")
async def delete_event(event_id: str):
    """Delete a security event"""
    global security_events
    security_events = [e for e in security_events if e["id"] != event_id]
    return {"message": "Event deleted successfully"}

# ========== Incidents Endpoints ==========

@app.get("/api/incidents", response_model=List[Incident])
async def get_incidents(status: Optional[str] = None):
    """Get all incidents"""
    if status:
        return [i for i in incidents if i["status"] == status]
    return incidents

@app.get("/api/incidents/{incident_id}", response_model=Incident)
async def get_incident(incident_id: str):
    """Get a specific incident"""
    incident = next((i for i in incidents if i["id"] == incident_id), None)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@app.post("/api/incidents", response_model=Incident)
async def create_incident(incident: IncidentCreate):
    """Create a new incident"""
    new_id = f"INC-2026-{str(len(incidents) + 1).zfill(3)}"
    now = datetime.utcnow().isoformat() + "Z"

    new_incident = {
        "id": new_id,
        "title": incident.title,
        "severity": incident.severity,
        "status": "in_progress",
        "createdAt": now,
        "updatedAt": now,
        "assignee": incident.assignee,
        "description": incident.description,
        "affectedSystems": incident.affectedSystems,
        "relatedEvents": incident.relatedEvents,
        "timeline": [
            {
                "time": datetime.utcnow().strftime("%H:%M"),
                "action": "Incident created",
                "user": "System"
            }
        ]
    }
    incidents.append(new_incident)

    # Broadcast new incident to all connected clients
    await manager.broadcast({
        "type": "new_incident",
        "data": new_incident
    })

    return new_incident

@app.put("/api/incidents/{incident_id}", response_model=Incident)
async def update_incident(incident_id: str, update: IncidentUpdate):
    """Update an incident"""
    incident = next((i for i in incidents if i["id"] == incident_id), None)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    if update.status is not None:
        incident["status"] = update.status
        incident["timeline"].append({
            "time": datetime.utcnow().strftime("%H:%M"),
            "action": f"Status changed to {update.status}",
            "user": "API"
        })
    if update.assignee is not None:
        incident["assignee"] = update.assignee

    incident["updatedAt"] = datetime.utcnow().isoformat() + "Z"
    return incident

# ========== Assets Endpoints ==========

@app.get("/api/assets", response_model=List[Asset])
async def get_assets(status: Optional[str] = None):
    """Get all assets"""
    if status:
        return [a for a in assets if a["status"] == status]
    return assets

@app.get("/api/assets/{asset_id}", response_model=Asset)
async def get_asset(asset_id: str):
    """Get a specific asset"""
    asset = next((a for a in assets if a["id"] == asset_id), None)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

# ========== Alert Rules Endpoints ==========

@app.get("/api/alerts", response_model=List[AlertRule])
async def get_alert_rules():
    """Get all alert rules"""
    return alert_rules

@app.put("/api/alerts/{rule_id}", response_model=AlertRule)
async def update_alert_rule(rule_id: str, update: AlertRuleUpdate):
    """Update an alert rule"""
    rule = next((r for r in alert_rules if r["id"] == rule_id), None)
    if not rule:
        raise HTTPException(status_code=404, detail="Alert rule not found")

    if update.enabled is not None:
        rule["enabled"] = update.enabled

    return rule

# ========== Dashboard Endpoints ==========

@app.get("/api/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    """Get dashboard statistics"""
    # Update stats dynamically
    stats = dashboard_stats.copy()
    stats["totalEvents"] = len(security_events)
    stats["criticalEvents"] = len([e for e in security_events if e["severity"] == "critical"])
    stats["activeIncidents"] = len([i for i in incidents if i["status"] == "in_progress"])
    stats["assetsMonitored"] = len(assets)
    stats["compromisedAssets"] = len([a for a in assets if a["status"] == "compromised"])
    return stats

# ========== WebSocket Endpoint ==========

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time event notifications"""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and receive any messages from client
            data = await websocket.receive_text()
            # Echo back or handle client messages if needed
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
        "message": "XDR Management API",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Start background task for generating events
@app.on_event("startup")
async def startup_event():
    """Start background tasks on application startup"""
    asyncio.create_task(generate_random_events())
    print("Background event generator started")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
