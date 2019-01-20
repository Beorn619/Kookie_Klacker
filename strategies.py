from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def update(self, player):
        raise NotImplementedError()


class KagazzieAI(Strategy):
    def update(self, player):
        pass