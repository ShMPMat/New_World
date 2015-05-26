import Render_functions
import Buttons
import Extra_functions
import pygame
import Spell
from findPathLee import findPath

class Interface():
    def __init__(self, char, npc, res, map_floor, map_wall, camera):
        self.character = char
        self.npc_list = npc
        self.all_persons = [char]      # Все персонажи
        self.all_persons.extend(npc)
        self.map_f = map_floor
        self.map_w = map_wall
        self.map_pass = []
        for line in self.map_f:
            self.map_pass.append(line.copy())
        for n in self.npc_list:
            self.map_pass[n.cor[1]][n.cor[0]] = 0
        self.z_ind = False
        self.resolution = res
        self.camera = camera
        self.path = None
        self.pathmarker = Render_functions.load_image('Pathmarker.png', alpha_cannel="True")  # Картинка выбраного пути
        self.ap = Render_functions.load_image('ActP_active.png', alpha_cannel="True")
        self.wasted_ap = Render_functions.load_image('ActP_wasted.png', alpha_cannel="True")
        self.buttons = []
        self.stepwise_buttons = []
        self.windows = [Window(pygame.Rect(0,0,res[0]/2,res[1]-20),"Background.png", [])
                        ]
        self.update_persona_window()
        self.active_windows = []
        x = self.resolution[0]-170
        y = 100
        if type(self.character.spells) == tuple:
            for spell in self.character.spells:
                self.stepwise_buttons.append(Buttons.Button_Flag(Render_functions.load_text(spell.name), self.character.set_wearpon, (x, y), arg=(spell, None)))
                y += 15
        else:
            self.stepwise_buttons.append(Buttons.Button_Flag(Render_functions.load_text(self.character.spells.name), char.set_wearpon, (x, y), arg=(self.character.spells, None)))

    def update(self):
        self.update_persona_window()
        self.map_pass = []
        for line in self.map_f:
            self.map_pass.append(line.copy())
        for n in self.npc_list:
            if not n.dead:
                self.map_pass[n.cor[1]][n.cor[0]] = 0

    def update_persona_window(self):
        self.windows[0].elements = [(Render_functions.load_text("Сила -          "+str(self.character.skills["strength"])), (5, 5)),
                                      (Render_functions.load_text("Магия -        "+str(self.character.skills["magic"])), (5, 25)),
                                       (Render_functions.load_text("Стрельба -   "+str(self.character.skills["shooting"])), (5, 45)),
                                       (Render_functions.load_text(str(self.character.name)), (65, self.resolution[1]-40)),
                                       (Render_functions.load_image('Outerwear_s.png', alpha_cannel="True"), (330,200))]
        if self.character.gear["Outerwear"]:
            self.windows[0].elements.append((Render_functions.load_image(self.character.gear["Outerwear"].img_s, alpha_cannel="True"), (330,200)))

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
            if e.button == 1 and not self.z_ind:
                chosen_tile = Extra_functions.get_click_tile(e.pos, self.camera.cor, self.map_f)
                t = True
                for per in self.all_persons:
                    if chosen_tile == per.cor:
                        self.character.set_target(per)
                        t = False
                        break
                if t:
                    self.character.set_path(findPath(self.map_pass, self.map_w, self.character.cor, chosen_tile))

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
        screen.blit(Render_functions.load_text("Здоровье "+str(self.character.healf)+"|"+str(self.character.max_healf)), (self.resolution[0]-110, 5))
        screen.blit(Render_functions.load_text("Манна "+str(self.character.manna)+"|"+str(self.character.max_manna)), (self.resolution[0]-110, 25))
        screen.blit(Render_functions.load_text("Броня "+str(self.character.armor)), (self.resolution[0]-110, 45))
        if self.buttons:
            for but in self.buttons:
                    but.render(screen)
        x = self.resolution[0] - 330
        y = self.resolution[1] - 25
        for i in range(15):
            if i < self.character.action_points:
                screen.blit(self.ap, (x, y))
            else:
                screen.blit(self.wasted_ap, (x, y))
            x += 22
        x = self.resolution[0] - 375
        y = self.resolution[1] - 45
        w = self.character.gear["Wearpon"]
        if w:
            if type(w) == Spell.Spell:
                if w.type == "Attacking":
                    screen.blit(Render_functions.load_image('Fireball.png', alpha_cannel="True"), (x, y))
                elif w.type == "Defence":
                    screen.blit(Render_functions.load_image('Shield.png', alpha_cannel="True"), (x, y))
        else:
            screen.blit(Render_functions.load_image('Fist.png', alpha_cannel="True"), (x, y))
        if self.character.stepwise_mod:
            if self.stepwise_buttons:
                for but in self.stepwise_buttons:
                    but.render(screen)
            if self.path:
                for tile in self.path:
                    screen.blit(self.pathmarker, (coof[0]+tile[0]*100, coof[1]+tile[1]*100))
            for npc in self.npc_list:
                if npc.aggression:
                    cor = npc.get_coords_on_map()[0] + self.camera.cor[0], npc.get_coords_on_map()[1] + self.camera.cor[1]
                    screen.blit(Render_functions.load_text(str(npc.healf), color=(200, 0, 0)), (cor[0]+5, cor[1]+5))
                    screen.blit(Render_functions.load_text(str(npc.manna), color=(0, 0, 150)), (cor[0]+5, cor[1]+19))
                    screen.blit(Render_functions.load_text(str(npc.armor), color=(100, 100, 100)), (cor[0]+5, cor[1]+33))
            if self.character.dead:
                screen.blit(Render_functions.load_text("Вы мертвы", pt=200, color=(220, 0, 0)), (80, self.resolution[1]/2-100))
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
        for sur, cor in self.elements:
            screen.blit(sur, cor)