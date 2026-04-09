from dataclasses import dataclass


@dataclass(frozen=True)
class ProducerInterval:
    producer: str
    interval: int
    previous_win: int
    following_win: int
