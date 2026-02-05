import pytest


class TestDashboard:
    """Test dashboard endpoints"""

    def test_get_dashboard_stats(self, client, auth_headers):
        """Test get dashboard statistics"""
        response = client.get("/api/dashboard/stats", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()

        # Check all required fields are present
        assert "totalEvents" in data
        assert "criticalEvents" in data
        assert "activeIncidents" in data
        assert "resolvedToday" in data
        assert "assetsMonitored" in data
        assert "compromisedAssets" in data
        assert "averageResponseTime" in data
        assert "threatLevel" in data

        # Check types
        assert isinstance(data["totalEvents"], int)
        assert isinstance(data["criticalEvents"], int)
        assert data["threatLevel"] in ["low", "medium", "high", "critical"]

    def test_dashboard_stats_unauthenticated(self, client):
        """Test dashboard stats without authentication"""
        response = client.get("/api/dashboard/stats")
        assert response.status_code == 401


class TestAssets:
    """Test assets endpoints"""

    def test_get_assets(self, client, auth_headers):
        """Test get all assets"""
        response = client.get("/api/assets", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_assets_filter_by_status(self, client, auth_headers):
        """Test filtering assets by status"""
        response = client.get("/api/assets?status=compromised", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        for asset in data:
            assert asset["status"] == "compromised"

    def test_get_asset_by_id(self, client, auth_headers):
        """Test get single asset by ID"""
        response = client.get("/api/assets/AST-001", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "AST-001"
        assert "riskScore" in data


class TestAlertRules:
    """Test alert rules endpoints"""

    def test_get_alert_rules(self, client, auth_headers):
        """Test get all alert rules"""
        response = client.get("/api/alerts", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_update_alert_rule_as_admin(self, client, auth_headers):
        """Test updating alert rule as admin"""
        response = client.put(
            "/api/alerts/RULE-001",
            json={"enabled": False},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["enabled"] == False

    def test_update_alert_rule_as_analyst_forbidden(self, client, analyst_headers):
        """Test that analyst cannot update alert rules"""
        response = client.put(
            "/api/alerts/RULE-001",
            json={"enabled": False},
            headers=analyst_headers
        )
        assert response.status_code == 403
