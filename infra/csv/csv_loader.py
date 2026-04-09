import csv
import re

from domain.entities.movie import Movie


def _parse_producers(raw: str) -> list[str]:
    normalized = re.sub(r"\s+and\s+", ", ", raw, flags=re.IGNORECASE)
    return [p.strip() for p in normalized.split(",") if p.strip()]


def load_movies_from_csv(path: str) -> list[Movie]:
    movies: list[Movie] = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            movies.append(Movie(
                year=int(row["year"].strip()),
                title=row["title"].strip(),
                studios=row["studios"].strip(),
                producers=_parse_producers(row["producers"].strip()),
                winner=row.get("winner", "").strip().lower() == "yes",
            ))
    return movies
