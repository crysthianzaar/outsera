from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str = "sqlite:///:memory:"
    CSV_PATH: str = "infra/data/movielist.csv"
    IN_MEMORY_DB: bool = True
