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
        else:
            self.attackfield_update()
            self.AI(viev_objects, map_f, map_w)
            super().update(dt, all_persons)
            if self.stepwise_mod and self.action_points - self.coofs['stepwise_move'] < 0 and not self.anim_play:
                self.finish = True

    def AI(self, viev_objects, map_f, map_w):
        """
                Интеллект NPC. Он может:
                    1.
        """
        for object in viev_objects:
            if relations_list[self.group.ID][object.group.ID] < 0 and object != self and not object.dead:
                if not object in self.alarm:
                    self.alarm.append(object)
                if not self.path:
                    self.set_path(findPath(map_f, map_w, self.cor, object.cor))
                    if self.path != -1:
                        self.path = self.path[:-1]
            else:
                if not self.path and not self.anim_play:
                    self.finish = True
            if self.attack_field.collidepoint(object.cor[0], object.cor[1]):
                self.path = None
                if self.alarm:
                    self.set_target(object)

    def hurt(self, damage):
        super().hurt(damage)

    def kill_men(self):
        super().kill_men()
        self.finish = True
        self.alarm = []

    def use_action_points(self, cost):
        """
                Отнять cost очков действий, если при этом их кол-во не станет меньше нуля
        """
        if self.action_points >= cost:
            self.action_points -= cost
            return True
        else:
            self.finish = True
            return False