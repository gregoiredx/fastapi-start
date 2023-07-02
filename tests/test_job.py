from fastapi_start.repository import UserRepository


def test_create_user(job_app, job_session):
    job_app.run("create_user", "John Test")

    users = UserRepository(job_session).get_users()
    assert len(users) == 1
    assert users[0].name == "John Test"
