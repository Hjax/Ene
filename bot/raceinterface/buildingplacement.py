import sc2
import time
import random

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
                    placement = await self.find_placement_avoiding(unittype, base.position, base.mineral_line_center())
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

    # an adjusted find_placement method that avoids mineral lines
    async def find_placement_avoiding(self, building, near, avoid, max_distance=20, placement_step: int=2):
        """Finds a placement location for building."""


        if isinstance(building, sc2.UnitTypeId):
            building = self.bot._game_data.units[building.value].creation_ability
        else:  # AbilityId
            building = self.bot._game_data.abilities[building.value]

        for distance in range(placement_step, max_distance, placement_step):
            possible_positions = [sc2.position.Point2(p).offset(near).to2 for p in (
                    [(dx, -distance) for dx in range(-distance, distance + 1, placement_step)] +
                    [(dx, distance) for dx in range(-distance, distance + 1, placement_step)] +
                    [(-distance, dy) for dy in range(-distance, distance + 1, placement_step)] +
                    [(distance, dy) for dy in range(-distance, distance + 1, placement_step)]
            )]
            possible_positions = [x for x in possible_positions if avoid.distance_to(x) > 10]
            res = await self.bot._client.query_building_placement(building, possible_positions)
            possible = [p for r, p in zip(res, possible_positions) if r == sc2.ActionResult.Success]
            if not possible:
                continue

            return random.choice(possible)
        return None
