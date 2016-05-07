from Men import Men
from findPathLee import findPath
from Groups import relations_list


class NPC(Men):
    def __init__(self, name, group, cor, map_f, map_w, vision=3, skills=(1, 1, 1), spelllist = (), body=("Body_1.png", "Head_1.png"), gear=("White_doc_robe.png", None)):
        super().__init__(name, group, cor, map_f, map_w, skills=skills, spelllist=spelllist, body=body, gear=gear)
        self.alarm = []
        self.finish = False

    def update(self, dt, map_f, map_w, viev_objects, all_persons):
        if self.dead:
            self.finish = True
            return
        self.finish = False
        self.AI(viev_objects, map_f, map_w)
        super().update(dt, all_persons)

    def AI(self, viev_objects, map_f, map_w):
        """
                Интеллект NPC. Он может:
                    1.
        """
        for object in viev_objects:
            if relations_list[self.group.ID][object.group.ID] < 0 and object != self and not object.dead:
                if not object.dead:
                    if not object in self.alarm:
                        if not self.alarm:
                            self.action_points = 0
                        self.alarm.append(object)
                elif object in self.alarm:
                    self.alarm.remove(object)
                if not self.path:
                    self.set_path(findPath(map_f, map_w, self.cor, object.cor))
            elif not self.anim_play:
                self.finish = True
        for object in self.alarm:
            if self.attack_field.collidepoint(object.cor[0], object.cor[1]):
                self.path = None
                self.set_target(object)

    def kill_men(self):
        super().kill_men()
        self.finish = True
        self.alarm = []

    def use_action_points(self, cost):
        """
                Отнять cost очков действий, если при этом их кол-во не станет меньше нуля
        """
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
        if self.action_points >= cost:
            # print("11111111111111")
            self.action_points -= cost
            return True
        else:
            if not self.anim_play:
                self.finish = True
            return False