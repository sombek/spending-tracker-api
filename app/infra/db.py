from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, create_session

from app.settings import settings

engine = create_engine(settings.DB_CONNECTION, pool_pre_ping=True)


# Return generator for infra session
def db_session() -> Generator[Session, None, None]:
    session = create_session(
        bind=engine,
        autocommit=False,
    )

    with session.begin():
        yield session


Base = declarative_base()
