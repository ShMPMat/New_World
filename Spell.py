from Whizbang import Whizbang
from Effect import Effect

class Spell():
    def __init__(self, name, type, manna_cost, ap_cost, distance, time, effect=None):
        self.name = name
        self.manna = manna_cost
        self.action_points = ap_cost
        self.distance = distance
        self.time = time
        self.type = type
        if self.type == "Attacking":
            self.whizbang = effect[-1]
            self.effects = effect[:-1]
        else:
            self.effects = effect

    def apply(self, exorcist, target, cor, lst, start_time):
        if exorcist.manna - self.manna < 0:
            return
        exorcist.manna -= self.manna
        if self.type == "Attacking":
            lst.append(Whizbang(cor, target.cor, self.whizbang))
        for type, value, range in self.effects:
            target.effects.append(Effect(type, target, value, start_time, self.time, range))


fireball = Spell("Огненный шар", "Attacking", 1, 4, 4, 1, effect=(("hurt", 3, "instant"), "Flying_fireball.png"))
improve_aah = Spell("Божественная помощь!", "Defence", 1, 4, 4, 20, effect=(("armor", 1, "cont"), ("health", 30, "cont")))