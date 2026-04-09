from domain.entities.movie import Movie
from infra.adapters.data_source import DataSource


def load_movies(adapter: DataSource) -> list[Movie]:
    return [_to_entity(record) for record in adapter.fetch_all()]


def _to_entity(record: dict) -> Movie:
    return Movie(
        year=int(record["year"].strip()),
        title=record["title"].strip(),
        studios=record["studios"].strip(),
        producers=Movie.parse_producers(record["producers"].strip()),
        winner=record.get("winner", "").strip().lower() == "yes",
    )
