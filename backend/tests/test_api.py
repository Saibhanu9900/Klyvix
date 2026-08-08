import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import create_access_token

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "Klyvix Backend"}

def test_list_personas():
    response = client.get("/api/personas")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert "id" in response.json()[0]

def test_protected_upload_endpoint_unauthorized():
    response = client.post("/api/upload")
    assert response.status_code == 401

def test_protected_upload_endpoint_authorized():
    # Create valid token
    token = create_access_token(data={"sub": "test@example.com"})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Empty post with auth (should fail on missing file, not 401)
    response = client.post("/api/upload", headers=headers)
    assert response.status_code == 422  # Unprocessable Entity (Missing file)
