from unittest.mock import patch

from fastapi.testclient import TestClient

from schemas.user import User, UserUpdate
from services.user_service import UserService


def mock_verify_jwt(
    token: str,
):
    """Mock JWT verification, returning a fake decoded payload."""
    return None


@patch("api.v1.users.verify_jwt", mock_verify_jwt)
def test_create_user_success(
    client: TestClient, user_service_mock: UserService, setup_wiring
):
    user_update = UserUpdate(
        **{
            "is_admin": False,
            "is_editor": False,
            "is_reader": True,
        }
    )
    user_id = "123"
    user_service_mock.update_user.return_value = User(
        id=user_id,
        name="John Doe",
        email="john@example.com",
        is_admin=user_update.is_admin,
        is_editor=user_update.is_editor,
        is_reader=user_update.is_reader,
        created_at="2025-02-08T12:57:18.267Z",
        updated_at="2025-02-08T12:57:18.267Z",
    )
    response = client.patch(
        f"v1/users/{user_id}",
        json=user_update.model_dump(),
        headers={"Authorization": "Bearer asda"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"
    assert response.json()["email"] == "john@example.com"
