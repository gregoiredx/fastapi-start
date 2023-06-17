from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///local.db", echo=True)

Session = sessionmaker(engine)


# Dependency
def yield_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
