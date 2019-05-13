import sc2
import time

class BuildingPlacement:
    def __init__(self, bot):
        self.bot = bot
    
    async def get_placement_for(self, unittype):
        if self.bot.game.is_command_structure(unittype):
            return self.bot.base_manager.next_base().position
        if self.bot.game.is_gas(unittype):
            return self.get_gas_placement()
        if unittype == sc2.UnitTypeId.PYLON or self.bot.game.unit_type_data()[unittype.value].race != sc2.Race.Protoss:
            for base in self.bot.base_manager.bases:
                if base.has_command_structure_of(sc2.data.Alliance.Self):
                    start = time.time()
                    placement = await self.bot.find_placement(unittype, base.position)
                    print((time.time() - start) * 1000)
                    if placement is not None:
                        return placement
        else: # protoss
            for pylon in self.bot.game.my_units_of_type(sc2.UnitTypeId.PYLON):
                placement = await self.bot.find_placement(unittype, pylon.position)
                if placement is not None:
                    return placement
        
    def get_gas_placement(self):
        for base in self.bot.base_manager.bases:
            if base.has_command_structure_of(sc2.data.Alliance.Self):
                for resource in base.gases:
                    if not self.bot.game.is_gas(resource):
                        return resource
        return None
