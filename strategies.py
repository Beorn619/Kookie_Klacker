from abc import ABC, abstractmethod
from Kookie_Klacker2 import Player


class Strategy(ABC):
    def __init__(self, Player):
        self.player = Player
    @abstractmethod
    def update(self, player):
        raise NotImplementedError()


class KagazzieAI(Strategy):
    def update(self):
        if self.player.cursor.can_buy:
            self.player.buy_building(self.player.cursor)
        if (self.player.tick %1000) == 0:
            self.player.stats()