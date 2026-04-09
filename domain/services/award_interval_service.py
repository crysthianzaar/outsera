from domain.entities.movie import Movie
from domain.services.award_interval_result import AwardIntervalResult
from domain.services.producer_interval import ProducerInterval


def calculate_award_intervals(movies: list[Movie]) -> AwardIntervalResult:
    winners = [m for m in movies if m.winner]

    producer_years: dict[str, list[int]] = {}
    for movie in winners:
        for producer in movie.producers:
            producer_years.setdefault(producer, []).append(movie.year)

    intervals: list[ProducerInterval] = []
    for producer, years in producer_years.items():
        sorted_years = sorted(years)
        for i in range(1, len(sorted_years)):
            intervals.append(ProducerInterval(
                producer=producer,
                interval=sorted_years[i] - sorted_years[i - 1],
                previous_win=sorted_years[i - 1],
                following_win=sorted_years[i],
            ))

    if not intervals:
        return AwardIntervalResult(min_intervals=[], max_intervals=[])

    min_interval = min(i.interval for i in intervals)
    max_interval = max(i.interval for i in intervals)

    return AwardIntervalResult(
        min_intervals=[i for i in intervals if i.interval == min_interval],
        max_intervals=[i for i in intervals if i.interval == max_interval],
    )
