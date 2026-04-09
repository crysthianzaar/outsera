from flask import Blueprint, current_app, jsonify

from api.auth import require_token
from api.award_intervals_response import AwardIntervalsResponse
from api.schemas import ProducerIntervalSchema
from usecases.get_award_intervals import GetAwardIntervalsUseCase

bp = Blueprint("api", __name__)


@bp.get("/ping")
def ping():
    return {"status": "pong"}


@bp.get("/health")
def health():
    return {"status": "ok"}


@bp.get("/producers/award-intervals")
@require_token
def award_intervals():
    session_factory = current_app.config["SESSION_FACTORY"]
    with session_factory() as session:
        from infra.repositories.sqlalchemy_movie_repository import SQLAlchemyMovieRepository
        repo = SQLAlchemyMovieRepository(session)
        result = GetAwardIntervalsUseCase(repo).execute()

    response = AwardIntervalsResponse(
        min=[
            ProducerIntervalSchema(
                producer=i.producer,
                interval=i.interval,
                previousWin=i.previous_win,
                followingWin=i.following_win,
            )
            for i in result.min
        ],
        max=[
            ProducerIntervalSchema(
                producer=i.producer,
                interval=i.interval,
                previousWin=i.previous_win,
                followingWin=i.following_win,
            )
            for i in result.max
        ],
    )
    return jsonify(response.model_dump())
