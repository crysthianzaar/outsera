from domain.repositories.movie_repository import MovieRepository
from domain.services.award_interval_service import AwardIntervalResult, calculate_award_intervals


class GetAwardIntervalsUseCase:
    def __init__(self, repository: MovieRepository) -> None:
        self._repository = repository

    def execute(self) -> AwardIntervalResult:
        movies = self._repository.find_all()
        return calculate_award_intervals(movies)
