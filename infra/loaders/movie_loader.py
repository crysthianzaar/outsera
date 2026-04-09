from domain.entities.movie import Movie
from infra.adapters.csv_adapter import CsvAdapter


def load_movies(adapter: CsvAdapter) -> list[Movie]:
    return [_to_entity(record) for record in adapter.fetch_all()]


def _to_entity(record: dict) -> Movie:
    return Movie(
        year=int(record["year"].strip()),
        title=record["title"].strip(),
        studios=record["studios"].strip(),
        producers=Movie.parse_producers(record["producers"].strip()),
        winner=record.get("winner", "").strip().lower() == "yes",
    )
