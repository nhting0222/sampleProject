import pytest


class TestIncidents:
    """Test incidents endpoints"""

    def test_get_incidents(self, client, auth_headers):
        """Test get all incidents"""
        response = client.get("/api/incidents", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_incidents_filter_by_status(self, client, auth_headers):
        """Test filtering incidents by status"""
        response = client.get("/api/incidents?status=in_progress", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        for incident in data:
            assert incident["status"] == "in_progress"

    def test_get_incident_by_id(self, client, auth_headers):
        """Test get single incident by ID"""
        response = client.get("/api/incidents/INC-2026-001", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "INC-2026-001"
        assert "timeline" in data

    def test_get_incident_not_found(self, client, auth_headers):
        """Test get nonexistent incident"""
        response = client.get("/api/incidents/INC-999", headers=auth_headers)
        assert response.status_code == 404

    def test_create_incident(self, client, analyst_headers):
        """Test creating new incident"""
        incident_data = {
            "title": "Test Incident",
            "severity": "high",
            "assignee": "Test User",
            "description": "Test incident description",
            "affectedSystems": 2,
            "relatedEvents": ["EVT-001"]
        }
        response = client.post("/api/incidents", json=incident_data, headers=analyst_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Incident"
        assert data["status"] == "in_progress"
        assert len(data["timeline"]) > 0

    def test_update_incident_status(self, client, analyst_headers):
        """Test updating incident status"""
        response = client.put(
            "/api/incidents/INC-2026-001",
            json={"status": "resolved"},
            headers=analyst_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "resolved"
        # Check timeline was updated
        assert any("resolved" in entry["action"].lower() for entry in data["timeline"])

    def test_update_incident_assignee(self, client, analyst_headers):
        """Test updating incident assignee"""
        response = client.put(
            "/api/incidents/INC-2026-001",
            json={"assignee": "New Assignee"},
            headers=analyst_headers
        )
        assert response.status_code == 200
        assert response.json()["assignee"] == "New Assignee"
