import pygame
import Tile
from Thing import Example, Equipment
from Character import Character
from Camera import Camera
from Interface import Interface
from Groups import groups
from NPC import NPC
import Render_functions
import pickle
from Buttons import  Button, Button_Img
import Spell


class GameProcess():
    def __init__(self, map_f, map_w):
        self.items = {0: Example(doctor_robe), 1: Example(doctor_robe)}
        self.items[0].update_slots(self.items[1],(0,0))
        self.character = Character("Test Character", groups["cher"], (2, 0), map_f, map_w, skills=(1, 3, 1), spelllist=(Spell.fireball, Spell.improve_aah), gear=(self.items[0], None))     # Создание игрового персонажа
        self.all_npc = [NPC("Test_Enemy", groups["enemy"], (1, 4), map_f, map_w, gear=(None, None)), NPC("Test_Enemy_2", groups["enemy"], (4, 2), map_f, map_w, gear=(None, None))]       # Ссылка на всех NPC
        self.all_persons = [self.character]
        self.all_persons.extend(self.all_npc)
        self.camera = Camera([0,0], (len(map_f[0])*100, len(map_f)*100), (RES_X, RES_Y))
        self.interface = Interface(self.character, self.all_npc, (RES_X, RES_Y), map_f, map_w, self.camera)
        self.interface.buttons.append(Button("Пошагово/Реальное время", (0, RES_Y-20), self.change_mod))
        self.interface.buttons.append(Button_Img(("Persona_icon.png","Persona_icon_2.png"), (RES_X-135, 7), self.interface.window_manager, arg=1))
        self.world_img = Render_functions.scene_render(map_f, map_w, objects, pygame.Surface((RES_X, RES_Y)))          # Поверхность, на которой отображается весь игровой мир

    def events(self, e):
        self.interface.events(e)
        self.camera.events(e)

    def update(self, dt):
        self.interface.update()
        if self.character.stepwise_mod:
            self.character.update(dt, self.all_persons)
            if self.character.action_points and not self.character.anim_play:
                for npc in self.all_npc:
                    npc.action_points += self.character.action_points
                self.character.action_points = 0
            for npc in self.all_npc:
                # print("   Закончил -    ", npc.path, "  Тревога -  ", npc.alarm, "  ОД   ", npc.action_points, "Анимация - ", npc.anim_play)
                npc.update(dt, map_f, map_w, self.get_objects_in_area(npc.vision_field), self.all_persons)
                if not npc.finish:
                    break
        else:
            self.character.update(dt, self.all_persons)
            for npc in self.all_npc:
                npc.action_points = 0
                npc.update(dt, map_f, map_w, self.get_objects_in_area(npc.vision_field), self.all_persons)
                if self.character in npc.alarm:
                    self.on_stepwise_mod()

    def on_stepwise_mod(self):
        """
                Включить пошаговый режим для всех
        """
        for men in self.all_persons:
            men.stepwise_mod = True

    def change_mod(self):
        """
                Сменить режим с пошагового на нормальный или обратно
        """
        for npc in self.all_npc:
            if npc.alarm:
                return
        self.character.change_mod()
        try:
            for npc in self.all_npc:
                npc.change_mod()
        except:
            self.all_npc.change_mod()

    def get_objects_in_area(self, area):
        objects = []
        for tile in area:
            for man in self.all_persons:
                if tile == man.cor:
                    objects.append(man)
        return objects

    def render(self, screen):
        self.ren = Render_functions.scene_render(map_f, map_w, objects, self.world_img)
        for men in self.all_persons:
            men.render(self.ren)
        screen.blit(self.ren, self.camera.cor)
        self.interface.render(screen, self.camera.cor)


def set_scene(scene_value):
    """
    Уникальная нанофункция, сменяющая сцену. Благодаря моим глубочайшим познаниям в архитектуре языка выглядит так уродливо
    """
    scene_value[0][0] = scene_value[1]



# Globals
FPS = 60                                            # ФПС программы
RES_X = 900                                         # Разрешение по длине
RES_Y = 700                                         # Разрешение по ширине


# Main Actions
file = open('d', 'rb')                              # Открыть файл с картами
map_f, map_w, map_d = pickle.load(file)             # Загрузить карты в собственные переменные
file.close()                                        # Закрыть файл с картами


pygame.init()                                       # PyGame начинает работу
screen = pygame.display.set_mode((RES_X, RES_Y))    # Создаем окно программы
clock = pygame.time.Clock()                         # Создаем таймер
menu = ["game"]                                     # Меню, которое в данный момент на экране
mainloop = True                                     # Двигатель главного цикла

objects = {     # Все доступные объекты
    "Floor": {
        1: Tile.Floor((0, 0), "B_Tile.png", 1),
        2: Tile.Floor((0, 0), "Tile-2.png", 2),
        3: Tile.Floor((0, 0), "Ground_1.png", 3)
    },
    "Wall": {
        1: Tile.Wall((0, 0), "Wall_1.png", 1)
    }
}


doctor_robe = Equipment("Врачебный халат", "White_doc_robe", (2, 2), 2, 1000, (5,5))
bulletproof_vest = Equipment("Бронежилет", "Bulletproof_vest", (2, 2), 2, 1000, (3,3))

game_process = GameProcess(map_f, map_w)

while mainloop:
    screen.fill((0, 0, 0))
    if menu[0] == "game":
        for e in pygame.event.get():
            if e.type == pygame.MOUSEMOTION or e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:
                game_process.events(e)
            if e.type == pygame.QUIT:
                    mainloop = False
        game_process.update(clock.get_time())
        game_process.render(screen)
    pygame.display.set_caption("FPS: " + str(clock.get_fps()))
    clock.tick(FPS)         # Управление ФПС
    pygame.display.flip()   # Обновляем дисплей