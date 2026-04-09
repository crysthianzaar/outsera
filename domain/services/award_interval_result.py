from domain.services.producer_interval import ProducerInterval


class AwardIntervalResult:
    def __init__(self, min_intervals: list[ProducerInterval], max_intervals: list[ProducerInterval]) -> None:
        self.min = min_intervals
        self.max = max_intervals
