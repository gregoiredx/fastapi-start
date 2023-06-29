from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends
from fastapi import FastAPI

from fastapi_start.repository import User
from fastapi_start.repository import UserRepository

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/users/")
def create_user(
    user_repository: Annotated[UserRepository, Depends()], name: str
) -> User:
    return user_repository.create_user(name=name)


@app.get("/users/")
def read_users(user_repository: Annotated[UserRepository, Depends()]) -> Sequence[User]:
    return user_repository.get_users()
