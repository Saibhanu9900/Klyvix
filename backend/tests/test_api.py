import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import create_access_token

client = TestClient(app)

from unittest.mock import patch, MagicMock, AsyncMock

@patch('app.models.database.SessionLocal')
@patch('app.core.cache.cache.redis')
@patch('app.core.retrieval.qdrant')
def test_health_check_healthy(mock_qdrant, mock_redis, mock_session):
    mock_db = MagicMock()
    mock_session.return_value = mock_db
    mock_redis.ping = AsyncMock(return_value=True)
    mock_qdrant.get_collections.return_value = []
    
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "Klyvix Backend"
    assert data["deps"]["database"] == "up"
    assert data["deps"]["redis"] == "up"
    assert data["deps"]["qdrant"] == "up"

def test_health_check_response_structure():
    response = client.get("/api/health")
    assert response.status_code in (200, 503)
    data = response.json()
    assert "status" in data
    assert "deps" in data

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
    token = create_access_token("test@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Empty post with auth (should fail on missing file, not 401)
    response = client.post("/api/upload", headers=headers)
    assert response.status_code == 422  # Unprocessable Entity (Missing file)
