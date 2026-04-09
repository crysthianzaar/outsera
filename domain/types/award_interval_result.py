from dataclasses import dataclass

from domain.types.producer_interval import ProducerInterval


@dataclass(frozen=True)
class AwardIntervalResult:
    min: tuple[ProducerInterval, ...]
    max: tuple[ProducerInterval, ...]
