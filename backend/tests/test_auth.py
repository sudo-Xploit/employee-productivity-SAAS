import pytest
from fastapi.testclient import TestClient


@pytest.mark.auth
def test_login(client, test_user):
    """Test user login"""
    login_data = {
        "username": "test@example.com",
        "password": "testpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    
    # Check response structure
    tokens = response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert "token_type" in tokens
    assert tokens["token_type"] == "bearer"


@pytest.mark.auth
def test_login_wrong_password(client, test_user):
    """Test login with wrong password"""
    login_data = {
        "username": "test@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401
    assert "detail" in response.json()


@pytest.mark.auth
def test_login_nonexistent_user(client):
    """Test login with nonexistent user"""
    login_data = {
        "username": "nonexistent@example.com",
        "password": "password"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401
    assert "detail" in response.json()


@pytest.mark.auth
def test_get_current_user(client, user_token_headers):
    """Test getting current user info"""
    response = client.get("/api/v1/auth/me", headers=user_token_headers)
    assert response.status_code == 200
    
    user_data = response.json()
    assert user_data["email"] == "test@example.com"
    assert user_data["full_name"] == "Test User"
    assert "id" in user_data
    assert "hashed_password" not in user_data


@pytest.mark.auth
def test_get_current_user_invalid_token(client):
    """Test getting current user with invalid token"""
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 401


@pytest.mark.auth
def test_refresh_token(client, refresh_token):
    """Test refreshing access token"""
    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    
    tokens = response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"


@pytest.mark.auth
def test_refresh_token_invalid(client):
    """Test refreshing with invalid token"""
    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": "invalid_token"}
    )
    assert response.status_code == 401


@pytest.mark.auth
def test_register_user(client):
    """Test user registration"""
    user_data = {
        "email": "newuser@example.com",
        "password": "newpassword",
        "full_name": "New User",
        "role": "ANALYST"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    
    new_user = response.json()
    assert new_user["email"] == "newuser@example.com"
    assert new_user["full_name"] == "New User"
    assert "id" in new_user
    assert "hashed_password" not in new_user


@pytest.mark.auth
def test_register_existing_user(client, test_user):
    """Test registering with existing email"""
    user_data = {
        "email": "test@example.com",  # Already exists
        "password": "password",
        "full_name": "Another User",
        "role": "ANALYST"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 400
    assert "detail" in response.json()
