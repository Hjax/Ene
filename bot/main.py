import json, time
from pathlib import Path

from bot.game.game import Game
from bot.game.gameinfocache import GameInfoCache
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
        self.game_info_cache = None

    async def on_step(self, iteration):
        if (iteration == 0):
            self.game = Game(self)
            self.tech_tree = TechTree(self)
            self.scouting = Scouting(self)
            self.race_interface = RaceInterface(self)
            self.base_manager = BaseManager(self)
            self.building_placement = BuildingPlacement(self)
            self.game_info_cache = GameInfoCache(self)

        self.game.start_step()
        start = time.time()
        self.game_info_cache.on_step()
        print((time.time() - start) * 1000)

        self.scouting.on_step()
        self.base_manager.on_step()

        if (self.game.supply() == self.game.supply_cap() and self.game.minerals() > 100):
            await self.race_interface.make(self.race_interface.get_race_supply_structure())
        elif (self.game.minerals() > 400):
             await self.race_interface.expand()
        else:
            await self.race_interface.make_worker()

        await self.game.end_step()


def main():
    with open("botinfo.json") as f:
        info = json.load(f)

    race = sc2.Race[info["race"]]

    sc2.run_game(sc2.maps.get("Abyssal Reef LE"), [
        sc2.player.Bot(race, MyBot()),
        sc2.player.Computer(sc2.Race.Random, sc2.Difficulty.Medium)
    ], realtime=False, step_time_limit=120.0, game_time_limit=(60*20), save_replay_as="test.SC2Replay")

if __name__ == '__main__':
    main()