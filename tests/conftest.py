from unittest.mock import MagicMock, Mock

import pytest
from fastapi.testclient import TestClient

from api.app import app
from core.dependency_injection import Container
from repositories.user import UserRepository
from services.auth_service import AuthService
from services.user_service import UserService


@pytest.fixture
def mock_user_repo():
    return MagicMock(spec=UserRepository)


@pytest.fixture
def user_service(mock_user_repo):
    return UserService(user_repository=mock_user_repo)


@pytest.fixture
def auth_service(mock_user_repo):
    return AuthService(user_repository=mock_user_repo)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def user_service_mock():
    return Mock(spec=UserService)


@pytest.fixture
def container(user_service_mock):
    container = Container()
    container.user_service.override(user_service_mock)
    return container


@pytest.fixture()
def setup_wiring(container):
    container.init_resources()
    container.wire(modules=[__name__])
    yield
    container.unwire()
