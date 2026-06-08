from datetime import timedelta
import pytest
import jwt
from utils.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)


def test_password_hashing_and_verification():
    """Prueba que una contraseña se encripte correctamente y se pueda verificar."""
    password_plano = "mi_secreto_123"

    # 1. Generar el hash
    hash_resultado = get_password_hash(password_plano)

    # El hash no debe ser igual al texto plano
    assert hash_resultado != password_plano

    # 2. Verificar coincidencia correcta
    assert verify_password(password_plano, hash_resultado) is True

    # 3. Verificar que falle con una contraseña incorrecta
    assert verify_password("otra_contraseña", hash_resultado) is False


def test_create_access_token_success():
    """Prueba que el token JWT se cree con la estructura y datos correctos."""
    usuario_id = "user_99"

    # Generar el token
    token = create_access_token(subject=usuario_id)
    assert isinstance(token, str)

    # Decodificar el token localmente para validar su contenido (Payload)
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert payload.get("sub") == usuario_id
    assert "exp" in payload


def test_create_access_token_with_custom_expires():
    """Prueba la creación del token pasando un tiempo de expiración personalizado."""
    usuario_id = "user_100"
    tiempo_personalizado = timedelta(minutes=10)

    token = create_access_token(subject=usuario_id, expires_delta=tiempo_personalizado)
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert payload.get("sub") == usuario_id
