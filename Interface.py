import Render_functions
import Buttons
import Extra_functions
import pygame
import Spell
import Thing
from findPathLee import findPath

class Interface():
    def __init__(self, char, npc, res, map_floor, map_wall, camera):
        self.character = char                   # Игровой персонаж
        self.npc_list = npc                     # NPC
        self.all_persons = [char]
        self.all_persons.extend(npc)            # Все персонажи (NPC и ГГ)
        self.map_f = map_floor                  # Карта тайлов
        self.map_w = map_wall                   # Карта стен
        self.map_pass = []                      # Карта проходимых\непроходимых тайлов
        for line in self.map_f:
            self.map_pass.append(line.copy())
        for n in self.npc_list:
            self.map_pass[n.cor[1]][n.cor[0]] = 0
        self.z_ind = False
        self.resolution = res                   # Разрешение окна
        self.camera = camera                    # Ссылка на камеру
        self.cursor = None
        self.path = None
        self.pathmarker = Render_functions.load_image('Pathmarker.png', alpha_cannel="True")  # Картинка выбраного пути
        self.ap = Render_functions.load_image('ActP_active.png', alpha_cannel="True")         # Картинка доступных ОД
        self.wasted_ap = Render_functions.load_image('ActP_wasted.png', alpha_cannel="True")  # Картинка потраченых ОД
        self.marks = {
            "Fist": Render_functions.load_image('Fist.png', alpha_cannel="True"),
            "Shield": Render_functions.load_image('Shield.png', alpha_cannel="True"),
            "Fireball": Render_functions.load_image('Fireball.png', alpha_cannel="True")
        }
        self.buttons = []
        self.stepwise_buttons = []
        self.ch = None
        self.des = None
        self.inventory_cor = (30, 100)           # Координаты первого окна инвентаря
        self.inventory_cors_count = []
        self.windows = [Window(pygame.Rect(0,0,res[0]/2,res[1]-20),"Background.png", [])
                        ]
        self.update_persona_window()
        self.active_windows = []                # Окна, которые в данный момент отображаются на экране
        x = self.resolution[0]-170
        y = 100
        if type(self.character.spells) == tuple:
            for spell in self.character.spells:
                self.stepwise_buttons.append(Buttons.Button_Flag(Render_functions.load_text(spell.name), self.character.set_wearpon, (x, y), arg=(spell, None)))
                y += 15
        else:
            self.stepwise_buttons.append(Buttons.Button_Flag(Render_functions.load_text(self.character.spells.name), char.set_wearpon, (x, y), arg=(self.character.spells, None)))

    def update(self):
        if 0 in self.active_windows:
            self.update_persona_window()
        self.map_pass = []
        for line in self.map_f:
            self.map_pass.append(line.copy())
        for n in self.npc_list:
            if not n.dead:
                self.map_pass[n.cor[1]][n.cor[0]] = 0

    def update_persona_window(self):
        self.windows[0].elements = {"static": [(Render_functions.load_text("Сила -          "+str(self.character.skills["strength"])), (5, 5)),
                                    (Render_functions.load_text("Магия -        "+str(self.character.skills["magic"])), (5, 25)),
                                    (Render_functions.load_text("Стрельба -   "+str(self.character.skills["shooting"])), (5, 45)),
                                    (Render_functions.load_text(str(self.character.name)), (65, self.resolution[1]-40)),
                                    (Render_functions.load_image('Outerwear_s.png', alpha_cannel="True"), (330,200)),
                                    (Render_functions.load_image('W_s.png', alpha_cannel="True"), (390,180)),
                                    (Render_functions.load_image('W_s.png', alpha_cannel="True"), (290,180))],
                                     "active": []}
        if self.character.gear["Outerwear"]:                # Проверка на наличие слотов инвентаря и их графическая отрисовка
            cor = list(self.inventory_cor)
            self.inventory_count = 0
            self.windows[0].elements["active"].append((Render_functions.tiled_background("Inventory_tile.png", self.character.gear["Outerwear"].slots[0]*20, self.character.gear["Outerwear"].slots[0]*20), tuple(cor)))
            cor[1] += self.windows[0].elements["active"][-1][0].get_height() + 10
            self.inventory_cors_count.append((tuple(cor),self.character.gear["Outerwear"]))
            for j, c in self.character.gear["Outerwear"].items:
                self.windows[0].elements["active"].append((j.icon, (self.inventory_cor[0]+c.x*20,self.inventory_cor[1]+c.y*20)))
            self.windows[0].elements["active"].append((self.character.gear["Outerwear"].img_s, (330, 200)))
            if self.des:
                for el, cor in self.windows[0].elements["active"]:
                    if self.des[0] == el:
                        self.windows[0].elements["active"].append((Render_functions.load_text(self.character.gear["Outerwear"].name), self.des[1]))
        if self.cursor:
            self.windows[0].elements["active"].append((self.cursor[0].icon, self.cursor[1]))

    def events(self, e):
        self.z_ind = False
        for n in self.active_windows:
            if self.windows[n].rect.collidepoint(e.pos):
                self.z_ind = True
        if self.buttons:
            for but in self.buttons:
                if but.events(e):
                    self.z_ind = True
        if self.character.stepwise_mod:
            for but in self.stepwise_buttons:
                if but.events(e):
                    self.z_ind = True
                    self.buttons_up(but, self.stepwise_buttons)
            if e.type == pygame.MOUSEMOTION:
                self.path = findPath(self.map_pass, self.map_w, self.character.cor, (Extra_functions.get_click_tile(e.pos, self.camera.cor, self.map_pass)))
                if self.path == -1:
                    self.path = None
        if e.type == pygame.MOUSEBUTTONUP:
            if e.button == 1:
                if not self.z_ind:
                    chosen_tile = Extra_functions.get_click_tile(e.pos, self.camera.cor, self.map_f)
                    t = True
                    for per in self.all_persons:
                        if chosen_tile == per.cor:
                            self.character.set_target(per)
                            t = False
                            break
                    if t:
                        self.character.set_path(findPath(self.map_pass, self.map_w, self.character.cor, chosen_tile))
                elif self.cursor:
                    for cor, con in self.inventory_cors_count:
                        chosen_tile = Extra_functions.get_click_tile(e.pos, cor, con.slots, size=20) # Fixme! ДА ЧЕМ Я ВООБЩЕ ДУМАЛ, КОГДА ЭТО ПИСАЛ????
                        if chosen_tile != -1:
                            if con.update_slots(self.cursor[0], chosen_tile):
                                if type(self.cursor[2]) == str:
                                    self.character.gear[self.cursor[2]] = None
                                    break
        if e.type == pygame.MOUSEMOTION and self.cursor:
            self.cursor[1][0] += e.rel[0]
            self.cursor[1][1] += e.rel[1]
        if e.type == pygame.MOUSEBUTTONUP:
            if e.button == 1:
                self.cursor = None
        if not 0 in self.active_windows:
            return
        if self.character.gear["Outerwear"]:
            for el, cor in self.windows[0].elements["active"]:
                if el != self.character.gear["Outerwear"].img_s:
                    continue
                rect = el.get_rect()
                rect.move_ip(cor)
                if rect.collidepoint(e.pos):
                    self.des = el, [e.pos[0]+10, e.pos[1]]
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        if e.button == 1:
                            self.cursor = [self.character.gear["Outerwear"], list(e.pos), "Outerwear"]
                            self.windows[0].elements["active"].remove((el, cor))
                else:
                    self.des = None

    def buttons_up(self, but, lst):
        """
                Получает кнопку, на которую нажали и список с кнопками. "Отжимает" остальные кнопки
        """
        for button in lst:
            if button != but and type(but) == Buttons.Button_Flag:
                button.stat = False

    def window_manager(self, num):
        num -= 1
        if num in self.active_windows:
            self.active_windows.remove(num)
        else:
            self.active_windows.append(num)

    def render(self, screen, coof):
        if self.character.stepwise_mod:
            if self.stepwise_buttons:
                for but in self.stepwise_buttons:
                    but.render(screen)
            if self.path:
                for tile in self.path:
                    screen.blit(self.pathmarker, (coof[0]+tile[0]*100, coof[1]+tile[1]*100))
            # for tile in self.character.vision_field:
            #         screen.blit(self.pathmarker, (coof[0]+tile[0]*100, coof[1]+tile[1]*100))
            for npc in self.npc_list:
                for tile in npc.vision_field:
                    screen.blit(self.pathmarker, (coof[0]+tile[0]*100, coof[1]+tile[1]*100))
                cor = npc.get_coords_on_map()[0] + self.camera.cor[0], npc.get_coords_on_map()[1] + self.camera.cor[1]
                screen.blit(Render_functions.load_text(str(npc.health), color=(200, 0, 0)), (cor[0]+5, cor[1]+5))
                screen.blit(Render_functions.load_text(str(npc.manna), color=(0, 0, 150)), (cor[0]+5, cor[1]+19))
                screen.blit(Render_functions.load_text(str(npc.armor), color=(100, 100, 100)), (cor[0]+5, cor[1]+33))
            if self.character.dead:
                screen.blit(Render_functions.load_text("Вы мертвы", pt=200, color=(220, 0, 0)), (80, self.resolution[1]/2-100))
        screen.blit(Render_functions.load_text("Здоровье "+str(self.character.health)+"|"+str(self.character.max_health)), (self.resolution[0]-110, 5))
        screen.blit(Render_functions.load_text("Манна "+str(self.character.manna)+"|"+str(self.character.max_manna)), (self.resolution[0]-110, 25))
        screen.blit(Render_functions.load_text("Броня "+str(self.character.armor)), (self.resolution[0]-110, 45))
        if self.buttons:
            for but in self.buttons:
                but.render(screen)
        x = self.resolution[0] - 45
        y = self.resolution[1] - 45
        w = self.character.gear["Wearpon"]
        if w:
            if type(w) == Spell.Spell:
                if w.type == "Attacking":
                    screen.blit(self.marks["Fireball"], (x, y))
                elif w.type == "Defence":
                    screen.blit(self.marks["Shield"], (x, y))
        else:
            screen.blit(self.marks["Fist"], (x, y))
        if self.active_windows:
            for n in self.active_windows:
                self.windows[n].render(screen)


class Window():
    def __init__(self, rect, background, elements):
        self.rect = rect
        self.background = Render_functions.tiled_background(background, self.rect.width, self.rect.height)
        self.elements = elements

    def render(self, screen):
        screen.blit(self.background, self.rect.topleft)
        for sur, cor in self.elements["static"]:
            screen.blit(sur, cor)
        for sur, cor in self.elements["active"]:
            screen.blit(sur, cor)