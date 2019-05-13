import json

class TechTree:
    def __init__(self, bot):
        self.bot = bot
        file_object = open("data.json", "r")
        self.data = json.loads(file_object.read())
        file_object.close()

    def get_ability_data(self, id):
        for item in self.data["Ability"]:
            if item["id"] == id:
                return item
        
    def get_unit_data(self, id):
        for item in self.data["Unit"]:
            if item["id"] == id:
                return item
    
    def get_upgrade_data(self, id):
        for item in self.data["Upgrade"]:
            if item["id"] == id:
                return item
    
    def get_unit_with_ability(self, abilitytype):
        for item in self.data["Unit"]:
            for ability in item["abilities"]:
                if ability["ability"] == abilitytype.value:
                    return self.bot.game.get_unit_by_id(item["id"])
