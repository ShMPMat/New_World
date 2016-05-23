import Render_functions
from pygame import Rect

class Thing():
    def __init__(self, name, spec_n, size, weight, cost, slot):
        self.name = name
        self.icon = Render_functions.load_image(spec_n+"_icon.png", alpha_cannel="True")
        self.size = size
        self.weight = weight
        self.cost = cost
        self.slots = slot

class Equipment(Thing):
    def __init__(self, name, spec_n, size, weight, cost, slot):
        super().__init__(name, spec_n, size, weight, cost, slot)
        img_suff = '.png'
        self.spec_n = spec_n
        self.img = Render_functions.load_image(spec_n+img_suff, alpha_cannel="True")
        self.img_s =  Render_functions.load_image(spec_n+"_s"+img_suff, alpha_cannel="True")

class Example():
    def __init__(self, type):
        self.type = type
        if type.slots:
            self.items = []

    def update_slots(self, thing, cor):
        if thing == self:
            print(23)
            return False
        if cor[0]+thing.size[0] > self.slots[0] or cor[1]+thing.size[1] > self.slots[1]:
            return False
        r = Rect(cor, thing.size)
        for item in self.items:
            if r.collidedict(item[1]):
                return False
        self.items.append((thing, r))
        return True

    def __getattr__(self, item): # fixme! I don't like it...
        if item == "name":
            return self.type.name
        elif item == "icon":
            return self.type.icon
        elif item == "size":
            return self.type.size
        elif item == "weight":
            return self.type.weight
        elif item == "cost":
            return self.type.cost
        elif item == "slots":
            return self.type.slots
        elif item == "spec_n":
            return self.type.spec_n
        elif item == "img":
            return self.type.img
        elif item == "img_s":
            return self.type.img_s