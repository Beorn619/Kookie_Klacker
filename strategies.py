from abc import ABC, abstractmethod
from typing import Dict
from Kookie_Klacker2 import Player, BuildingGroup

class Strategy(ABC):
    @abstractmethod
    def buy_buildings(self, player: Player) -> Dict[BuildingGroup, int]:
        raise NotImplementedError()

    @abstractmethod
    def buy_upgrades(self, player: Player):
        raise NotImplementedError()


class KagazzieAI(Strategy):
    def buy_buildings(self, player: Player) -> Dict[BuildingGroup, int]:
        pass

    def buy_upgrades(self, player: Player):
        pass


class DumbFriendAI(Strategy):
    def buy_buildings(self, player: Player) -> Dict[BuildingGroup, int]:
        pass

    def buy_upgrades(self, player: Player):
        pass   
