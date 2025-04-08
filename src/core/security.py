import hashlib

import jwt
from fastapi import HTTPException

from core.settings import settings

TOKEN_EXPIRED_MESSAGE = "Token expired"
INVALID_TOKEN_MESSAGE = "Invalid token"


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def encode_jwt(
    token_data: dict,
    secret_key: str = settings.SECRET_KEY,
    algorithm: str = settings.ALGORITHM,
) -> str:
    if secret_key is None:
        secret_key = settings.SECRET_KEY
    if algorithm is None:
        algorithm = settings.SECRET_KEY
    encoded_token = jwt.encode(
        token_data,
        key=secret_key,
        algorithm=algorithm,
    )
    return encoded_token


def decode_jwt(
    jwt_token: str,
    secret_key: str,
    algorithm: str,
) -> dict:
    # Decode JWT

    decoded_jwt = jwt.decode(
        jwt_token,
        key=secret_key,
        algorithms=algorithm,
    )
    return decoded_jwt


def verify_jwt(
    token: str,
    secret_key: str = settings.SECRET_KEY,
    algorithm: str = settings.ALGORITHM,
) -> dict:
    # Verify JWT
    if secret_key is None:
        secret_key = settings.SECRET_KEY
    if algorithm is None:
        algorithm = settings.SECRET_KEY

    try:
        payload = decode_jwt(token, secret_key=secret_key, algorithm=algorithm)
        return payload
    except jwt.ExpiredSignatureError as err:
        raise HTTPException(
            status_code=401, detail=TOKEN_EXPIRED_MESSAGE
        ) from err
    except jwt.InvalidTokenError as err:
        raise HTTPException(
            status_code=401, detail=INVALID_TOKEN_MESSAGE
        ) from err


def verify_password(password: str, hashed_password: str) -> bool:
    return hash_password(password) == hashed_password
