from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def update(self, player):
        raise NotImplementedError()


class KagazzieAI(Strategy):
    def __init__(self):
        self.butt= 0
    def update(self, player):
        if player.cursor.can_buy:
            player.buy_building(player.cursor)