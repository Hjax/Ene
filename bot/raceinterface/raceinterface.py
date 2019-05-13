import sc2

class RaceInterface:
    def __init__(self, bot):
        self.bot = bot
    
    async def make(self, unittype):
        creation_ability = self.bot.game.get_production_ability(unittype)
        creation_unit = self.bot.tech_tree.get_unit_with_ability(creation_ability) 
        available_creators = self.bot.units.of_type(creation_unit)

        # if its made by a worker its a structure
        # otherwise its made by a structure

        for unit in available_creators:
            if unit.is_idle or unit.is_collecting:
                if (self.bot.game.is_worker(creation_unit)):
                    self.bot.game.unit_command(unit, creation_ability, await self.bot.building_placement.get_placement_for(unittype))
                else:
                    self.bot.game.unit_command(unit, creation_ability)
    
    async def expand(self):
        await self.make(self.get_race_command_structure())
    
    async def make_worker(self):
        await self.make(self.get_race_worker())

    async def make_gas(self):
        await self.make(self.get_race_gas())
    
    def get_race_command_structure(self):
        if (self.bot.game.race() == sc2.Race.Protoss.value):
            return sc2.UnitTypeId.NEXUS
        elif (self.bot.game.race() == sc2.Race.Terran.value):
            return sc2.UnitTypeId.COMMANDCENTER
        else:
            return sc2.UnitTypeId.HATCHERY

    def get_race_worker(self):
        if (self.bot.game.race() == sc2.Race.Protoss.value):
            return sc2.UnitTypeId.PROBE
        elif (self.bot.game.race() == sc2.Race.Terran.value):
            return sc2.UnitTypeId.SCV
        else:
            return sc2.UnitTypeId.DRONE
    
    def get_race_supply_structure(self):
        if (self.bot.game.race() == sc2.Race.Protoss.value):
            return sc2.UnitTypeId.PYLON
        elif (self.bot.game.race() == sc2.Race.Terran.value):
            return sc2.UnitTypeId.SUPPLYDEPOT
        else:
            return sc2.UnitTypeId.OVERLORD
    
    def get_race_gas(self):
        if (self.bot.game.race() == sc2.Race.Protoss.value):
            return sc2.UnitTypeId.ASSIMILATOR
        elif (self.bot.game.race() == sc2.Race.Terran.value):
            return sc2.UnitTypeId.REFINERY
        else:
            return sc2.UnitTypeId.EXTRACTOR