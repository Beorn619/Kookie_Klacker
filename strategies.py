from abc import ABC, abstractmethod
import math, operator


class Strategy(ABC):
    @abstractmethod
    def update(self, player):
        raise NotImplementedError()

class KagazzieAI(Strategy):
    def __init__(self, player):
        self.player = player
        self.target = None
        self.target_type = None

    def update(self):

        if self.target == None:
            self.target, self.target_type = self.choose_target()

        self.attempt_buy()

        if self.player.tick % 500 == 0:
            self.player.stats()
            
    
    def time_to_buy(self, obj):
        time = math.ceil((obj.next_cost-self.player.cookies)/self.player.total_cps)
        return time
    
    def building_roi(self, obj):
        return obj.next_cost/obj.cps_per
    
    def upgrade_roi(self, obj):
        if obj.name != 'Cursor':
            return (obj.next_cps_per(1) - obj.cps_per)/obj.upgrades.next_cost
        else:
            return ((obj.next_cps_per(1) +  (self.player.cookies_per_click_mouse(1)*self.player.clicks_per_second)) - (obj.cps_per+(self.player.cookies_per_click_mouse()*self.player.clicks_per_second)))/obj.upgrades.next_cost
    
    def grandma_upgrade_roi(self, obj):
        pass
    
    def income_upgrade_roi(self, obj):
        pass

    def choose_target(self):
        building_times = []
        upgrade_times = []
        #grandma_upgrade_times = []
        #income_upgrade_times = []

        purchases = [building_times, upgrade_times]

        for building in self.player.buildings:
            building_times.append([math.ceil(self.time_to_buy(building)+self.building_roi(building)), building, 'Building'])
            if building.upgrades.next_req <= self.player.owned_buildings[building]:
                upgrade_times.append([math.ceil(self.time_to_buy(building.upgrades)+self.upgrade_roi(building)), building, 'Upgrade'])
            else:
                pass#Make this calculate ROI on the Quickest path to upgrade TODO
        for group in purchases:
            group.sort(key=lambda tup: tup[0])
        
        target = purchases[0][0][1]
        target_time = purchases[0][0][0]
        target_type = purchases[0][0][2]
        for group in purchases:
            if len(group) == 0:
                continue
            elif group[0][0] < target_time:
                target = group[0][1]
                target_time = group[0][0]
                target_type = group[0][2]
        return target, target_type

    def attempt_buy(self):
        if self.target_type == 'Building':
            if self.target.can_buy == True:
                self.player.buy_building(self.target)
                self.target = None
                self.target_type = None
        
        elif self.target_type == 'Upgrade':
            if self.target.can_upgrade:
                self.player.upgrade_building(self.target)
                self.target = None
                self.target_type = None