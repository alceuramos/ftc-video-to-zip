from datetime import UTC, datetime, timedelta

import jwt

from core.security import decode_jwt


def test_decode_jwt():
    payload = {
        "sub": "test@example.com",
        "is_admin": True,
        "is_reader": True,
        "is_editor": False,
        "exp": datetime.now(UTC) + timedelta(minutes=30),
    }
    token = jwt.encode(payload, "secret", "HS256")
    decoded_payload = decode_jwt(token, "secret", "HS256")
    payload["exp"] = int(payload["exp"].timestamp())
    assert decoded_payload == payload
