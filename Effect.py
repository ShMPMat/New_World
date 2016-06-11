
class Effect():
    def __init__(self, type, target, value, start, time, range):
        if type == "hurt":
            self.type = target.hurt
        elif type == "armor":
            self.type = target.update_armor
        elif type == "health":
            self.type = target.update_max_health
        elif type == "heal":
            self.type = target.heal
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
            elif time.get_delta_time(self.start[0], self.start[1], self.start[2]) >= self.time:
                self.type(-self.value)
                return True
        else:
            pass
