import sc2

class GameInfoCache:
    def __init__(self, bot):
        self.bot = bot

        self.all_units = {}
        self.current_units = {}

        self.production = {}
        self.counts_friendly = {}
        self.counts_enemy = {}

        self.visible_friendly = {}
        self.visible_enemy = {}
        self.visible_neutral = {}

        self.workers_building = set()
        self.claimed_gases = set()
    
    def on_step(self):
        self.production = {}
        self.counts_friendly = {}
        self.counts_enemy = {}

        self.current_units = {}

        self.visible_friendly = {}
        self.visible_enemy = {}
        self.visible_neutral = {}

        self.workers_building = set()
        self.claimed_gases = set()

        for unit in self.bot.game.units():
            self.all_units[unit.tag] = unit
            self.current_units[unit.tag] = unit

            if (unit.alliance == sc2.data.Alliance.Self.value):
                if (unit.is_ready):
                    self.counts_friendly[unit.type_id] = self.counts_friendly.get(unit.type_id, 0) + 1
                else:
                    thing = self.bot.game.get_production_ability(unit.type_id)
                    self.production[self.bot.game.get_production_ability(unit.type_id)] = self.production.get(self.bot.game.get_production_ability(unit.type_id), 0) + 1
                self.visible_friendly[unit.tag] = unit
                if unit.type_id in self.visible_friendly:
                    self.visible_friendly[unit.type_id].append(unit)
                else:
                    self.visible_friendly[unit.type_id] = [unit]
                for order in unit.orders:
                    self.production[order.ability.id] = self.production.get(order.ability.id, 0) + 1
                    if (self.bot.game.is_worker(unit.type_id)):
                        if order.ability.id == sc2.AbilityId.ZERGBUILD_EXTRACTOR or order.ability.id == sc2.AbilityId.PROTOSSBUILD_ASSIMILATOR or order.ability.id == sc2.AbilityId.TERRANBUILD_REFINERY:
                            self.claimed_gases.add(order.target.tag)
                        if (order.ability.id != sc2.AbilityId.HARVEST_GATHER and order.ability.id != sc2.AbilityId.HARVEST_RETURN):
                            for unitdata in self.bot.game.unit_type_data().values():
                                if order.ability.id == unitdata.creation_ability:
                                    self.workers_building.add(unit.tag)
                                    break

            elif (unit.alliance == sc2.data.Alliance.Enemy.value):
                self.counts_enemy[unit.type_id] = self.counts_enemy.get(unit.type_id, 0) + 1
                if unit.type_id in self.visible_enemy:
                    self.visible_enemy[unit.type_id].append(unit)
                else:
                    self.visible_enemy[unit.type_id] = [unit]
                
            else:
                if unit.type_id in self.visible_neutral:
                    self.visible_neutral[unit.type_id].append(unit)
                else:
                    self.visible_neutral[unit.type_id] = [unit]