import os

from config import Config


class AppConfig(Config):
    DATABASE_URL: str = "sqlite:///:memory:"
    CSV_PATH: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../infra/data/movielist.csv"))
    IN_MEMORY_DB: bool = True
