from pydantic import BaseModel

from api.schemas import ProducerIntervalSchema


class AwardIntervalsResponse(BaseModel):
    min: list[ProducerIntervalSchema]
    max: list[ProducerIntervalSchema]
