from typing import TypedDict


class MovieRecord(TypedDict):
    year: int
    title: str
    studios: str
    producers: list[str]
    winner: bool
