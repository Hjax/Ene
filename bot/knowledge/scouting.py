import sc2

class Scouting:
    def __init__(self, bot):
        self.bot = bot
        self.spawns = []
    
    def on_step(self):
        if len(self.spawns) == 0:
            self.spawns = self.bot.game.enemy_spawn_locations()

        if len(self.spawns) > 1:
            for structure in self.bot.game.known_enemy_structures():
                self.spawns = [self.closest_enemy_spawn_to(structure.location)]

        # TODO add worker scouting
    
    def closest_enemy_spawn_to(self, location):
        best = None
        for point in self.spawns:
            if best is None or point.distance_to(location) < best.distance_to(location):
                best = point
        return best 
    
    def closest_enemy_spawn(self):
        return self.closest_enemy_spawn_to(self.bot.game.start_location())