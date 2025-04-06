from datetime import UTC, datetime, timedelta

import jwt

from src.core.security import encode_jwt


def test_encode_jwt():
    payload = {
        "sub": "test@example.com",
        "is_admin": True,
        "is_reader": True,
        "is_editor": False,
        "exp": datetime.now(UTC) + timedelta(minutes=30),
    }
    token = encode_jwt(payload, "secret", "HS256")
    decoded_token = jwt.decode(token, "secret", "HS256")
    payload["exp"] = int(payload["exp"].timestamp())
    assert decoded_token == payload
