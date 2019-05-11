import sc2

class Base:
    def __init__(self, bot, position):
        self.position = position
        self.command_structure = None
        self.bot = bot
        self.minerals = []
        self.gases = []

    def update(self):
        # TODO figure out if this does anything
        self.minerals = [x for x in self.bot.expansion_locations[self.position] if x.is_mineral_field]
        self.gases = [x for x in self.bot.expansion_locations[self.position] if x.is_vespene_geyser]

    def set_command_structure(self, unit):
        self.command_structure = unit
    
    def has_command_structure_of(self, alliance):
        result = self.command_structure is not None and self.command_structure.alliance == alliance.value
        return result
    
    def has_command_structure(self):
        return self.command_structure is not None
    