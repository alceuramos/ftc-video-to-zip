from datetime import UTC, datetime, timedelta

from fastapi import HTTPException
from pytest import raises

from core.security import (
    INVALID_TOKEN_MESSAGE,
    TOKEN_EXPIRED_MESSAGE,
    encode_jwt,
    verify_jwt,
)


def test_verify_jwt_success():
    payload = {
        "sub": "test@example.com",
        "is_admin": True,
        "is_reader": True,
        "is_editor": False,
        "exp": datetime.now(UTC) + timedelta(minutes=30),
    }
    verify_jwt(encode_jwt(payload))


def test_verify_jwt_expired_token():
    payload = {
        "sub": "test@example.com",
        "is_admin": True,
        "is_reader": True,
        "is_editor": False,
        "exp": datetime.now(UTC) - timedelta(minutes=30),
    }
    encoded_token = encode_jwt(payload, "secret", "HS256")
    with raises(HTTPException, match=f"401: {TOKEN_EXPIRED_MESSAGE}"):
        verify_jwt(encoded_token, "secret", "HS256")


def test_verify_jwt_invalid_token():
    payload = {
        "sub": "test@example.com",
        "is_admin": True,
        "is_reader": True,
        "is_editor": False,
        "exp": datetime.now(UTC) - timedelta(minutes=30),
    }
    encoded_token = encode_jwt(payload, "wrong-secret", "HS256")
    with raises(HTTPException, match=f"401: {INVALID_TOKEN_MESSAGE}"):
        verify_jwt(encoded_token, "secret", "HS256")
