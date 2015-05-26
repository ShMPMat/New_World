import Render_functions

class Thing():
    def __init__(self, name, icon, weight, cost):
        self.name = name
        self.icon = Render_functions.load_image(icon, alpha_cannel="True")
        self.weight = weight
        self.cost = cost

class Equipment(Thing):
    def __init__(self, name, icon, weight, cost, img, img_s):
        super().__init__(name, icon, weight, cost)
        self.img = Render_functions.load_image(img, alpha_cannel="True")
        self.img_str = img
        self.img_s = img_s