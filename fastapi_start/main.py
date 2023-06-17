from fastapi import Depends
from fastapi import FastAPI
from sqlalchemy.orm import Session

from fastapi_start.database import yield_session
from fastapi_start.repository import UserRepository

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/users/")
def create_user(session: Session = Depends(yield_session)):
    return UserRepository(session).create_user(name="John")


@app.get("/users/")
def read_users(session: Session = Depends(yield_session)):
    return UserRepository(session).get_users()
