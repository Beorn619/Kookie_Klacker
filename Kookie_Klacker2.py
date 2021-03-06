#Kookie Klacker2
import math, time
from abc import ABC
from strategies import KagazzieAI as ai

building_cost_multiplyer = 1.15
building_sell_multiplyer = 4
upgrades_till_cursor_add = 3
clicks_per_second = 3
total_income_upgrade_base_cost = 1000000


#Zero for no speed limit
updates_per_second = 0

#Zero for no end
ending_tick = 86400

class Player:
    def __init__(self, name: str, ai):

        self.cookies = 0

        self.name = name
        strategy = ai(self)
        self.strategy = strategy

        self.owned_buildings = self.create_BuildingGroups()
        self.grandma_upgrades = self.create_grandma_upgrades()
        self.tick = 0
        self.stop = False

        self.ending_tick = ending_tick
        self.updates_per_second = updates_per_second
        self.clicks_per_second = clicks_per_second

        self.create_income_multiplyer_upgrades()
   
    def create_BuildingGroups(self):
        self.cursor = Cursor(self, 'Cursor', 15, 0.1)
        self.grandma = Grandma(self, 'Grandma', 100.0, 1.0)
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
        
        self.buildings = [
            self.cursor, 
            self.grandma, 
            self.farm, 
            self.mine, 
            self.factory,
            self.bank, 
            self.temple, 
            self.wizard_tower, 
            self.shipment, 
            self.alchemy_lab, 
            self.portal,
            self.time_machine,
            self.antimatter_condenser,
            self.prism,
            self.chance_maker,
            self.fractal_engine,
            ]

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

    def create_grandma_upgrades(self):
        buildings_till_grandma_upgrades = 2
        grandma_upgrades = []
        for i in range(0,len(self.buildings)-buildings_till_grandma_upgrades,1):
            self.buildings[i+buildings_till_grandma_upgrades].grandma_upgrade = GrandmaUpgrades(
                {self.grandma:1,
                self.buildings[i+buildings_till_grandma_upgrades] :15},
                {self.grandma:1,
                self.buildings[i+buildings_till_grandma_upgrades] :0.001/(i+1)},
                self.buildings[i+buildings_till_grandma_upgrades].upgrades.mults[1]*self.buildings[i+buildings_till_grandma_upgrades].upgrades.base_price
            )
            grandma_upgrades.append(self.buildings[i+buildings_till_grandma_upgrades].grandma_upgrade)
        return grandma_upgrades
    
    def create_income_multiplyer_upgrades(self):#TODO
        pass

    @property
    def count_grandma_upgrades(self):
        count = 0
        for building in self.buildings:
            if building.grandma_upgrade:
                if building.grandma_upgrade.bought:
                    count += 1
        return count

    def buy_building(self, building: 'BuildingGroup', amount:int=1):
        if self.cookies < building.multiple_price(amount):
            self.stats()
            building.stats()
            raise Exception("You do not have enough cookies to buy this building.")
            
        self.cookies -= building.multiple_price(amount)
        self.owned_buildings[building] += amount

    def sell_building(self, building: 'BuildingGroup', amount:int=1 ):
        if self.building_count(building) == 0:
            self.stats()
            building.stats()
            raise Exception("You do not have enough of this building to sell.")
            
        
        self.cookies += building.multiple_price(amount)/4
        self.owned_buildings[building] -= amount

    def building_count(self, building: 'BuildingGroup') -> int:
        return self.owned_buildings[building]
    
    @property
    def total_cps(self):
        cps = 0
        for building in self.owned_buildings:
            cps += self.building_count(building)*building.cps_per
        cps += (clicks_per_second*self.cookies_per_click())
        return round(cps, len(str(round(cps)))+1)

    def stats(self):
        print("\n",self.name)
        for building in self.owned_buildings:
            if self.building_count(building):
                print(building,"(",building.upgrade_count,")",":", self.building_count(building))
        print("Cps:",self.total_cps)
        print("Cookies:", math.floor(self.cookies))
        print("Tick:",self.tick)
        print("Grandma Upgrades:",self.count_grandma_upgrades)
    
    def upgrade_building(self, building: 'BuildingGroup'):
        if building.can_upgrade:
            building.upgrade()
        else:
            self.stats()
            building.stats()
            raise Exception("You cannot upgrade this building.")

    def buy_grandma_upgrade(self, building: 'BuildingGroup'):
        if building.can_buy_grandma_upgrade:
            self.cookies -= building.grandma_upgrade.cost
            building.grandma_upgrade.bought = True

    @property
    def cookies_per_click(self) -> int:
        return self.cookies_per_click_mouse
    
    @property
    def non_cursor_buildings(self) -> int:
        total_buildings = 0
        for building in self.owned_buildings:
            if building.name != 'Cursor':
                total_buildings += self.building_count(building)
        return total_buildings

    def cookies_per_click_mouse(self, extra_upgrades=0):
        if upgrades_till_cursor_add >= (self.cursor.upgrade_count+extra_upgrades):
            cps = (2**(self.cursor.upgrade_count+extra_upgrades))
        else:
            cps = (2**upgrades_till_cursor_add)

            total_buildings = self.non_cursor_buildings
            cps_add = self.cookies_per_building(extra_upgrades)
            cps += total_buildings*cps_add
        return cps

    def cookies_per_building(self, extra_upgrades=0) -> float:
        cps_add = 0
        cps_add_constants = (0.1, 0.5, 5, 50, 500, 5000, 50000, 500000, 5000000)
        for i in range(0,(self.cursor.upgrade_count+extra_upgrades)-upgrades_till_cursor_add,1):
            cps_add += cps_add_constants[i]
        return cps_add

    def update(self):
        if self.stop != True:
            self.tick += 1
            self.cookies += self.total_cps
            self.strategy.update()

    def cps_after_grandma_upgrade(self, building: 'BuildingGroup') -> float:
        if building.grandma_upgrade == None:
            self.stats()
            building.stats()
            raise Exception("You do not have any grandma upgrades.")
        elif building.grandma_upgrade.bought == True:
            self.stats()
            building.stats()
            raise Exception("You have already bought that grandma upgrade.")
        building.grandma_upgrade.bought = True
        cps = self.total_cps
        building.grandma_upgrade.bought = False
        return cps


