import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_read_root(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Welcome to the Test API"


@pytest.mark.unit
def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.unit
def test_docs_endpoint(client):
    """Test that the docs endpoint is accessible"""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
