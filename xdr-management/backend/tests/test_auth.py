import pytest


class TestAuthentication:
    """Test authentication endpoints"""

    def test_login_success(self, client):
        """Test successful login"""
        response = client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "admin123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["username"] == "admin"
        assert data["user"]["role"] == "admin"

    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post(
            "/api/auth/login",
            data={"username": "admin", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user"""
        response = client.post(
            "/api/auth/login",
            data={"username": "nonexistent", "password": "password"}
        )
        assert response.status_code == 401

    def test_get_current_user(self, client, auth_headers):
        """Test get current user info"""
        response = client.get("/api/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "admin"
        assert data["role"] == "admin"

    def test_get_current_user_unauthorized(self, client):
        """Test get current user without token"""
        response = client.get("/api/auth/me")
        assert response.status_code == 401

    def test_refresh_token(self, client, auth_headers):
        """Test token refresh"""
        response = client.post("/api/auth/refresh", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    def test_different_user_roles(self, client):
        """Test login for different user roles"""
        users = [
            ("admin", "admin123", "admin"),
            ("analyst", "analyst123", "analyst"),
            ("viewer", "viewer123", "viewer")
        ]

        for username, password, expected_role in users:
            response = client.post(
                "/api/auth/login",
                data={"username": username, "password": password}
            )
            assert response.status_code == 200
            assert response.json()["user"]["role"] == expected_role
