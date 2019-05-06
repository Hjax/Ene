import json
from pathlib import Path

from game.game import Game

import sc2

# Bots are created as classes and they need to have on_step method defined.
# Do not change the name of the class!
class MyBot(sc2.BotAI):
    with open(Path(__file__).parent / "../botinfo.json") as f:
        NAME = json.load(f)["name"]

    def __init__(self):
        self.Game = Game(self)

    async def on_step(self, iteration):
        pass
