from repositories.user import UserRepository
from services.user_service import UserService


def test_is_user_authenticated(
    user_service: UserService, mock_user_repo: UserRepository
):
    user_email = "john@example.com"
    mock_user_repo.validate_credentials.return_value = True

    result = user_service.is_user_authenticated(user_email, "password")
    assert result is True


def test_is_user_authenticated_failed(
    user_service: UserService, mock_user_repo: UserRepository
):
    user_email = "john@example.com"
    mock_user_repo.validate_credentials.return_value = False

    result = user_service.is_user_authenticated(user_email, "wrong_password")
    assert result is False
