from datetime import timedelta
import pytest
import jwt
from utils.security import (
    get_password_hash,
    verify_password,
    create_access_token
)
from app.core.config import settings


def test_password_hashing_and_verification():
    """Tests that a password is encrypted correctly and can be verified."""
    plain_password = "my_secret_123"

    # 1. Generate the hash
    hashed_password = get_password_hash(plain_password)

    # The hash must not be equal to the plain text
    assert hashed_password != plain_password

    # 2. Verify correct match
    assert verify_password(plain_password, hashed_password) is True

    # 3. Verify that it fails with an incorrect password
    assert verify_password("another_password", hashed_password) is False


def test_create_access_token_success():
    """Tests that the JWT token is created with the correct structure and data."""
    user_id = "user_99"

    # Generate token
    token = create_access_token(subject=user_id)
    assert isinstance(token, str)

    # Decode the token locally to validate its payload content
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert payload.get("sub") == user_id
    assert "exp" in payload


def test_create_access_token_with_custom_expires():
    """Tests token creation passing a custom expiration time."""
    user_id = "user_100"
    custom_expire = timedelta(minutes=10)

    token = create_access_token(subject=user_id, expires_delta=custom_expire)
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert payload.get("sub") == user_id
