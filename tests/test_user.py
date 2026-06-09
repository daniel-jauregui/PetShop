import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreate


def test_user_create_schema_success():
    """Tests that the schema accepts passwords with valid lengths."""
    # Valid lower boundary (8 characters)
    payload_min = {"username": "testuser", "password": "a" * 8}
    user_min = UserCreate(**payload_min)
    assert user_min.password == "a" * 8

    # Valid upper boundary (72 characters)
    payload_max = {"username": "testuser", "password": "a" * 72}
    user_max = UserCreate(**payload_max)
    assert user_max.password == "a" * 72


def test_user_create_schema_password_too_short():
    """Tests that the schema rejects passwords shorter than 8 characters."""
    payload = {"username": "testuser", "password": "a" * 7}

    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**payload)

    # Verify that the error relates to the minimum length constraint
    assert "string_too_short" in str(exc_info.value)


def test_user_create_schema_password_too_long():
    """Tests that the schema rejects passwords longer than 72 characters."""
    payload = {"username": "testuser", "password": "a" * 73}

    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**payload)

    # Verify that Pydantic stops execution due to character excess
    assert "string_too_long" in str(exc_info.value)