class BuildingGroup(ABC):
    def __init__(self, 
        player: Player,
        name: str,
        base_cost: int,
        cps: int,
        upgrades: 'PathedUpgrades'
        ):
        self.player = player

        self.name = name

        self.base_cost = base_cost


        self.upgrade_count = 0
        self.base_cps = cps

        self.upgrades = upgrades

        self.grandma_upgrade = None

    @property
    def cps_per(self) -> float:
        if self.grandma_upgrade.bought:
            grandma_cps_boost = 1+(self.grandma_upgrade.mults[self]*self.player.owned_buildings[self.player.grandma])
            return self.base_cps*(2**(self.upgrade_count))*(grandma_cps_boost)
        return self.base_cps*(2**(self.upgrade_count))

    def next_cps_per(self, extra_upgrades: int) -> float:
        if self.upgrade_count+extra_upgrades < len(self.upgrades.reqs):
            self.upgrade_count +=extra_upgrades
            cps = self.cps_per
            self.upgrade_count-=extra_upgrades
            return cps
        else:
            self.player.stats()
            self.stats()
            raise Exception("You are trying to estimate the cps with too many upgrades.")
    
    @property
    def next_cost(self) -> int:
        return math.ceil(self.base_cost*(building_cost_multiplyer**self.player.owned_buildings[self]))

    @property
    def can_upgrade(self) -> bool:
        if self.upgrades.reqs == []:
            return False
        elif self.player.cookies <= self.upgrades.next_cost:
            return False
        elif self.upgrades.next_req > self.player.building_count(self):
            return False
        else:
            return True

    @property
    def can_buy(self) -> bool:
        if self.player.cookies>=self.next_cost:
            return True
        else:
            return False
    
    @property
    def can_buy_grandma_upgrade(self) -> bool:
        if self.grandma_upgrade == None:
            return False
        elif self.grandma_upgrade.bought:
            return False
        elif self.player.cookies < self.grandma_upgrade.cost:
            return False
        else:
            return True

    def upgrade(self):
        if self.can_upgrade:
            self.player.cookies -= self.upgrades.next_cost
            self.upgrade_count += 1
        else:
            raise Exception("You cannot upgrade this.")

    def multiple_price(self, amount:int) -> float:
        return math.ceil(self.base_cost*(building_cost_multiplyer**(self.player.owned_buildings[self]+amount)-(building_cost_multiplyer**(self.player.owned_buildings[self])))/(0.15))

    def stats(self):
        print("\n",self.name)
        print("Base Cost:",self.base_cost)
        print("Upgrade Count:",self.upgrade_count)
        print("Base Cps:",self.base_cps)
        print("Cps Per:", self.cps_per)
        print("Next Cost:", self.next_cost)
        print("Base Upgrade Price:",self.upgrades.base_price)
        print("Next Upgrade Cost Multiplyer:", self.upgrades.next_mult)
        print("Next Upgrade Req:", self.upgrades.next_req)
        print("Can Buy:", self.can_buy)
        print("Can Upgrade:", self.can_upgrade)
        if self.grandma_upgrade:
            print("Bought Grandma Upgrade:", self.grandma_upgrade.bought)

    def __repr__(self) -> str:
        return self.name


