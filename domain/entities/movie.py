from dataclasses import dataclass


@dataclass
class Movie:
    year: int
    title: str
    studios: str
    producers: list[str]
    winner: bool
