import sc2

class RaceInterface:
    def __init__(self, bot):
        self.bot = bot
    
    def make(self, unittype):
        creation_ability = self.bot.game.get_production_ability(unittype)
        creation_unit = self.bot.tech_tree.get_unit_with_ability(creation_ability) 
        available_creators = self.bot.units.of_type(creation_unit)

        # if its made by a worker its a structure
        # otherwise its made by a structure

        for unit in available_creators:
            if unit.is_idle or unit.is_collecting:
                if (self.bot.game.is_worker(creation_unit)):
                    self.bot.game.unit_command(unit, creation_ability, self.bot.building_placement.get_placement_for(unittype))
                else:
                    self.bot.game.unit_command(unit, creation_ability)
    
    def expand(self):
        self.make(self.get_race_command_structure(self.bot.game.race()))
    
    def make_worker(self):
        self.make(self.get_race_worker(self.bot.game.race())) 
    
    def get_free_builder(self):
        workers = self.bot.game.workers()
        for worker in workers:
            if worker.is_idle or worker.is_collecting:
                return worker
    
    def get_race_command_structure(self, race):
        if (race == sc2.Race.Protoss.value):
            return sc2.UnitTypeId.NEXUS
        elif (race == sc2.Race.Terran.value):
            return sc2.UnitTypeId.COMMANDCENTER
        else:
            return sc2.UnitTypeId.HATCHERY

    def get_race_worker(self, race):
        if (race == sc2.Race.Protoss.value):
            return sc2.UnitTypeId.PROBE
        elif (race == sc2.Race.Terran.value):
            return sc2.UnitTypeId.SCV
        else:
            return sc2.UnitTypeId.DRONE
    
    def get_race_supply_structure(self, race):
        if (race == sc2.Race.Protoss.value):
            return sc2.UnitTypeId.PYLON
        elif (race == sc2.Race.Terran.value):
            return sc2.UnitTypeId.SUPPLYDEPOT
        else:
            return sc2.UnitTypeId.OVERLORD

    def build_supply_structure(self):
        pass
    
    def build_worker(self):
        pass

    def can_afford(self, unittype_upgrade_or_ability):
        pass