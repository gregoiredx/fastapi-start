from fastapi_start import job
from fastapi_start.repository import UserRepository


def test_create_user(job_session):
    job.create_user(name="John Test")

    users = UserRepository(job_session).get_users()
    assert len(users) == 1
    assert users[0].name == "John Test"
