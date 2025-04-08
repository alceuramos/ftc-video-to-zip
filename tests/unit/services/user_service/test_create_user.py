import pytest

from db.postgresql.models.user import User
from repositories.user import UserRepository
from schemas.user import UserInput
from services.user_service import EMAIL_ALREADY_USED_ERROR, UserService


def test_create_user_success(
    user_service: UserService, mock_user_repo: UserRepository
):
    user_data = UserInput(
        name="John Doe", email="john@example.com", password=""
    )
    mock_user = User(id=1, name=user_data.name, email=user_data.email)
    mock_user_repo.add.return_value = mock_user
    mock_user_repo.get_by_email.return_value = None

    result = user_service.create_user(user_data)
    assert result.name == user_data.name
    assert result.email == user_data.email


def test_create_user_already_registered(
    user_service: UserService, mock_user_repo: UserRepository
):
    user_data = UserInput(
        name="John Doe", email="john@example.com", password="password"
    )
    mock_user = User(id=1, name=user_data.name, email=user_data.email)
    mock_user_repo.add.return_value = mock_user
    mock_user_repo.get_by_email.return_value = mock_user

    with pytest.raises(ValueError, match=EMAIL_ALREADY_USED_ERROR):
        user_service.create_user(user_data)
