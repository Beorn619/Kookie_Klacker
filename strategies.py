from abc import ABC, abstractmethod
from Kookie_Klacker import Player, BuildingType

class Strategy(ABC):
    @abstractmethod
    def buy_buildings(self, player):
        raise NotImplementedError()

    @abstractmethod
    def buy_upgrades(self, player):
        raise NotImplementedError()


class KagazzieAI(Strategy):
    def buy_buildings(self, player):
        pass

    def buy_upgrades(self, player):
        pass


class DumbFriendAI(Strategy):
    def buy_buildings(self, player):
        pass

    def buy_upgrades(self, player):
        pass