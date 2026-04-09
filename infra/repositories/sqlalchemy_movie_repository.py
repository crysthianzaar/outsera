from sqlalchemy.orm import Session

from domain.entities.movie import Movie
from domain.repositories.movie_repository import MovieRepository
from infra.db.models import MovieModel


def _to_entity(model: MovieModel) -> Movie:
    return Movie(
        year=model.year,
        title=model.title,
        studios=model.studios,
        producers=model.producers,
        winner=model.winner,
    )


def _to_model(entity: Movie) -> MovieModel:
    return MovieModel(
        year=entity.year,
        title=entity.title,
        studios=entity.studios,
        producers=entity.producers,
        winner=entity.winner,
    )


class SQLAlchemyMovieRepository(MovieRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save_all(self, movies: list[Movie]) -> None:
        self._session.add_all([_to_model(m) for m in movies])
        self._session.commit()

    def find_all(self) -> list[Movie]:
        return [_to_entity(m) for m in self._session.query(MovieModel).all()]
