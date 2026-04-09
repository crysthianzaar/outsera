from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.types import JSON

from infra.db.base import Base


class MovieModel(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    title = Column(String(500), nullable=False)
    studios = Column(Text, nullable=False)
    producers = Column(JSON, nullable=False)
    winner = Column(Boolean, nullable=False, default=False)
