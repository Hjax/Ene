import sc2
from bot.constants import Constants

class Game:
    def __init__(self, bot):
        self.bot = bot
        self.actions = []
        self.messages = []
        self.spending = [0, 0]
    
    async def start_frame(self):
        self.actions = []
        self.spending = [0, 0]

    async def end_frame(self):
        self.bot.do_actions(self.actions)
        for message in self.messages:
            await self.bot.chat_send(message)
    
    def unit_type_data(self):
        return self.bot._game_data.units
    
    def upgrade_data(self):
        return self.bot._game_data.upgrades
    
    def ability_data(self):
        return self.bot._game_data.abilities

    def unit_command(self, unit, ability, target=None, queue=False):
        self.actions.append(sc2.unit_command.UnitCommand(ability, unit, target, queue))

    # TODO precompute this
    def get_production_ability(self, unittype):
        for unitdatakey in self.unit_type_data().keys():
            if unittype.value == unitdatakey:
                return self.unit_type_data()[unitdatakey].creation_ability
        return None

    def effects(self):
        return self.bot.state.effects
    
    def has_upgrade(self, upgrade) -> bool:
        return upgrade in self.bot.state.upgrades

    def on_creep(self, point: sc2.position.Point2) -> bool:
        return self.bot.has_creep(point)

    def units(self) -> sc2.units.Units:
        return self.bot.state.units

    def get_unit(self, tag) -> sc2.unit.Unit:
        return self.units().by_tag(tag)

    def chat(self, message):
        if (Constants.CHAT):
            self.messages.append(message)

    def visible(self, point) -> bool:
        return self.bot.is_visible(point)

    def game_time(self):
        self.bot.time()
    
    def frame(self):
        return self.bot.state.game_loop

    async def check_placement(self, building, position):
        return await self.bot.can_place(building, position)

    def supply(self):
        return self.bot.supply_used
    
    def supply_cap(self):
        return self.bot.supply_cap

    def minerals(self):
        return self.bot.minerals - self.spending[0]

    def vespene(self):
        return self.bot.vespene - self.spending[1]

    def spend(self, minerals, vespene):
        self.spending = [self.spending[0] + minerals, self.spending[1] + vespene]

    def cost(self, ability):
        return self.bot._game_data.calcuate_ability_cost(ability)

    def purchase(self, upgradeOrUnit):
        self.spend(self.cost(upgradeOrUnit).minerals, self.cost(upgradeOrUnit).vespene)

    def can_afford(self, upgradeOrUnit):
        return self.minerals() > self.cost(upgradeOrUnit).minerals and self.vespene() > self.cost(upgradeOrUnit).vespene

    def height(self, point):
        return self.bot.state.terrain_height[point]

    def buildable(self, point):
        return self.bot.state.placement_grid[point] != 0
    
    def pathable(self, point):
        return self.bot.state.pathing_grid[point] != 0
    
    def is_command_structure(self, unittype):
        return unittype in [sc2.UnitTypeId.NEXUS, sc2.UnitTypeId.COMMANDCENTER, sc2.UnitTypeId.COMMANDCENTERFLYING, sc2.UnitTypeId.ORBITALCOMMAND, sc2.UnitTypeId.ORBITALCOMMANDFLYING, sc2.UnitTypeId.PLANETARYFORTRESS, sc2.UnitTypeId.HATCHERY, sc2.UnitTypeId.LAIR, sc2.UnitTypeId.HIVE]

    def is_worker(self, unittype):
        return unittype in [sc2.UnitTypeId.DRONE, sc2.UnitTypeId.SCV, sc2.UnitTypeId.PROBE]

    def resources_killed(self):
        return [self.bot.state.score.killed_minerals_army + self.bot.state.score.killed_minerals_economy, self.bot.state.score.killed_vespene_army + self.bot.state.score.killed_vespene_economy]