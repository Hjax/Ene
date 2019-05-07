import sc2

class RaceInterface:
    def __init__(self, bot):
        self.bot = bot
    
    def make(self, unittype):
        creation_ability = self.bot.game.get_production_ability(unittype)
        creation_unit = self.bot.tech_tree.get_unit_with_ability(creation_ability) 
        available_creators = self.bot.units.of_type(creation_unit)

        # if its made by a worker its a structure
        # otherwise its made by a structure

        for unit in available_creators:
            if unit.is_idle or unit.is_collecting:
                if (self.bot.game.is_worker(creation_unit)):
                    pass
                else:
                    self.bot.game.unit_command(unit, creation_ability)
    
    