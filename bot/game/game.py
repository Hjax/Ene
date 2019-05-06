import sc2

class Game:
    def __init__(self, bot):
        self.bot = bot
        self.actions = []
    
    def start_frame(self):
        self.actions = []

    def end_frame(self):
        self.bot.do_actions(self.actions)

    def unit_command(self, ability, unit, target=None, queue=False):
        self.actions.append(sc2.unit_command.UnitCommand(ability, unit, target, queue))

    def effects(self):
        return self.bot.effects
    
    