class DefaultBuilding(BuildingGroup):
    def __init__(self, 
        player: Player,
        name: str,
        base_cost: int,
        cps: int,
        base_upgrade_cost_mult: int = 10
        ):
        
        upgrades = PathedUpgrades(name+'Upgrades',self, base_cost*base_upgrade_cost_mult)
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
        self,
        base_upgrade_cost,
        [1,1,10,25,50,100,150,200,250,300,350, 400],
        [1, 5, 100, 1000, 100000, 1000000, 10000000, 100000000, 100000000000, 100000000000000, 100000000000000000, 100000000000000000000])
        BuildingGroup.__init__(self, player, name, base_cost, cps, upgrades)
    
    @property
    def cps_per(self) -> int:
        if upgrades_till_cursor_add >= (self.upgrade_count):#If upgrades work normally
            cps = self.base_cps*(2**(self.upgrade_count))
        else:#If you need to start add flat amounts
            cps = self.base_cps*(2**upgrades_till_cursor_add)

            total_buildings = self.player.non_cursor_buildings
            cps_add = self.cookies_per_building()
            cps += total_buildings*cps_add
        return cps
    

    def cookies_per_building(self) -> float:
        cps_add = 0
        cps_add_constants = (0.1, 0.5, 5, 50, 500, 5000, 50000, 500000, 5000000)
        for i in range(0,(self.upgrade_count)-upgrades_till_cursor_add,1):
            cps_add += cps_add_constants[i]
        return cps_add


class Grandma(BuildingGroup):
    def __init__(self, 
        player: Player,
        name: str,
        base_cost: int,
        cps: int,
        base_upgrade_cost_mult: int = 10
        ):
        
        upgrades = PathedUpgrades(name+'Upgrades',self, base_cost*base_upgrade_cost_mult)
        BuildingGroup.__init__(self, player, name, base_cost, cps, upgrades)

    @property
    def cps_per(self) -> int:
        return self.base_cps*(2**(self.upgrade_count+self.player.count_grandma_upgrades))


class PathedUpgrades:
    def __init__(
            self, 
            name,
            building,
            base_price: int, 
            reqs = [1,5,25,50,100,150,200,250,300,350,400], 
            mults= [1, 5, 50, 50000, 5000000, 500000000, 500000000000, 500000000000000, 500000000000000000, 500000000000000000000, 5000000000000000000000000]):
        self.name = name
        self.reqs = reqs
        self.mults = mults
        self.base_price = base_price
        self.building = building
    
    @property
    def next_cost(self) -> int:
        return self.base_price*self.next_mult
    
    @property
    def next_req(self) -> int:
        if self.building.upgrade_count <= len(self.reqs):
            return self.reqs[self.building.upgrade_count]
        else:
            return None
    
    @property
    def next_mult(self) -> int:
        if self.building.upgrade_count <= len(self.mults):
            return self.mults[self.building.upgrade_count]
        else:
            return None


class GrandmaUpgrades:
    def __init__(self, reqs, mults, cost):
        self.reqs = reqs
        self.mults = mults
        self.cost = cost
        self.next_cost = cost
        self.bought = False

class IncomeMultiplyerUpgrade:
    def __init__(self, base_cost: int, mult: float, player: Player):
        self.base_cost = base_cost
        self.next_cost = base_cost
        self.mult = mult
        self.bought = False
        self.player = player
    
    @property
    def cps_after_buy(self):
        if self.bought == False:
            return self.player.total_cps*(1+self.mult)
        else:
            self.player.stats()
            raise Exception("You cannot see cps after you buy this because it is already bought.")
    
    @property
    def can_buy(self):
        if self.bought == True:
            return False
        elif self.next_cost > self.player.cookies:
            return False
        else:
            return True



def calling_updates(players):
    for player in players:
        player.update()
        if ending_tick:
            if player.tick >= ending_tick:
                player.stop = True


def is_finished(players):
    stop = True
    for player in players:
        if player.stop != True:
            stop = False
            break
    return stop


def hold(start):
    if ((1/updates_per_second)-(time.time()-start))>0:
        time.sleep((1/updates_per_second)-(time.time()-start))


def main():
    joe = Player('Joe', ai)
    players = [joe]

    
    input("\nPress Enter To Start.")
    while True:
        start = time.time()
        calling_updates(players)
        check_break = is_finished(players)
        if check_break:
            for player in players:
                player.stats()
            break
        if updates_per_second != 0:
            hold(start)

main()
