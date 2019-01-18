#Kookie Klacker2
import math
#from strategies import Strategy, KagazzieAI
from abc import ABC, abstractmethod, abstractproperty


building_cost_multiplyer = 1.15
building_sell_multiplyer = 4


class Player:
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
    
    def count(self, building: 'BuildingGroup'):
        return self.owned_buildings[building]



class BuildingGroup(ABC):
    def __init__(self, 
        player: Player,
        name: str,
        base_cost: int,
        cps: int,
        upgrades: 'PathedUpgrades'
        ):
        self._player = player

        self.name = name

        self.base_cost = base_cost


        self.upgrade_count = 0
        self.base_cps = cps

        self.upgrades = upgrades

    @abstractmethod
    def cps_per(self):
        raise NotImplementedError()

    @property
    def next_cost(self):
        return math.ceil(self.base_cost*(building_cost_multiplyer**self._player.owned_buildings[self]))

    @property
    def next_req(self):
        return self.upgrades.reqs[0] if self.upgrades.reqs else None

    @property
    def next_mult(self):
        return self.upgrades.mults[0] if self.upgrades.mults else None


    @abstractmethod
    def stats(self):
        raise NotImplementedError()
        

class Grandma(BuildingGroup):
    def __init__(self, 
        player: Player,
        name: str,
        base_cost: int,
        cps: int,
        ):
        
        upgrades = PathedUpgrades(name+'Upgrades', 1100)
        BuildingGroup.__init__(self, player, name, base_cost, cps, upgrades)
        
        self.name = name

    def cps_per(self) -> int:
        return self.base_cost*(2**self.upgrade_count)
    
    def upgrade(self):
        self.upgrades.next()
        self._player


    
    def stats(self):
        print(self.name)
        print("Base Cost:",self.base_cost)
        print("Upgrade Count:",self.upgrade_count)
        print("Base Cps:",self.base_cps)
        print("Cps Per:", self.cps_per(self))
        print("Next Cost:", self.next_cost(self))
        print("Next Upgrade Req:", self.next_req(self))
        print("Next Cost Multiplyer:", self.next_mult(self))
        print("Base Upgrade Price:",self.upgrades.base_price)



class PathedUpgrades:
    def __init__(
            self, 
            name,
            base_price: int, 
            reqs = [1,5,25,50,100,150,200,250,300,350,400], 
            mults= [5, 50, 50000, 5000000, 500000000, 500000000000, 500000000000000, 500000000000000000, 500000000000000000000, 5000000000000000000000000]):
        self.name = name
        self.reqs = reqs
        self.mults = mults
        self.base_price = base_price
    
    @property
    def next_price(self):
        return self.base_price*self.mults[0]
    
    @property
    def next_req(self):
        return self.reqs[0]
    
    def next(self):
        self.reqs.pop()
        self.mults.pop()


p = Player('Joe')
g = Grandma(p, 'Grandma', 100, 1)
g.stats()


