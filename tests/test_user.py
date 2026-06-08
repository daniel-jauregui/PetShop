import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreate


def test_user_create_schema_success():
    """Prueba que el esquema acepte contraseñas con longitudes válidas."""
    # Límite inferior válido (8 caracteres)
    payload_min = {"username": "testuser", "password": "a" * 8}
    user_min = UserCreate(**payload_min)
    assert user_min.password == "a" * 8

    # Límite superior válido (72 caracteres)
    payload_max = {"username": "testuser", "password": "a" * 72}
    user_max = UserCreate(**payload_max)
    assert user_max.password == "a" * 72


def test_user_create_schema_password_too_short():
    """Prueba que el esquema rechace contraseñas de menos de 8 caracteres."""
    payload = {"username": "testuser", "password": "a" * 7}

    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**payload)

    # Verificamos que el error apueste a la longitud mínima
    assert "string_too_short" in str(exc_info.value)


def test_user_create_schema_password_too_long():
    """Prueba que el esquema rechace contraseñas de más de 72 caracteres."""
    payload = {"username": "testuser", "password": "a" * 73}

    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**payload)

    # Verificamos que Pydantic detenga la ejecución por exceso de caracteres
    assert "string_too_long" in str(exc_info.value)
