from Men import Men
from findPathLee import findPath
from Groups import relations_list


class NPC(Men):
    def __init__(self, name, group, cor, map_f, map_w, time, skills=(1, 1, 1), spelllist = (), body=("Body_1.png", "Head_1.png"), gear=(None, None)):
        super().__init__(name, group, cor, map_f, map_w, time, skills=skills, spelllist=spelllist, body=body, gear=gear)
        self.alarm = []

    def update(self, map_f, map_w, viev_objects, all_persons):
        if self.dead:
            return
        if not self.cur_anim:
            self.AI(viev_objects, map_f, map_w)
        super().update(all_persons)

    def AI(self, viev_objects, map_f, map_w):
        """
                Интеллект NPC. Он может:
                    1.
        """
        self.others_actions = []
        for object in viev_objects:
            if self.get_relations(object) < 0:
                if not object.dead:
                    if not object in self.alarm:
                        self.alarm.append(object)
                elif object in self.alarm:
                    self.alarm.remove(object)
                if not self.path:
                    self.set_path(findPath(map_f, map_w, self.cor, object.cor))
        for object in self.alarm:
            if self.attack_field.collidepoint(object.cor[0], object.cor[1]):
                self.path = None
                self.set_target(object)

    def get_relations(self, object):
        if object == self or object.dead:
            return 0
        relation = relations_list[self.group.ID][object.group.ID]
        try:
            for action, value in self.relations[object]:
                relation += value
        except: pass
        return relation

    def kill_self(self):
        super().kill_self()
        self.alarm = []