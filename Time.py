
class Time():
    def __init__(self):
        self.dt = None
        self.minutes = 0
        self.second = 0
        self.miliseconds = 0

    def update(self, dt):
        self.dt = dt
        self.miliseconds += dt
        self.second += self.miliseconds//1000
        self.miliseconds %= 1000
        self.minutes += self.second//60
        self.second %= 60

    def get_delta_time(self, seconds, minutes):
        return (self.minutes-minutes)*60 + self.second-seconds

    def get_time(self):
        return self.second, self.minutes