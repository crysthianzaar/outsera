from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from infra.db.base import Base


class MovieModel(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    year: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    studios: Mapped[str] = mapped_column(Text, nullable=False)
    producers: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    winner: Mapped[bool] = mapped_column(nullable=False, default=False)
