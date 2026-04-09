import csv


class CsvAdapter:
    def __init__(self, path: str, delimiter: str = ";", encoding: str = "utf-8-sig") -> None:
        self._path = path
        self._delimiter = delimiter
        self._encoding = encoding

    def fetch_all(self) -> list[dict]:
        with open(self._path, newline="", encoding=self._encoding) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=self._delimiter)
            return [dict(row) for row in reader]
