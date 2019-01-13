from abc import ABC, abstractmethod
from typing import Dict
from Kookie_Klacker import Player, BuildingType

class Strategy(ABC):
    @abstractmethod
    def buy_buildings(self, player: Player) -> Dict[BuildingType, int]:
        raise NotImplementedError()

    @abstractmethod
    def buy_upgrades(self, player: Player):
        raise NotImplementedError()


class KagazzieAI(Strategy):
    def buy_buildings(self, player: Player) -> Dict[BuildingType, int]:
        pass

    def buy_upgrades(self, player: Player):
        pass


class DumbFriendAI(Strategy):
    def buy_buildings(self, player: Player) -> Dict[BuildingType, int]:
        pass

    def buy_upgrades(self, player: Player):
        pass   
