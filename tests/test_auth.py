import uuid
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user_success():
    """Tests that a user can register successfully."""
    # Generate a unique username for each run (e.g. user_4a12b...)
    unique_username = f"user_{uuid.uuid4().hex[:8]}"

    payload = {
        "username": unique_username,
        "password": "secure_password_123"
    }
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == payload["username"]
    assert "id" in data
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_user_already_exists():
    """Tests that registering an already existing username is not allowed."""
    unique_username = f"user_{uuid.uuid4().hex[:8]}"
    payload = {
        "username": unique_username,
        "password": "secure_password_123"
    }

    # First registration (Successful)
    client.post("/api/v1/auth/register", json=payload)

    # Attempt second registration with the exact same username (Must fail)
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Username already registered."


def test_login_success():
    """Tests that a registered user can obtain their JWT token."""
    unique_username = f"user_{uuid.uuid4().hex[:8]}"
    password = "my_super_password"

    # Register dynamic user first
    client.post("/api/v1/auth/register", json={"username": unique_username, "password": password})

    # Attempt to Login
    login_data = {
        "username": unique_username,
        "password": password
    }
    response = client.post("/api/v1/auth/token", data=login_data)

    assert response.status_code == status.HTTP_200_OK
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
