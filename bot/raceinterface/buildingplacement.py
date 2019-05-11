import sc2

class BuildingPlacement:
    def __init__(self, bot):
        self.bot = bot
    
    def get_placement_for(self, unittype):
        if self.bot.game.is_command_structure(unittype):
            return self.bot.base_manager.next_base()
            
        
