import pytest
from starlette.testclient import TestClient

from fastapi_start import main
from fastapi_start.database import yield_session
from fastapi_start.repository import mapper_registry
from tests import in_test_database


@pytest.fixture(scope="session", autouse=True)
def _schemas():
    mapper_registry.metadata.create_all(in_test_database.engine)


@pytest.fixture()
def session():
    with in_test_database.yield_auto_rollback_session() as session:
        yield session


@pytest.fixture(scope="session")
def app():
    return main.app


@pytest.fixture(autouse=True)
def app_session(app, session):
    app.dependency_overrides[yield_session] = lambda: session
    yield session
    del app.dependency_overrides[yield_session]


@pytest.fixture(scope="module")
def client(app):
    return TestClient(app)
