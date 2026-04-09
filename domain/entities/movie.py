import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Movie:
    year: int
    title: str
    studios: str
    producers: tuple[str, ...]
    winner: bool

    @staticmethod
    def parse_producers(raw_producers: str) -> tuple[str, ...]:
        normalized = re.sub(r"\s+and\s+", ", ", raw_producers, flags=re.IGNORECASE)
        return tuple(name.strip() for name in normalized.split(",") if name.strip())
