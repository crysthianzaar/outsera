from collections import defaultdict

from domain.entities.movie import Movie
from domain.types.award_interval_result import AwardIntervalResult
from domain.types.producer_interval import ProducerInterval


def calculate_award_intervals(movies: list[Movie]) -> AwardIntervalResult:
    winning_movies = [movie for movie in movies if movie.winner]

    win_years_by_producer = _group_win_years_by_producer(winning_movies)
    all_consecutive_intervals = _build_consecutive_intervals(win_years_by_producer)

    if not all_consecutive_intervals:
        return AwardIntervalResult(min=(), max=())

    return _select_min_and_max_intervals(all_consecutive_intervals)


def _group_win_years_by_producer(winning_movies: list[Movie]) -> dict[str, list[int]]:
    win_years_by_producer: dict[str, list[int]] = defaultdict(list)

    for movie in winning_movies:
        for producer in movie.producers:
            win_years_by_producer[producer].append(movie.year)

    return win_years_by_producer


def _build_consecutive_intervals(
    win_years_by_producer: dict[str, list[int]],
) -> list[ProducerInterval]:
    consecutive_intervals: list[ProducerInterval] = []

    for producer, win_years in win_years_by_producer.items():
        if len(win_years) < 2:
            continue

        sorted_win_years = sorted(win_years)

        for previous_year, following_year in zip(sorted_win_years, sorted_win_years[1:]):
            consecutive_intervals.append(ProducerInterval(
                producer=producer,
                interval=following_year - previous_year,
                previous_win=previous_year,
                following_win=following_year,
            ))

    return consecutive_intervals


def _select_min_and_max_intervals(
    all_intervals: list[ProducerInterval],
) -> AwardIntervalResult:
    shortest_interval = min(entry.interval for entry in all_intervals)
    longest_interval = max(entry.interval for entry in all_intervals)

    return AwardIntervalResult(
        min=tuple(entry for entry in all_intervals if entry.interval == shortest_interval),
        max=tuple(entry for entry in all_intervals if entry.interval == longest_interval),
    )
