from domain.entities.movie import Movie
from domain.repositories.movie_repository import MovieReader, MovieWriter
from infra.adapters.database_adapter import DatabaseAdapter


class MovieReadRepository(MovieReader):
    def __init__(self, db: DatabaseAdapter) -> None:
        self._db = db

    def find_all(self) -> list[Movie]:
        records = self._db.fetch_all()
        return [_db_record_to_movie(r) for r in records]


class MovieWriteRepository(MovieWriter):
    def __init__(self, db: DatabaseAdapter) -> None:
        self._db = db

    def save_all(self, movies: list[Movie]) -> None:
        self._db.save_all([_to_record(movie) for movie in movies])


def _db_record_to_movie(record: dict) -> Movie:
    return Movie(
        year=record["year"],
        title=record["title"],
        studios=record["studios"],
        producers=tuple(record["producers"]),
        winner=record["winner"],
    )


def _to_record(movie: Movie) -> dict:
    return {
        "year": movie.year,
        "title": movie.title,
        "studios": movie.studios,
        "producers": movie.producers,
        "winner": movie.winner,
    }
