from Men import Men


class Character(Men):
    def __init__(self, name, group, cor, map_f, map_w, time, skills=(1,1,1), spelllist = (), body=("Body_1.png", "Head_1.png"), gear=(None, None)):
        super().__init__(name, group, cor,  map_f, map_w, time, skills=skills, spelllist=spelllist, body=body, gear=gear)