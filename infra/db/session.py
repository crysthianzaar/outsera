from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from infra.db.base import Base


def create_session_factory(database_url: str, in_memory: bool = False) -> sessionmaker[Session]:
    if in_memory:
        engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    else:
        engine = create_engine(database_url)

    Base.metadata.create_all(engine)
    return sessionmaker(engine, autoflush=False, autocommit=False)
