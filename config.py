import os


class Config:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///:memory:")
    CSV_PATH: str = os.getenv("CSV_PATH", "data/movielist.csv")
    API_TOKEN: str | None = os.getenv("API_TOKEN")
