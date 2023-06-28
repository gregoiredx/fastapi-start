import pytest

from fastapi_start.repository import mapper_registry
from tests import in_test_database


@pytest.fixture(scope="session", autouse=True)
def _schemas():
    mapper_registry.metadata.create_all(in_test_database.engine)


@pytest.fixture()
def session():
    with in_test_database.yield_auto_rollback_session() as session:
        yield session
