from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client(app):
    return TestClient(app)


def test_read_main(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"Hello": "World"}


def test_get_users(client):
    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


def test_create_user(client):
    response = client.post("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "name": "John"}

    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [{"id": 1, "name": "John"}]


def test_create_and_get_user(client):
    client.post("/users")
    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [{"id": 1, "name": "John"}]
