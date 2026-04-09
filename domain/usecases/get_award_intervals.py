from domain.repositories.movie_repository import MovieReader
from domain.services.award_interval_service import calculate_award_intervals
from domain.types.award_interval_result import AwardIntervalResult


class GetAwardIntervalsUseCase:
    def __init__(self, repository: MovieReader) -> None:
        self._repository = repository

    def execute(self) -> AwardIntervalResult:
        movies = self._repository.find_all()
        return calculate_award_intervals(movies)
