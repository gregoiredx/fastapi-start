from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_start.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"Hello": "World"}
