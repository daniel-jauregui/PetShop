import uuid
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user_success():
    """Prueba que un usuario se pueda registrar exitosamente."""
    # Generamos un username único por cada corrida (ej. user_4a12b...)
    unique_username = f"user_{uuid.uuid4().hex[:8]}"

    payload = {
        "username": unique_username,
        "password": "password_seguro_123"
    }
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == payload["username"]
    assert "id" in data
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_user_already_exists():
    """Prueba que no se permita registrar un username que ya existe."""
    unique_username = f"user_{uuid.uuid4().hex[:8]}"
    payload = {
        "username": unique_username,
        "password": "password_seguro_123"
    }

    # Primer registro (Exitoso)
    client.post("/api/v1/auth/register", json=payload)

    # Intento de segundo registro con el mismo username exacto (Debe fallar)
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Username already registered."


def test_login_success():
    """Prueba que un usuario registrado pueda obtener su token JWT."""
    unique_username = f"user_{uuid.uuid4().hex[:8]}"
    password = "mi_super_password"

    # Registrar al usuario dinámico primero
    client.post("/api/v1/auth/register", json={"username": unique_username, "password": password})

    # Intentar hacer Login
    login_data = {
        "username": unique_username,
        "password": password
    }
    response = client.post("/api/v1/auth/token", data=login_data)

    assert response.status_code == status.HTTP_200_OK
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
