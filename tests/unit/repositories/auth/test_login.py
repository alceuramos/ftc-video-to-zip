from freezegun import freeze_time

from repositories.user import UserRepository
from schemas.user import User, UserCredentials
from services.auth_service import AuthService


def test_login_success(
    auth_service: AuthService, mock_user_repo: UserRepository
):
    mock_user = User(
        id=1,
        name="John Doe",
        email="john@example.com",
        is_admin=False,
        is_editor=False,
        is_reader=True,
    )
    mock_credentials = UserCredentials(
        email="john@example.com", password="password"
    )
    mock_user_repo.validate_credentials.return_value = mock_user
    expected_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huQGV4YW1wbGUuY29tIiwiaXNfYWRtaW4iOmZhbHNlLCJpc19yZWFkZXIiOnRydWUsImlzX2VkaXRvciI6ZmFsc2UsImV4cCI6MTczNTY5MzIwMH0.80t2TVjQZBYIcWvHIYj-sT7mYybLXrouUmsMjIeaEuM"  # noqa: E501

    with freeze_time("2025-01-01"):
        result = auth_service.login(mock_credentials)
    assert result.access_token == expected_token
