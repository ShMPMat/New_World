import Render_functions

class Thing():
    def __init__(self, name, icon, size, weight, cost, slot):
        self.name = name
        self.icon = Render_functions.load_image(icon, alpha_cannel="True")
        self.size = size
        self.weight = weight
        self.cost = cost

class Equipment(Thing):
    def __init__(self, name, icon, size, weight, cost, slot, img, img_s):
        super().__init__(name, icon, size, weight, cost, slot)
        self.img = Render_functions.load_image(img, alpha_cannel="True")
        self.img_str = img
        self.img_s =  Render_functions.load_image(img_s, alpha_cannel="True")