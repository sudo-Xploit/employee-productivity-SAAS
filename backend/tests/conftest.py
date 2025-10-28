import os
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Create a simple test app
app = FastAPI(title="Test App")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Test API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


@pytest.fixture
def client():
    """Create a test client for the app."""
    return TestClient(app)
