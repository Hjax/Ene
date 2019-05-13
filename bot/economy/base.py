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
    
    def mineral_line_center(self):
        result = sc2.position.Point2([0, 0])
        total = 0
        for resource in self.minerals + self.gases:
            result += resource.position
            total += 1
        if total == 0:
            return result
        self.bot._client.debug_box_out(sc2.position.Point2([result[0] / total, result[1] / total]), sc2.position.Point2([(result[0] / total) + 1, (result[1] / total) + 1]))
        return sc2.position.Point2([result[0] / total, result[1] / total])