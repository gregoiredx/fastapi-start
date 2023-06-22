from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi_start.settings import Settings
from fastapi_start.settings import get_settings


@lru_cache
def get_engine(db_url: str, echo: bool) -> Engine:
    return create_engine(db_url, echo=echo)


def yield_session(settings: Annotated[Settings, Depends(get_settings)]):
    engine = get_engine(settings.db_url, echo=True)
    session = Session(engine)
    try:
        yield session
    finally:
        session.commit()
        session.close()


class Repository:
    def __init__(self, session: Session = Depends(yield_session)):
        self.session = session
