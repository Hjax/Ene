import json

class TechTree:
    def __init__(self):
        self.data = json.loads(open("data.json", "r").read())

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
    
    def get_unit_with_ability(self, ability_id):
        for item in self.data["Unit"]:
            for ability in item["abilities"]:
                if ability["ability"] == ability_id:
                    return item["id"]
