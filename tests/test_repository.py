import pytest

from fastapi_start.repository import UserRepository


@pytest.fixture()
def user_repository(session):
    return UserRepository(session)


def test_get_user(user_repository):
    assert user_repository.get_users() == []


def test_create_user(user_repository):
    created_user = user_repository.create_user("John Doe")

    assert created_user.id == 1
    assert created_user.name == "John Doe"
    assert user_repository.get_users() == [created_user]
