from abc import ABC, abstractmethod
import math, time


class Strategy(ABC):
    @abstractmethod
    def update(self, player):
        raise NotImplementedError()

class KagazzieAI(Strategy):
    def __init__(self, player):
        self.player = player
        self.target = None

    def update(self):
        if self.target == None:
            buildings_time_to_profit, upgrades_time_to_profit = self.times_to_profit()
            self.target = self.choose_target(buildings_time_to_profit, upgrades_time_to_profit)
        if (self.player.tick % 10000) == 0:
            self.player.stats()
        self.target = self.attempt_to_buy(self.target)

    
    def time_to_buy(self, obj):
        time = math.ceil((obj.next_cost-self.player.cookies)/self.player.total_cps)
        return time
    
    def time_to_repay_building(self, building):
        return (building.next_cost)/building.cps_per
    
    def times_to_profit(self):
        buildings_time_to_profit = []
        upgrades_time_to_profit = []
        for building in self.player.owned_buildings.keys():
            buildings_time_to_profit.append(math.ceil(self.time_to_buy(building)+self.time_to_repay_building(building)))
            if building.upgrades.next_req <= self.player.owned_buildings[building]:
                upgrades_time_to_profit.append(self.time_to_buy(building.upgrades)+self.time_to_repay_upgrade(building))
            else:
                upgrades_time_to_profit.append(None)
            
        return buildings_time_to_profit, upgrades_time_to_profit
    
    def time_to_repay_upgrade(self, building):
        return int(math.ceil((building.upgrades.next_cost)/((building.cps_per_after_upgrade()-building.cps_per)*self.player.owned_buildings[building])))
    
    def choose_target(self, buildings_time_to_profit, upgrades_time_to_profit):
        target_time = buildings_time_to_profit[0]
        target = [self.player.buildings[0],'building']
        for i in range(0,len(self.player.buildings)):
            if buildings_time_to_profit[i] < target_time:
                target = [self.player.buildings[i], 'building']
                target_time = buildings_time_to_profit[i]
            if upgrades_time_to_profit[i]:
                if upgrades_time_to_profit[i] < target_time:
                    target = [self.player.buildings[i], 'upgrade']
                    target_time = buildings_time_to_profit[i]
        return target

    def attempt_to_buy(self, target):
        obj = target[0]
        t = target[1]

        if t == 'building':
            if obj.can_buy:
                self.player.buy_building(self.target[0])
                return None
        else:
            if obj.can_upgrade:
                self.player.upgrade_building(self.target[0])
                return None
        return target