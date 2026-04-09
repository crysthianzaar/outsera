from flask import Blueprint, jsonify

from api.responses import AwardIntervalsResponse
from domain.repositories.movie_repository import MovieReader
from domain.usecases.get_award_intervals import GetAwardIntervalsUseCase


def create_producers_blueprint(use_case: GetAwardIntervalsUseCase) -> Blueprint:
    bp = Blueprint("producers", __name__)

    @bp.get("/producers/award-intervals")
    def award_intervals():
        result = use_case.execute()
        return jsonify(AwardIntervalsResponse.from_domain(result).model_dump())

    return bp
