from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def update(self, player):
        raise NotImplementedError()

class KagazzieAI(Strategy):
    def __init__(self, player):
        self.player = player
    def update(self):
        self.player.stats()