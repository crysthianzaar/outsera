import logging

from flask import Flask, jsonify

from api.blueprints.health import bp as health_bp
from api.blueprints.producers import bp as producers_bp
from config import Config
from infra.adapters.csv_adapter import CsvAdapter
from infra.adapters.database_adapter import DatabaseAdapter
from infra.db.session import create_session_factory
from infra.loaders.movie_loader import load_movies
from infra.repositories.movie_repository import MovieRepository

logger = logging.getLogger(__name__)


def create_app(config: Config | None = None) -> Flask:
    app = Flask(__name__)
    cfg = config or Config()

    session_factory = create_session_factory(cfg.DATABASE_URL, in_memory=cfg.IN_MEMORY_DB)
    db = DatabaseAdapter(session_factory)
    repo = MovieRepository(db)

    app.config["MOVIE_REPO"] = repo

    _seed_database(csv_path=cfg.CSV_PATH, repo=repo)
    app.register_blueprint(health_bp)
    app.register_blueprint(producers_bp)
    _register_error_handlers(app)

    logger.info("Application started. CSV loaded from: %s", cfg.CSV_PATH)

    return app


def _seed_database(csv_path: str, repo: MovieRepository) -> None:
    movies = load_movies(CsvAdapter(csv_path))
    repo.save_all(movies)


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(e):
        logger.warning("404 Not Found: %s", e)
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def internal_error(e):
        logger.exception("500 Internal Server Error: %s", e)
        return jsonify({"error": "Internal server error"}), 500
