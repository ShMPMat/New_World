import pygame
import random
import Render_functions
from coefficients import *
from Spell import Spell
from math import copysign, fabs, sqrt, acos
from Effect import Effect

class Men():
    def __init__(self, name, group, cor, map_f, map_w, time, attack=1, skills=(1, 1, 1), spelllist = (), body=("Body_1.png", "Head_1.png"), gear=(None, None)):
        # Основные параметры персонажа
        self.name = name                        # Имя
        self.group = group                      # Принадлежность к группе
        self.cor = cor                          # Координаты
        self.speed = 10                         # Скорость передвижения
        self.body = {                           # Изображения частей тела персонажей по умолчанию
            "head": Render_functions.load_image(body[1], alpha_cannel="True"),                  # Голова
            "body": Render_functions.load_image(body[0], alpha_cannel="True"),                  # Тело
        }
        self.gear = {"Outerwear": None,                             # Верхняя одежда
                     "Hands": None,                                # Оружие
                     "Left_shoulder": None,
                     "Right_shoulder": None
                     }
        if gear[0]:
            self.gear["Outerwear"] = gear[0]
        if gear[1]:
            self.gear["Hands"] = gear[1]
        self.skills = {                         # Навыки
            "magic":    skills[0],                                                     # Магия
            "strength": skills[1],                                                     # Сила
            "shooting": skills[2]                                                      # Стрельба
        }
        self.relations = {}
        self.animations = {}
        self.dialogue = None
        self.animations_update(body, gear)
        self.spells = spelllist                         # Заклинания
        self.effects = []                               # Эффекты, наложеные на персонажа
        self.max_health = self.skills["strength"]*10     # Максимальные очки здоровья
        self.health = self.skills["strength"]*10         # Текущие очки здоровья
        self.max_manna = self.skills["magic"]*10        # Максимальные очки манны
        self.manna = self.skills["magic"]*10            # Текущие очки манны
        self.armor = 0                                  # Показатель брони
        self.dead = False                               # Мертв ли персонаж
    # Технические заморочки
        self.coofs = {                          # Коэффициенты (стоимость движения)
            "b_punch": HAND_TO_HAND,                                 # Удар в рукопашную
            "b_inv_use": INV_USE,
            "move": MOVE,                                                 # Движение на клетку
            "rotate": ROTATE,
            False: 100000
        }
        self.time = time
        self.path = ()                          # Путь, по которому идет персонаж
        self.rotate = 0                         # Угол, на который повернут персонаж
        self.move_progress = [0, 0]             # Помогает отобразить процесс перехода с одной клетки на другую
        self.anim_speed = None                  # Скорость смены кадров в миллисекундах
        self.cur_anim = None                    # Код совершаемого действия
        self.worktime = 0                       # Время последней смены кадра
        self.anim_play(False)
        self.anim_stage = 0                     # Кадр анимации
        self.ren_img = None                     # Картинка, которая отображается на экране
        self.ren_img = self.img_designer()      # Начальное обновление картинки
        self.stepwise_mod = False               # Включает/Выключает пошаговый режим
        self.last_stop = None                   # Место, где персонажа в последний раз остановили методом stop
        self.attack_distance = attack           # Дальность, на которой можно атаковать (1 клетка по умолчанию)
        self.attackfield_update()               # Область атаки в виде Rect'а
        self.target = None                      # Цель атаки
        self.whizbangs = []
        self.angle = 0
        self.step = None
        self.vision_length = 10
        self.vision_field = None
        self.map_f = map_f
        self.map_w = map_w
        self.update_visionfield()

    def update(self, all_persons):
        for effect in self.effects:
            if effect.update(self.time):
                self.effects.remove(effect)
        if self.dead:
            return
        if self.path:
            if not self.step:
                if self.look_direction(self.path[0]): # fixme! ЗАСТРЕВАНИЕ ПРИ КЛИКЕ НА СЕБЯ!!!!!!!!!1
                    self.step = self.path[0]
                    self.path = self.path[1:]
                    for per in all_persons:
                        if  per.dead or per == self:
                            continue
                        if self.step == per.step:
                            if self.skills["strength"] > per.skills["strength"]:
                                per.stop()
                            else:
                                self.stop()
                            break
                        elif self.step == per.cor:
                            self.stop()
        elif self.target:
            self.attackfield_update()
            self.hit(self.time)
        if self.step:
            self.anim_play("move")
        self.worktime += self.time.dt
        if self.worktime/1000 >= self.anim_speed:
            self.worktime -= self.anim_speed*1000
            self.ren_img = self.img_designer()
        for w in self.whizbangs:
            w.update()
            if w.end:
                self.whizbangs.remove(w)

    def update_visionfield(self):
        def app(lst, tile):
            if tile not in lst:
                lst.append(tile)
        past_list = []
        sub = []
        unseen = []
        vision_list = []
        unseen_list = []
        actual_list = [self.cor]
        for _ in range(self.vision_length):
            if unseen_list:
                for x, y in unseen_list:
                    try:
                        if fabs((self.cor[0]-x)/(self.cor[1]-y)) >= 1:
                            unseen.append((x+int(copysign(1, y-self.cor[0])), y))
                            unseen.append((y+int(copysign(1, y-self.cor[0])), y+int(copysign(1, y-self.cor[1]))))
                        if fabs((self.cor[1]-y)/(self.cor[0]-x)) >= 1:
                            unseen.append((x, y+int(copysign(1, y-self.cor[1]))))
                            unseen.append((x+int(copysign(1, x-self.cor[0])), y+int(copysign(1, y-self.cor[1]))))
                    except:
                        if self.cor[0]==x:
                            unseen.append((x-1, y+int(copysign(1, x-self.cor[0]))))
                            unseen.append((x+1, y+int(copysign(1, x-self.cor[0]))))
                        else:
                            unseen.append((x+int(copysign(1, y-self.cor[1])), y-1))
                            unseen.append((x+int(copysign(1, y-self.cor[1])), y+1))
                    unseen_list.remove((x, y))
            if unseen:
                for tile in unseen:
                    app(unseen_list, tile)
            for x, y in actual_list:
                if not (x, y):
                    app(unseen_list, (x, y))
                elif self.cor[0] - x > 0 and self.map_w[y][x][3]:
                    app(unseen_list, (x, y))
                elif self.cor[0] - x < 0 and self.map_w[y][x][1]:
                    app(unseen_list, (x, y))
                elif self.cor[1] - y < 0 and self.map_w[y][x][2]:
                    app(unseen_list, (x, y))
                elif self.cor[1] - y > 0 and self.map_w[y][x][0]:
                    app(unseen_list, (x, y))
                else:
                    vision_list.append((x, y))
                    if x+1 >= len(self.map_f[0]):
                        app(unseen_list, (x+1, y))
                    elif self.map_w[y][x+1][1] or self.map_w[y][x][3]:
                        app(unseen_list, (x+1, y))
                    elif not (x+1, y) in past_list and not (x+1, y) in unseen_list:
                        sub.append((x+1, y))
                    if x <= 0:
                        app(unseen_list, (x-1, y))
                    elif self.map_w[y][x-1][3] or self.map_w[y][x][1]:
                        app(unseen_list, (x-1, y))
                    elif not (x-1, y) in past_list and not (x-1, y) in unseen_list:
                        sub.append((x-1, y))
                    if y+1 >= len(self.map_f):
                        app(unseen_list, (x, y+1))
                    elif self.map_w[y+1][x][2] or self.map_w[y][x][0]:
                        app(unseen_list, (x, y+1))
                    elif not (x, y+1) in past_list and not (x, y+1) in unseen_list:
                        sub.append((x, y+1))
                    if x <= 0:
                        app(unseen_list, (x, y-1))
                    elif self.map_w[y-1][x][0] or self.map_w[y][x][2]:
                        app(unseen_list, (x, y-1))
                    elif not (x, y-1) in past_list and not (x, y-1) in unseen_list:
                        sub.append((x, y-1))
                    past_list.append((x, y))
            actual_list = sub.copy()
            sub.clear()
        self.vision_field = vision_list

    def move(self, new_cor):
        """
                Двигает персонажа с тайла на тайл и отображает процесс
        """
        if new_cor[0] > self.cor[0]:        # Вправо
            self.move_progress[0] += self.speed
            if self.move_progress[0] >= 100:
                self.move_progress[0] = 0
                self.cor = new_cor
        elif new_cor[0] < self.cor[0]:        # Влево
            self.move_progress[0] -= self.speed
            if self.move_progress[0] <= -100:
                self.move_progress[0] = 0
                self.cor = new_cor
        elif new_cor[1] > self.cor[1]:        # Вниз
            self.move_progress[1] += self.speed
            if self.move_progress[1] >= 100:
                self.move_progress[1] = 0
                self.cor = new_cor
        elif new_cor[1] < self.cor[1]:        # Вверх
            self.move_progress[1] -= self.speed
            if self.move_progress[1] <= -100:
                self.move_progress[1] = 0
                self.cor = new_cor
        if self.move_progress == [0,0]:
            self.attackfield_update()
            self.update_visionfield()
            self.step = None
            self.anim_play(False)

    def stop(self):
        """
                Остановить персонажа
        """
        if self.step:
            self.last_stop = self.step
            self.path = None
            if self.move_progress[0] == 0 and self.move_progress[1] == 0:
                self.step = None

    def change_mod(self):
        """
                Включает/выключает пошаговый бой
        """
        self.stepwise_mod = not self.stepwise_mod

    def hit(self, time): # fixme! Много ударов за анимацию у ГГ!!!!!!
        """
                Поворачивает персонажа в сторону цели и бьёт её
        """
        if not self.attack_field.collidepoint(self.target.cor) or self.target.cor not in self.vision_field:
            self.target = None
            return
        if not self.look_direction(self.target.cor):
            return
        if self.cur_anim:
            return
        if self.gear["Hands"]:
            if type(self.gear["Hands"]) == Spell:
                if self.target == self and self.gear["Hands"].type != "Defence":
                    self.target = None
                    return
                self.gear["Hands"].apply(self, self.target, self.cor, self.whizbangs, time.get_time())
        elif self.target != self:
            self.target.effects.append(Effect("hurt", self.target, self.skills["strength"], time.get_time(), time, "instant"))
            self.anim_play("b_punch")
        self.target = None

    def set_hands(self, weapon):
        """
                Смена оружия на новое (или приготовить кулаки, если его нет)
        """
        self.gear["Hands"] = weapon
        if weapon:
            self.attack_distance = weapon.distance
        else:
            self.attack_distance = 1
        self.attackfield_update()

    def set_target(self, target):
        self.target = target

    def apply_thing(self, thing, target, time):
        thing.apply(target, time) # fixme! Ты знаешь, что
        self.anim_play("b_inv_use")

    def hurt(self, damage):
        """
                Получение урона
        """
        if random.randint(1, 10) > 1:
            damage -= self.armor
            if damage < 0:
                damage = 0
            self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.kill_self()

    def kill_self(self):
        self.dead = True

    def update_armor(self, value):
        self.armor += value

    def update_max_health(self, value):
        k = self.health/self.max_health
        self.max_health += value
        self.health = int(self.max_health*k)

    def heal(self, value):
        self.health += value
        if self.health > self.max_health:
            self.health = self.max_health

    def attackfield_update(self):
        """
                Обновляет область, по которой персонаж может бить
        """
        self.attack_field = pygame.Rect(self.cor[0]-self.attack_distance, self.cor[1]-self.attack_distance, self.attack_distance*2+1, self.attack_distance*2+1)

    def set_path(self, path):
        """
                Устанавливает путь
        """
        if path == -1:
            return
        self.path = path

    def look_direction(self, cor):
        """
                Рассчитывает угол поворота персонажа, чтобы он смотрел на определенный тайл
        """
        x1 = cor[0]-self.cor[0]
        y1 = cor[1]-self.cor[1]
        x2 = 0
        y2 = -1
        try:
            self.angle = int(acos((x1*x2+y1*y2)/(sqrt(x1**2+y1**2)*sqrt(x2**2+y2**2)))*180/3.14)
        except:
            pass
        if cor[0]-self.cor[0] > 0:
            self.angle = -self.angle + 360
        if self.rotate != self.angle:
            self.anim_play("rotate")
        else:
            self.anim_play(False)
            return True

    def animations_update(self, body, gear):
        if gear[0]:
            foundation = gear[0].spec_n
        else:
            foundation = body[0][:-4]
        self.animations = {
            "b_punch": (Render_functions.load_image(foundation+"_a_punch1.png", alpha_cannel="True"),
                        Render_functions.load_image(foundation+"_a_punch2.png", alpha_cannel="True"),
                        Render_functions.load_image(foundation+"_a_punch3.png", alpha_cannel="True"),
                        Render_functions.load_image(foundation+"_a_punch4.png", alpha_cannel="True"),
                        Render_functions.load_image(foundation+"_a_punch5.png", alpha_cannel="True")),
            "b_inv_use": (Render_functions.load_image(foundation+".png", alpha_cannel="True"),
                          Render_functions.load_image(foundation+".png", alpha_cannel="True"),
                          Render_functions.load_image(foundation+".png", alpha_cannel="True"),
                          Render_functions.load_image(foundation+".png", alpha_cannel="True"),
                          Render_functions.load_image(foundation+".png", alpha_cannel="True"),
                          Render_functions.load_image(foundation+".png", alpha_cannel="True"),
                          Render_functions.load_image(foundation+".png", alpha_cannel="True"),
                          Render_functions.load_image(foundation+".png", alpha_cannel="True"))
        }

    def get_anim_frame(self):
        a = self.animations[self.cur_anim]
        if self.anim_stage < len(a):
            self.anim_stage += 1
            return a[self.anim_stage-1]
        else:
            self.anim_play(False)
            self.anim_stage = 0

    def img_rotate(self, value, angle=10):
        """
                Поворачивает картинку в сторону значения угла value на angle градусов. 0 градусов - вверх
        """
        a = value
        value -= self.rotate
        if value >= 360:
            value -= 360
        elif value < 0:
            value += 360
        if value <= 180:
            if value < 10:
                self.rotate = a
            else:
                self.rotate += angle
        else:
            if value < 10:
                self.rotate = a
            else:
                self.rotate -= angle
        if self.rotate >= 360:
            self.rotate -= 360
        elif self.rotate < 0:
            self.rotate += 360

    def anim_play(self, ca):
        if self.cur_anim == ca:
            return
        self.cur_anim = ca
        if not ca or ca == "move" or ca == "rotate":
            self.anim_speed = self.coofs[ca]
        else:
            self.anim_speed = self.coofs[ca]/len(self.animations[ca])
        self.worktime = 0

    def img_designer(self):
        """
                Собирает картинку из частей, поворачивает на нужный угол,
                вклеивает на поверхность 100х100 пикселей (размер тайла)
        """
        body = None
        if self.cur_anim:
            if "b_" in self.cur_anim:
                body = self.get_anim_frame()
            elif self.cur_anim == "rotate":
                self.img_rotate(self.angle)
            elif self.cur_anim == "move":
                self.move(self.step)
        if not body:
            if self.gear["Outerwear"]:
                body = self.gear["Outerwear"].img
            else:
                body = self.body["body"]
        head = self.body["head"]
        img = pygame.Surface((body.get_width(), int(head.get_height()/2+body.get_height())), pygame.SRCALPHA)
        img.blit(body, (0, img.get_height()-body.get_height()))
        img.blit(head, (img.get_width()/2-head.get_width()/2, img.get_height()/2-head.get_height()/2))
        img = pygame.transform.rotate(img, self.rotate)
        main_img = pygame.Surface((100, 100), pygame.SRCALPHA)
        main_img.blit(img, (main_img.get_width()/2-img.get_width()/2, main_img.get_height()/2-img.get_height()/2))
        return main_img

    def get_coords_on_map(self):
        return self.cor[0]*100+self.move_progress[0], self.cor[1]*100+self.move_progress[1]

    def render(self, screen):
        screen.blit(self.ren_img, self.get_coords_on_map())
        for w in self.whizbangs:
            w.render(screen)