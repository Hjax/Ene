import sc2

from bot.economy.base import Base

class BaseManager:
    def __init__(self, bot):
        self.bot = bot
        self.bases = [Base(self.bot, location) for location in self.bot.expansion_locations.keys()]
    
        # TODO calculate pathing distances between bases
        # TODO create start of game functions to clear rallies

    def on_step(self):
        for structure in self.bot.game.units():
            if self.bot.game.is_command_structure(structure.type_id):
                for base in self.bases:
                    if base.position.distance_to(structure.position) < 5:
                        base.set_command_structure(structure)
        for base in self.bases:
            base.update()
        
    def main_base(self):
        best = None 
        for base in self.bases:
            if base.has_command_structure_of(sc2.data.Alliance.Self):
                if best == None or best.position.distance_to(self.bot.scouting.closest_enemy_spawn_to(best.position)) < base.position.distance_to(self.bot.scouting.closest_enemy_spawn_to(base.position)):
                    best = base 
        return best
    
    def next_base(self):
        best = None 
        best_dist = 9999
        for base in self.bases:
            if not base.has_command_structure():
                if best is None or self.main_base().position.distance_to(base.position) - base.position.distance_to(self.bot.scouting.closest_enemy_spawn()) < best_dist:
                    best_dist = self.main_base().position.distance_to(base.position) - base.position.distance_to(self.bot.scouting.closest_enemy_spawn()) < best_dist
                    best = base
        return best

