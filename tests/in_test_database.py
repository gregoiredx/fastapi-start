from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import StaticPool
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo_pool=True,
    echo=True,
)

_Session = sessionmaker(engine)


@contextmanager
def yield_auto_rollback_session() -> Generator[Session, None, None]:
    session = _Session()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
