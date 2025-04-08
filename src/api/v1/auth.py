from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.dependency_injection import Container
from core.security import verify_jwt
from schemas.user import UserCredentials
from services.auth_service import AuthService
from src.schemas.token import Token

router = APIRouter()


@router.post("/login", response_model=Token)
@inject
def login_user(
    user_credentials: UserCredentials,
    auth_service: AuthService = (Depends(Provide[Container.auth_service])),
):
    token = auth_service.login(user_credentials)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return token


@router.get("/validate-token")
def validate_token(
    auth: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    token = auth.credentials  # Extract Bearer token
    payload = verify_jwt(token)
    return {
        "message": "Token is valid",
        "email": payload["sub"],
        "is_admin": payload["is_admin"],
        "is_reader": payload["is_reader"],
        "is_editor": payload["is_editor"],
    }
