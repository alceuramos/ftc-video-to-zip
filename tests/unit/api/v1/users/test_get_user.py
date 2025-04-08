from unittest.mock import patch

from fastapi.testclient import TestClient

from schemas.user import User
from services.user_service import UserService


def mock_verify_jwt(
    token: str,
):
    """Mock JWT verification, returning a fake decoded payload."""
    return None


@patch("api.v1.users.verify_jwt", mock_verify_jwt)
def test_get_user(
    client: TestClient, user_service_mock: UserService, setup_wiring
):
    user_email = "email@test.com"
    user_service_mock.get_user_by_email.return_value = User(
        id="123",
        name="User Test",
        email=user_email,
        is_admin=False,
        is_editor=False,
        is_reader=True,
        created_at="2025-02-08T12:57:18.267Z",
        updated_at="2025-02-08T12:57:18.267Z",
    )

    response = client.get(
        f"/v1/users/{user_email}",
        headers={"Authorization": "Bearer asda"},
    )

    assert response.status_code == 200
