#Kookie Klacker2
import math
#from strategies import Strategy, KagazzieAI
from abc import ABC, abstractmethod, abstractproperty


building_cost_multiplyer = 1.15
building_sell_multiplyer = 4


class Player:
    def __init__(self, name: str):

        self.cookies = 999999999999999
        #self.strategy = ai

        self.name = name

        self.owned_buildings = self.create_BuildingGroups()
    
    def create_BuildingGroups(self):
        self.cursor = Cursor(self, 'Cursor', 15, 0.1)
        self.grandma = DefaultBuilding(self, 'Grandma', 100.0, 1.0)
        self.farm = DefaultBuilding(self, 'Farm', 1100.0, 8.0)
        self.mine = DefaultBuilding(self, 'Mine', 12000.0, 47.0)
        self.factory = DefaultBuilding(self, 'Factory', 130000.0, 260.0)
        self.bank = DefaultBuilding(self, 'Bank', 1400000.0, 1400.0)
        self.temple = DefaultBuilding(self, 'Temple', 20000000.0, 7800.0)
        self.wizard_tower = DefaultBuilding(self, 'Wizard Tower', 330000000.0, 44000.0)
        self.shipment = DefaultBuilding(self, 'Shipment', 5100000000.0, 260000.0)
        self.alchemy_lab = DefaultBuilding(self, 'Alchemy Lab', 75000000000.0, 1600000.0)
        self.portal = DefaultBuilding(self, 'Portal', 1000000000000.0, 10000000.0)
        self.time_machine = DefaultBuilding(self, 'Time Machine', 14000000000000.0, 65000000.0)
        self.antimatter_condenser = DefaultBuilding(self, 'Anitmatter Condenser', 170000000000000.0, 430000000.0)
        self.prism = DefaultBuilding(self, 'Prism', 2100000000000000.0, 2900000000.0)
        self.chance_maker = DefaultBuilding(self, 'Chance Maker', 26000000000000000.0, 21000000000.0)
        self.fractal_engine = DefaultBuilding(self, 'Fractal Engine', 310000000000000000.0, 150000000000.0)
        return {
            self.cursor: 0,
            self.grandma: 0,
            self.farm: 0,
            self.mine: 0,
            self.factory: 0,
            self.bank: 0,
            self.temple: 0,
            self.wizard_tower: 0,
            self.shipment: 0,
            self.alchemy_lab: 0,
            self.portal: 0,
            self.time_machine: 0,
            self.antimatter_condenser: 0,
            self.prism: 0,
            self.chance_maker: 0,
            self.fractal_engine: 0
        }
        
    def buy_building(self, building: 'BuildingGroup', amount:int=1):
        if self.cookies < building.multiple_price(amount):
            self.stats()
            building.stats()
            raise Exception("You do not have enough cookies to buy this building")
            
        
        self.cookies -= building.multiple_price(amount)
        self.owned_buildings[building] += amount

    def sell_building(self, building: 'BuildingGroup', amount:int=1 ):
        if self.building_count(building) == 0:
            self.stats()
            building.stats()
            raise Exception("You do not have enough of thi building to sell")
            
        
        self.cookies += building.multiple_price(amount)/4
        self.owned_buildings[building] -= amount

    def building_count(self, building: 'BuildingGroup') -> 'BuildingGroup':
        return self.owned_buildings[building]
    
    @property
    def total_cps(self):
        for building in self.owned_buildings:
            cps += self.building_count(building)*building.cps_per
        return cps

    def stats(self):
        print("\n",self.name)
        for building in self.owned_buildings:
            if self.building_count(building):
                print(building,":", self.building_count(building))
        print("Cookies:", self.cookies)
    
    def upgrade_building(self, building: 'BuildingGroup'):
        if self.cookies < building.upgrades.next_cost:
            self.stats()
            building.stats()
            raise Exception("Not enough cookies to upgrade")
            
        elif building.upgrades.can_upgrade:
            self.stats()
            building.stats()
            raise Exception("There are no more upgrades to buy")
        building.upgrade()

    @property
    def cookies_per_click(self):
        pass
        #TODO

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

    @property
    def cps_per(self) -> int:
        return self.base_cost*(2**self.upgrade_count)

    @property
    def next_cost(self):
        return math.ceil(self.base_cost*(building_cost_multiplyer**self._player.owned_buildings[self]))

    @property
    def next_req(self):
        return self.upgrades.reqs[0] if self.upgrades.reqs else None

    @property
    def next_mult(self) -> int:
        return self.upgrades.mults[0] if self.upgrades.mults else None
    
    @property
    def can_upgrade(self) -> bool:
        if self._player.cookies >= self.upgrades.next_price:
            return True
        else:
            return False

    @property
    def can_buy(self) -> bool:
        if self._player.cookies>=self.next_cost:
            return True
        else:
            return False
    
    def upgrade(self):
        self.upgrades.next()
        self.upgrade_count += 1

    def multiple_price(self, amount:int):
        return math.ceil(self.base_cost*(building_cost_multiplyer**(self._player.owned_buildings[self]+amount)-(building_cost_multiplyer**(self._player.owned_buildings[self]))))

    def stats(self):
        print("\n",self.name)
        print("Base Cost:",self.base_cost)
        print("Upgrade Count:",self.upgrade_count)
        print("Base Cps:",self.base_cps)
        print("Cps Per:", self.cps_per)
        print("Next Cost:", self.next_cost)
        print("Base Upgrade Price:",self.upgrades.base_price)
        print("Next Upgrade Cost Multiplyer:", self.next_mult)
        print("Next Upgrade Req:", self.next_req)
        print("Can Buy:", self.can_buy)
        print("Can Upgrade:", self.can_upgrade)

    def __str__(self):
        return self.name
        
