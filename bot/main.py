import json
from pathlib import Path

from bot.game.game import Game
from bot.game.gameinfocache import GameInfoCache

import sc2

# Bots are created as classes and they need to have on_step method defined.
# Do not change the name of the class!
class MyBot(sc2.BotAI):
    with open(Path(__file__).parent / "../botinfo.json") as f:
        NAME = json.load(f)["name"]

    def __init__(self):
        self.Game = Game(self)
        self.GameInfoCache = GameInfoCache(self)

    async def on_step(self, iteration):
        await self.Game.start_frame()
        self.GameInfoCache.on_frame();
        if (self.GameInfoCache.production.get(sc2.AbilityId.PROTOSSBUILD_NEXUS, 0) > 0):
            print("woooooooo")
        await self.Game.end_frame();
