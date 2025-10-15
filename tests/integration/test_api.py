import pytest
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

class TestAPI:
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()

    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_register_user(self):
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password": "testpass123",
            "role": "viewer"
        }
        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code in [200, 400]

    def test_proteins_endpoint_unauthorized(self):
        response = client.get("/api/proteins/")
        assert response.status_code == 401
