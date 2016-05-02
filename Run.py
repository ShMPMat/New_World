import pygame
import Tile
import Thing
from Character import Character
from Camera import Camera
from Interface import Interface
from Groups import groups
from NPC import NPC
import Render_functions
import pickle
import Buttons
import Spell


class GameProcess():
    def __init__(self, map_f, map_w):
        self.turn = -1                      # Очередь хода в пошаговом режиме (-1 - это наш персонаж)
        self.character = Character("Test Character", groups["cher"], (2, 0), map_f, map_w, skills=(1, 3, 1), spelllist=(Spell.fireball, Spell.improve_aah), gear=(doctor_robe, None))     # Создание игрового персонажа
        self.all_npc = [NPC("Test_Enemy", groups["enemy"], (1, 4), map_f, map_w, gear=(None, None)), NPC("Test_Enemy_2", groups["enemy"], (4, 2), map_f, map_w, gear=(None, None))]       # Ссылка на всех NPC
        self.all_persons = [self.character]
        self.all_persons.extend(self.all_npc)
        self.camera = Camera([0,0], (len(map_f[0])*100, len(map_f)*100), (RES_X, RES_Y))
        self.interface = Interface(self.character, self.all_npc, (RES_X, RES_Y), map_f, map_w, self.camera)
        self.interface.buttons.append(Buttons.Button("Пошагово/Реальное время", (0, RES_Y-20), self.change_mod))
        self.interface.buttons.append(Buttons.Button_Img(("Persona_icon.png","Persona_icon_2.png"), (RES_X-135, 7), self.interface.window_manager, arg=1))
        self.interface.stepwise_buttons.append(Buttons.Button("Конец хода", (300, RES_Y-20), self.new_step))
        self.world_img = pygame.Surface((RES_X, RES_Y))          # Поверхность, на которой отображается весь игровой мир

    def events(self, e):
        self.interface.events(e)
        self.camera.events(e)

    def update(self, dt):
        self.interface.update()
        if self.character.stepwise_mod:
            if self.turn == -1:
                self.character.update(dt, self.all_persons)
            else:
                try:
                    self.all_npc[self.turn].update(dt, map_f, map_w, self.get_objects_in_area(self.all_npc[self.turn].vision_field), self.all_persons)
                    print(self.turn, "   Закончил -    ", self.all_npc[self.turn].path, "  Тревога -  ", self.all_npc[self.turn].alarm, "  ОД   ", self.all_npc[self.turn].action_points, "Анимация - ", self.all_npc[self.turn].anim_play)
                    if self.all_npc[self.turn].finish:
                        self.turn += 1
                except:
                    if self.all_npc[self.turn-1].finish:
                        self.turn = -1
        else:
            self.character.update(dt, self.all_persons)
            for npc in self.all_npc:
                npc.update(dt, map_f, map_w, self.get_objects_in_area(npc.vision_field), self.all_persons)
                if self.character in npc.alarm:
                    self.on_stepwise_mod()

    def on_stepwise_mod(self):
        """
                Включить пошаговый режим для всех
        """
        self.turn = -1
        for men in self.all_persons:
            men.stepwise_mod = True

    def change_mod(self):
        """
                Сменить режим с пошагового на нормальный или обратно
        """
        for npc in self.all_npc:
            if npc.alarm:
                return
        self.turn = -1
        self.character.change_mod()
        try:
            for npc in self.all_npc:
                npc.change_mod()
        except:
            self.all_npc.change_mod()

    def new_step(self):
        """
                Начать новый ход (он начинается с хода противников)
        """
        self.turn = 0
        self.character.action_points = 15
        try:
            for npc in self.all_npc:
                npc.action_points = 15
                npc.finish = False
        except:
            self.all_npc.action_points = 15
            self.all_npc.finish = False

    def get_objects_in_area(self, area):
        objects = []
        for tile in area:
            for man in self.all_persons:
                if tile == man.cor:
                    objects.append(man)
        return objects

    def render(self, screen):
        self.world_img = Render_functions.scene_render(map_f, map_w, objects, self.world_img)
        for men in self.all_persons:
            men.render(self.world_img)
        screen.blit(self.world_img, self.camera.cor)
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


doctor_robe = Thing.Equipment("Врачебный халат","White_doc_robe_icon.png", (2,2), 2,1000, 0, "White_doc_robe.png", "White_doc_robe_s.png")
bulletproof_vest = Thing.Equipment("Бронежилет","Bulletproof_vest_icon.png", (2,2), 2,1000, 0, "Bulletproof_vest.png", "Bulletproof_vest_s.png")

game_process = GameProcess(map_f, map_w)

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