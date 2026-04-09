from flask import Flask, jsonify

from api.routes import bp
from config import Config
from infra.csv.csv_loader import load_movies_from_csv
from infra.db.session import create_session_factory
from infra.repositories.sqlalchemy_movie_repository import SQLAlchemyMovieRepository
from usecases.import_movies import ImportMoviesUseCase


def create_app(config: Config | None = None) -> Flask:
    app = Flask(__name__)

    cfg = config or Config()
    app.config["API_TOKEN"] = cfg.API_TOKEN

    session_factory = create_session_factory(cfg.DATABASE_URL)
    app.config["SESSION_FACTORY"] = session_factory

    _load_csv(cfg.CSV_PATH, session_factory)

    app.register_blueprint(bp)
    _register_error_handlers(app)

    return app


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error"}), 500


def _load_csv(csv_path: str, session_factory) -> None:
    movies = load_movies_from_csv(csv_path)
    with session_factory() as session:
        repo = SQLAlchemyMovieRepository(session)
        ImportMoviesUseCase(repo).execute(movies)
