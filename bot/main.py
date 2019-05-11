import json
from pathlib import Path

from bot.game.game import Game
from bot.techtree.techtree import TechTree
from bot.raceinterface.raceinterface import RaceInterface
from bot.knowledge.scouting import Scouting
from bot.economy.basemanager import BaseManager
from bot.raceinterface.buildingplacement import BuildingPlacement

import sc2

# Bots are created as classes and they need to have on_step method defined.
# Do not change the name of the class!
class MyBot(sc2.BotAI):
    with open(Path(__file__).parent / "../botinfo.json") as f:
        NAME = json.load(f)["name"]
    
    def __init__(self):
        self.game = None
        self.tech_tree = None
        self.scouting = None
        self.race_interface = None
        self.base_manager = None

    async def on_step(self, iteration):
        if (iteration == 0):
            self.game = Game(self)
            self.tech_tree = TechTree(self)
            self.scouting = Scouting(self)
            self.race_interface = RaceInterface(self)
            self.base_manager = BaseManager(self)
            self.building_placement = BuildingPlacement(self)

        self.game.start_step()

        self.scouting.on_step()
        self.base_manager.on_step()

        if (self.game.supply() == self.game.supply_cap()):
            self.race_interface.make(self.race_interface.get_race_supply_structure(self.game.race()))
        elif (self.game.minerals() > 300):
             self.race_interface.expand()
        else:
            self.race_interface.make_worker()

        await self.game.end_step()
