from http import HTTPStatus

from fastapi_start.repository import UserRepository


def test_read_main(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"Hello": "World"}


def test_get_users(client):
    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


def test_create_user(client, app_session):
    response = client.post("/users", params={"name": "John"})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "name": "John"}
    users = UserRepository(app_session).get_users()
    assert len(users) == 1
    assert users[0].name == "John"


def test_create_and_get_user(client):
    client.post("/users", params={"name": "John"})
    client.post("/users", params={"name": "Bob"})
    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [{"id": 1, "name": "John"}, {"id": 2, "name": "Bob"}]


def test_get_existing_user(client, app_session):
    UserRepository(app_session).create_user("Bob")

    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [{"id": 1, "name": "Bob"}]
