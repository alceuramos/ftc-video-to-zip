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
def test_list_users(
    client: TestClient, user_service_mock: UserService, setup_wiring
):
    mock_users = [
        User(
            id="123",
            name="User Test",
            email="email@test.com",
            is_admin=False,
            is_editor=False,
            is_reader=True,
            created_at="2025-02-08T12:57:18.267Z",
            updated_at="2025-02-08T12:57:18.267Z",
        ),
        User(
            id="456",
            name="User Test",
            email="email2@test.com",
            is_admin=False,
            is_editor=False,
            is_reader=True,
            created_at="2025-02-08T12:57:18.267Z",
            updated_at="2025-02-08T12:57:18.267Z",
        ),
    ]
    user_service_mock.list_users.return_value = mock_users

    response = client.get(
        "/v1/users",
        headers={"Authorization": "Bearer asda"},
    )

    assert response.status_code == 200
    assert len(response.json()) == len(mock_users)
