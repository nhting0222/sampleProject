import pytest


class TestSecurityEvents:
    """Test security events endpoints"""

    def test_get_events_authenticated(self, client, auth_headers):
        """Test get events with authentication"""
        response = client.get("/api/events", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_events_unauthenticated(self, client):
        """Test get events without authentication"""
        response = client.get("/api/events")
        assert response.status_code == 401

    def test_get_events_filter_by_severity(self, client, auth_headers):
        """Test filtering events by severity"""
        response = client.get("/api/events?severity=critical", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        for event in data:
            assert event["severity"] == "critical"

    def test_get_events_filter_by_status(self, client, auth_headers):
        """Test filtering events by status"""
        response = client.get("/api/events?status=investigating", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        for event in data:
            assert event["status"] == "investigating"

    def test_get_event_by_id(self, client, auth_headers):
        """Test get single event by ID"""
        response = client.get("/api/events/EVT-001", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "EVT-001"

    def test_get_event_not_found(self, client, auth_headers):
        """Test get nonexistent event"""
        response = client.get("/api/events/EVT-999", headers=auth_headers)
        assert response.status_code == 404

    def test_create_event_as_analyst(self, client, analyst_headers):
        """Test creating event as analyst"""
        event_data = {
            "type": "Test Event",
            "source": "TEST-SERVER",
            "description": "Test event description",
            "severity": "medium",
            "affectedAssets": ["TEST-SERVER"],
            "iocs": [],
            "mitre": []
        }
        response = client.post("/api/events", json=event_data, headers=analyst_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "Test Event"
        assert data["status"] == "investigating"

    def test_create_event_as_viewer_forbidden(self, client, viewer_headers):
        """Test that viewer cannot create events"""
        event_data = {
            "type": "Test Event",
            "source": "TEST-SERVER",
            "description": "Test event description",
            "severity": "medium",
            "affectedAssets": [],
            "iocs": [],
            "mitre": []
        }
        response = client.post("/api/events", json=event_data, headers=viewer_headers)
        assert response.status_code == 403

    def test_update_event_status(self, client, analyst_headers):
        """Test updating event status"""
        response = client.put(
            "/api/events/EVT-001",
            json={"status": "resolved"},
            headers=analyst_headers
        )
        assert response.status_code == 200
        assert response.json()["status"] == "resolved"

    def test_delete_event_as_admin(self, client, auth_headers):
        """Test deleting event as admin"""
        response = client.delete("/api/events/EVT-003", headers=auth_headers)
        assert response.status_code == 200

        # Verify event is deleted
        response = client.get("/api/events/EVT-003", headers=auth_headers)
        assert response.status_code == 404

    def test_delete_event_as_analyst_forbidden(self, client, analyst_headers):
        """Test that analyst cannot delete events"""
        response = client.delete("/api/events/EVT-001", headers=analyst_headers)
        assert response.status_code == 403
