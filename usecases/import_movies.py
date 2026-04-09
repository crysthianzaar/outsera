from domain.entities.movie import Movie
from domain.repositories.movie_repository import MovieRepository


class ImportMoviesUseCase:
    def __init__(self, repository: MovieRepository) -> None:
        self._repository = repository

    def execute(self, movies: list[Movie]) -> None:
        self._repository.save_all(movies)
