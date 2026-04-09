from typing import Protocol

from domain.entities.movie import Movie


class MovieRepository(Protocol):
    def save_all(self, movies: list[Movie]) -> None: ...

    def find_all(self) -> list[Movie]: ...
