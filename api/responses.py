from pydantic import BaseModel

from domain.types.award_interval_result import AwardIntervalResult
from domain.types.producer_interval import ProducerInterval


class ProducerIntervalSchema(BaseModel):
    producer: str
    interval: int
    previousWin: int
    followingWin: int

    @classmethod
    def from_domain(cls, interval: ProducerInterval) -> "ProducerIntervalSchema":
        return cls(
            producer=interval.producer,
            interval=interval.interval,
            previousWin=interval.previous_win,
            followingWin=interval.following_win,
        )


class AwardIntervalsResponse(BaseModel):
    min: list[ProducerIntervalSchema]
    max: list[ProducerIntervalSchema]

    @classmethod
    def from_domain(cls, result: AwardIntervalResult) -> "AwardIntervalsResponse":
        return cls(
            min=[ProducerIntervalSchema.from_domain(i) for i in result.min],
            max=[ProducerIntervalSchema.from_domain(i) for i in result.max],
        )
