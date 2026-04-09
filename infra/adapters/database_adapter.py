from sqlalchemy.orm import sessionmaker, Session

from infra.db.models import MovieModel


class DatabaseAdapter:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def fetch_all(self) -> list[dict]:
        with self._session_factory() as session:
            rows = session.query(MovieModel).all()
            return [_to_dict(row) for row in rows]

    def save_all(self, records: list[dict]) -> None:
        with self._session_factory() as session:
            session.add_all([_to_model(r) for r in records])
            session.commit()


def _to_dict(model: MovieModel) -> dict:
    return {
        "year": model.year,
        "title": model.title,
        "studios": model.studios,
        "producers": model.producers,
        "winner": model.winner,
    }


def _to_model(record: dict) -> MovieModel:
    return MovieModel(
        year=record["year"],
        title=record["title"],
        studios=record["studios"],
        producers=record["producers"],
        winner=record["winner"],
    )
