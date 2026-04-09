from pydantic import BaseModel


class ProducerIntervalSchema(BaseModel):
    producer: str
    interval: int
    previousWin: int
    followingWin: int
