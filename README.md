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

| Method | Route     | Description          |
|--------|-----------|----------------------|
| GET    | `/ping`   | Liveness check       |
| GET    | `/health` | Health status        |

---

## Architecture

The project follows a clean layered architecture:

- **`domain/`** — pure business logic, no framework dependencies
  - `entities/` — immutable domain objects (`Movie`)
  - `repositories/` — abstract protocols (`MovieReader`, `MovieWriter`)
  - `services/` — domain algorithms (`award_interval_service`)
  - `types/` — value objects (`ProducerInterval`, `AwardIntervalResult`)
  - `usecases/` — use case orchestration
- **`api/`** — HTTP layer (Flask blueprints, Pydantic response models)
- **`infra/`** — infrastructure implementations (SQLAlchemy, CSV loader)

---

## Project Structure

```
.
├── api/
│   ├── blueprints/
│   │   ├── health.py               # Observability endpoints
│   │   └── producers.py            # Domain endpoints
│   └── responses.py                # Pydantic response models
├── domain/
│   ├── entities/
│   │   └── movie.py                # Immutable Movie entity
│   ├── repositories/
│   │   └── movie_repository.py     # MovieReader / MovieWriter protocols
│   ├── services/
│   │   └── award_interval_service.py
│   ├── types/
│   │   ├── award_interval_result.py
│   │   └── producer_interval.py
│   └── usecases/
│       └── get_award_intervals.py
├── infra/
│   ├── data/
│   │   └── movielist.csv
│   ├── db/
│   │   ├── base.py
│   │   ├── models.py               # SQLAlchemy 2.0 ORM models
│   │   └── session.py
│   ├── loaders/
│   │   └── movie_file_loader.py
│   └── repositories/
│       ├── repository_factory.py
│       └── sqlalchemy_movie_repository.py
├── tests/integration/
├── config.py                       # Settings via pydantic-settings
├── create_app.py                   # Flask application factory
├── main.py                         # WSGI entrypoint (gunicorn main:app)
├── Dockerfile                      # Multi-stage: production + test
├── docker-compose.yml
└── requirements.txt
```

---

## Environment Variables

| Variable       | Default                    | Description                                  |
|----------------|----------------------------|----------------------------------------------|
| `DATABASE_URL` | `sqlite:///:memory:`       | Database URL                                 |
| `CSV_PATH`     | `infra/data/movielist.csv` | Path to the movies CSV file                  |
| `IN_MEMORY_DB` | `true`                     | Use StaticPool for in-memory SQLite database |
