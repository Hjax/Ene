import json
from pathlib import Path

from bot.game.game import Game
from bot.techtree.techtree import TechTree
from bot.raceinterface.raceinterface import RaceInterface

import sc2

# Bots are created as classes and they need to have on_step method defined.
# Do not change the name of the class!
class MyBot(sc2.BotAI):
    with open(Path(__file__).parent / "../botinfo.json") as f:
        NAME = json.load(f)["name"]

    def __init__(self):
        self.game = Game(self)
        self.tech_tree = TechTree(self)
        self.race_interface = RaceInterface(self)

    async def on_step(self, iteration):
        self.game.start_frame()

        if (self.workers.amount < 15):
            self.race_interface.make(self.game.get_race_worker(self.game.race())) 

        await self.game.end_frame()
