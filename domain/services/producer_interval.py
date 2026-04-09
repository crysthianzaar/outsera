class ProducerInterval:
    def __init__(self, producer: str, interval: int, previous_win: int, following_win: int) -> None:
        self.producer = producer
        self.interval = interval
        self.previous_win = previous_win
        self.following_win = following_win