class DefaultBuilding(BuildingGroup):
    def __init__(self, 
        player: Player,
        name: str,
        base_cost: int,
        cps: int,
        base_upgrade_cost_mult: int = 10
        ):
        
        upgrades = PathedUpgrades(name+'Upgrades', base_cost*base_upgrade_cost_mult)
        BuildingGroup.__init__(self, player, name, base_cost, cps, upgrades)

class Cursor(BuildingGroup):
    def __init__(self, 
        player: Player,
        name: str,
        base_cost: int,
        cps: int,
        base_upgrade_cost: int = 100
        ):
        
        upgrades = PathedUpgrades(
        name+'Upgrades',
        base_upgrade_cost,
        [1,1,10,25,50,100,150,200,250,300,350, 400],
        [1, 5, 100, 1000, 100000, 1000000, 10000000, 100000000, 100000000000, 100000000000000, 100000000000000000, 100000000000000000000]
        )
        BuildingGroup.__init__(self, player, name, base_cost, cps, upgrades)
    
    @property
    def cps_per(self):
        upgrades_till_add = 3
        if upgrades_till_add >= self.upgrade_count:
            cps = self.base_cps*(2**self.upgrade_count)
        else:
            cps = self.base_cps*(2**upgrades_till_add)

            total_buildings = 0

            cps_add = 0
            cps_add_constants = (0.1, 0.5, 5, 50, 500, 5000, 50000, 500000, 5000000)
            for i in range(self.upgrade_count-upgrades_till_add):
                cps_add += cps_add_constants[i]
            
            for building in self._player.owned_buildings:
                if building != Cursor:
                    total_buildings += self._player.building_count(building)
            cps += total_buildings*cps_add
        return cps

class PathedUpgrades:
    def __init__(
            self, 
            name,
            base_price: int, 
            reqs = [1,5,25,50,100,150,200,250,300,350,400], 
            mults= [1, 5, 50, 50000, 5000000, 500000000, 500000000000, 500000000000000, 500000000000000000, 500000000000000000000, 5000000000000000000000000]):
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
    
    @property
    def can_upgrade(self):
        if self.reqs:
            return True
        else:
            return False

p = Player('Joe')
p.buy_building(p.grandma, 100)

p.stats()
p.grandma.stats()
p.farm.stats()