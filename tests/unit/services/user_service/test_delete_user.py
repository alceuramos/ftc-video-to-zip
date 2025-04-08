from repositories.user import UserRepository
from schemas.user import User
from services.user_service import UserService


def test_delete_user(
    user_service: UserService, mock_user_repo: UserRepository
):
    user_email = "john@example.com"
    mock_user = User(
        id=1,
        name="John Doe",
        email=user_email,
        is_admin=False,
        is_editor=False,
        is_reader=True,
    )
    mock_user_repo.get_by_id.return_value = mock_user
    mock_user_repo.delete_user.return_value = mock_user

    result = user_service.delete_user(mock_user.id)
    assert result.name == mock_user.name
    assert result.email == mock_user.email
