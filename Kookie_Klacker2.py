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
    def __init__(self, name: str):
        
        self.cookies = 2080
        self.total_cps = 0
        #self.strategy = ai

        self.name = name

        self.owned_buildings = {

        }#All building types : how many the player owns
        
        
    def buy_building(self, building: 'BuildingGroup', amount: int = 1):
        pass
        #TODO
     

    def sell_building(self, building: 'BuildingGroup', amount: int = 1):
        pass
        #TODO

    def building_count(self, building: 'BuildingGroup') -> 'BuildingGroup':
        return self.owned_buildings[building]
        
    def update_cps(self):
        pass #TODO

    def stats(self):
        pass#TODO


    def check_buy(self):
        pass#TODO



class BuildingGroup(ABC):
   def __init__(self, 
        player: Player,
        name: str,
        base_cost: int,
        cps: int
        ):
        self._player = player

        self. name = name

        self.base_cost = base_cost
        self.next_cost = base_cost
        
        self.base_cps = cps
        self.cps_mult = 1
    
    @abstractproperty
    def base_cps(self) -> int:
        raise NotImplementedError()
    
    @abstractmethod
    def cps_func(self):
        raise NotImplementedError()

    @abstractproperty
    def upgrades(self) -> 'PathedUpgrade':
        raise NotImplementedError()


    def cps_per(self, upgrade_count: int) -> float:
        return self.base_cps * (2**upgrade_count)

    @property
    def next_cost(self):
        #return math.ceil(self.base_cost*(self.building_cost_multiplyer**self.player.owned_buildings[building]))
        pass #TODO

    @abstractmethod
    def stats(self):
        #TODO
        pass
    
    def upgrade(self):
        self.upgrades.next()
        self._player
        

class Grandma(BuildingGroup):
    def __init__(self, 
        player: Player,
        name: str,
        base_cost: int,
        cps: int
        ):
        
        BuildingGroup.__init__(self, player, name, base_cost, cps)
        
        cps_increase = {
            1 : player.owned_buildings[Clicker]
            1.01 : player.owned_buildings[Farm]
        }
        #The idea is that integers would get added to CPS for every other building type, floats would get multiplied with self.mult
        #In this case grandma would be getting +1 cps per clicker
        #and +1% for every farm

        


    @property
    def base_cps(self):
        return 1

    def cps_func(self,player) -> 'cps':
        return player.count(Grandma) * 4


class PathedUpgrades:
    def __init__(
            self, 
            name, 
            cps_func,
            base_price: int, 
            reqs = [1,5,25,50,100,150,200,250,300,350,400], 
            mults=[5,10,100,100,100,1000,1000,1000,1000,10000]):
        self.name = name
        self.reqs = reqs
        self.mults = mults
        self.base_price = base_price
        self.price = base_price
        self.cps_func = cps_func


    @property
    def next_req(self):
        return self.reqs[0] if self.reqs else None

    @property
    def next_mult(self):
        return self.mults[0] if self.mults else None

    def next(self):
        self.reqs.pop()
        self.mults.pop()

    def cps(self, player):
        self.cps_func(player)        

        

class Upgrade:
    pass
