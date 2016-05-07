from Men import Men


class Character(Men):
    def __init__(self, name, group, cor, map_f, map_w, skills=(1,1,1), spelllist = (), body=("Body_1.png", "Head_1.png"), gear=(None, None)):
        super().__init__(name, group, cor,  map_f, map_w, skills=skills, spelllist=spelllist, body=body, gear=gear)

    def use_action_points(self, cost):
        self.action_points += cost
        return True