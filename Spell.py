from Whizbang import Whizbang

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
        start_time = list(start_time)
        start_time[0]+=self.action_points
        start_time = tuple(start_time)
        if self.type == "Attacking":
            lst.append(Whizbang(cor, target.cor, self.whizbang))
        for type, value, range in self.effects:
            if type == "hurt":
                target.effects.append(Effect(target.hurt, value, start_time, self.time, range))
            elif type == "armor":
                target.effects.append(Effect(target.update_armor, value, start_time, self.time, range))
            elif type == "health":
                target.effects.append(Effect(target.update_max_health, value, start_time, self.time, range))

class Effect():
    def __init__(self, type, value, start, time, range):
        self.type = type
        self.value = value
        self.start = start
        self.time = time
        self.range = range
        self.sw = True

    def update(self, time):
        if self.range == "instant":
            self.type(self.value)
            return True
        elif self.range == "cont":
            if self.sw:
                self.type(self.value)
                self.sw = False
            elif time.get_delta_time(self.start[0], self.start[1]) >= self.time:
                self.type(-self.value)
                return True
        else:
            pass


fireball = Spell("Огненный шар", "Attacking", 1, 4, 4, 1, effect=(("hurt", 3, "instant"), "Flying_fireball.png"))
improve_aah = Spell("Божественная помощь!", "Defence", 1, 4, 4, 20, effect=(("armor", 1, "cont"), ("health", 30, "cont")))