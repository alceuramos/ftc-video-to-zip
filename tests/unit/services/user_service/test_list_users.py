from repositories.user import UserRepository
from schemas.user import User
from services.user_service import UserService


def test_list_users(user_service: UserService, mock_user_repo: UserRepository):
    mock_users = [
        User(
            id=1,
            name="John Doe",
            email="john@example.com",
            is_admin=False,
            is_editor=False,
            is_reader=True,
        ),
        User(
            id=2,
            name="Jack Doe",
            email="Jack@example.com",
            is_admin=False,
            is_editor=False,
            is_reader=True,
        ),
    ]
    mock_user_repo.list_users.return_value = mock_users

    result = user_service.list_users(limit=10, page=1)
    assert len(result) == 2
