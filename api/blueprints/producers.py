from flask import Blueprint, current_app, jsonify

from api.responses import AwardIntervalsResponse
from domain.repositories.movie_repository import MovieReader
from domain.usecases.get_award_intervals import GetAwardIntervalsUseCase

bp = Blueprint("producers", __name__)


@bp.get("/producers/award-intervals")
def award_intervals():
    repo: MovieReader = current_app.config["MOVIE_REPO"]
    result = GetAwardIntervalsUseCase(repo).execute()
    return jsonify(AwardIntervalsResponse.from_domain(result).model_dump())
