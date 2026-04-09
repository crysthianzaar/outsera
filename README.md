# Golden Raspberry Awards API

RESTful API to read the list of nominees and winners in the **Worst Film** category of the Golden Raspberry Awards.

---

## Requirements

- Docker
- Docker Compose

---

## Running the API

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

---

## Running the Integration Tests

```bash
docker-compose --profile test run --rm test
```

Tests run against an in-memory SQLite database — no external dependencies required.

---

## Running Tests Locally

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
pytest -v
```

---

## API Endpoint

### `GET /producers/award-intervals`

Returns the producer with the longest and shortest interval between two consecutive awards.

```bash
curl http://localhost:8000/producers/award-intervals
```

**Response:**

```json
{
  "min": [
    {
      "producer": "Joel Silver",
      "interval": 1,
      "previousWin": 1990,
      "followingWin": 1991
    }
  ],
  "max": [
    {
      "producer": "Matthew Vaughn",
      "interval": 13,
      "previousWin": 2002,
      "followingWin": 2015
    }
  ]
}
```

### Utility endpoints

| Method | Route     | Description    |
|--------|-----------|----------------|
| GET    | `/ping`   | Liveness check |
| GET    | `/health` | Health status  |

---

## Architecture

The project follows Clean Architecture with strict layer separation:

- **`domain/`** — pure business logic, zero framework dependencies
  - `entities/` — immutable domain objects (`Movie`)
  - `repositories/` — abstract protocols (`MovieReader`, `MovieWriter`)
  - `services/` — domain algorithms (`award_interval_service`)
  - `types/` — value objects (`ProducerInterval`, `AwardIntervalResult`)
  - `usecases/` — use case orchestration (`GetAwardIntervalsUseCase`)
- **`api/`** — HTTP layer (Flask blueprints, Pydantic response models)
- **`infra/`** — infrastructure implementations
  - `adapters/` — isolation layer: `DatabaseAdapter`, `CsvAdapter`, `MovieStore` protocol, `MovieRecord` typed dict
  - `db/` — SQLAlchemy 2.0 ORM model and session factory
  - `loaders/` — CSV ingestion pipeline
  - `repositories/` — `MovieReadRepository` and `MovieWriteRepository`

---

## Project Structure

```
.
├── api/
│   ├── blueprints/
│   │   ├── health.py                   # Liveness and health endpoints
│   │   └── producers.py                # Award intervals endpoint
│   └── responses.py                    # Pydantic response models
├── domain/
│   ├── entities/
│   │   └── movie.py                    # Immutable Movie entity
│   ├── repositories/
│   │   └── movie_repository.py         # MovieReader / MovieWriter protocols
│   ├── services/
│   │   └── award_interval_service.py   # Core business logic
│   ├── types/
│   │   ├── award_interval_result.py
│   │   └── producer_interval.py
│   └── usecases/
│       └── get_award_intervals.py
├── infra/
│   ├── adapters/
│   │   ├── csv_adapter.py              # CSV file reader
│   │   ├── data_source.py              # DataSource / MovieStore protocols
│   │   ├── database_adapter.py         # SQLAlchemy isolation layer
│   │   └── movie_record.py             # MovieRecord TypedDict
│   ├── data/
│   │   └── movielist.csv
│   ├── db/
│   │   ├── base.py
│   │   ├── movie_model.py              # SQLAlchemy 2.0 ORM model
│   │   └── session.py
│   ├── loaders/
│   │   └── movie_loader.py             # CSV → domain entity mapping
│   └── repositories/
│       ├── movie_repository_impl.py    # MovieReadRepository / MovieWriteRepository
├── tests/integration/
├── config.py                           # Settings via pydantic-settings
├── create_app.py                       # Flask application factory
├── main.py                             # WSGI entrypoint (gunicorn)
├── pyproject.toml                      # Tool configuration (ruff, mypy, pytest)
├── Dockerfile                          # Multi-stage: production + test
├── docker-compose.yml
├── requirements.txt
└── requirements-dev.txt
```

---

## Environment Variables

| Variable       | Default                    | Description                                  |
|----------------|----------------------------|----------------------------------------------|
| `DATABASE_URL` | `sqlite:///:memory:`       | Database URL                                 |
| `CSV_PATH`     | `infra/data/movielist.csv` | Path to the movies CSV file                  |
| `IN_MEMORY_DB` | `true`                     | Use StaticPool for in-memory SQLite database |
