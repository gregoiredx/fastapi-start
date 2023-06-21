import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi_start.repository import UserRepository
from fastapi_start.repository import mapper_registry

engine = create_engine("sqlite://")

Session = sessionmaker(engine)


@pytest.fixture(scope="module", autouse=True)
def _schemas():
    mapper_registry.metadata.create_all(engine)


@pytest.fixture()
def session():
    session = Session()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


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
