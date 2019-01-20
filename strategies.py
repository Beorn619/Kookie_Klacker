from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def update(self, player):
        raise NotImplementedError()

class KagazzieAI(Strategy):
    def update(self):
        print(self.owned_buildings)