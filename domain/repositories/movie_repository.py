from typing import Protocol

from domain.entities.movie import Movie


class MovieReader(Protocol):
    def find_all(self) -> list[Movie]: ...


class MovieWriter(Protocol):
    def save_all(self, movies: list[Movie]) -> None: ...
