from typing import Protocol


class DataSource(Protocol):
    def fetch_all(self) -> list[dict]: ...
