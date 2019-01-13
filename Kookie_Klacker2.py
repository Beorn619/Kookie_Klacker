#Kookie Klacker2
import math
#from strategies import Strategy, KagazzieAI
from abc import ABC, abstractmethod, abstractproperty
from typing import List, Dict, Tuple


building_cost_multiplyer = 1.15
building_sell_multiplyer = 4

#Things to ask damour
#Making building: BuildingGroup in def buy_building() and sell building too


class Player:
    """Players can Buy, sell, and they start with 15 cookies"""
    def __init__(self, name: str, ai):
        
        self.cookies = 2080
        self.total_cps = 0
        self.strategy = ai

        self.name = name

        self.owned_buildings = {

        }#All building types : how many the player owns
        
        

    def buy_building(self, building, amount: int = 1):
        price = math.floor(building.base_cost*(building_cost_multiplyer**(self.owned_buildings[building]+amount) - building_cost_multiplyer**(self.owned_buildings[building]))/.15)+1
        
        if building.can_buy == False:
            print(building.name)
            print("amount :", amount)
            raise Exception("You do not have the cookeis to buy this")
        print("Bought", amount, building.name)

        self.cookies -= price
        self.owned_buildings[building] += amount
        building.cps_total = self.owned_buildings[building]*building.cps_per
        building.next_cost = math.floor(building.base_cost*(building_cost_multiplyer**self.owned_buildings[building]))+1

        self.update_cps()
        self.check_buy()   
        
    def sell_building(self, building, amount: int = 1):
        if self.owned_buildings[building] < amount:
            raise Exception("You are trying to sell more building than you have")
        
        print("Sold", amount, building.name)

        self.owned_buildings[building] -= amount
        self.cookies += math.floor(building.next_cost/(building_sell_multiplyer**amount))

        if self.owned_buildings[building] != 0:
            building.next_cost = math.floor(building.base_cost*(building_cost_multiplyer**self.owned_buildings[building]))+1
        else:
            building.next_cost = building.base_cost
        building.cps_total = self.owned_buildings[building]*building.cps_per

        self.update_cps()
        self.check_buy()
            
    def update_cps(self):
        total = 0
        for building_type in self.owned_buildings.keys():
            total += self.owned_buildings[building_type]*building_type.cps_per
        self.total_cps = total

    def stats(self):
        pass


    def check_buy(self):
        pass



class BuildingGroup(ABC):
    def __init__(self, player: Player):
        self._player = player
    
    @abstractproperty
    def base_cps(self) -> int:
        raise NotImplementedError()

    @abstractproperty
    def upgrades(self) -> List['Upgrade']:
        raise NotImplementedError()

    def cps_per(self, upgrade_count: int) -> float:
        return self.base_cps * (2**upgrade_count)

    @abstractmethod
    def stats(self):
        pass

class Upgrade:
    pass # TODO


class Grandma(BuildingGroup):
    @property
    def base_cps(self):
        return 1