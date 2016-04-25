import pygame

class Camera():
    def __init__(self, cor):
        self.cor = cor
        self.ch = False

    def events(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:
            if e.button == 2:
                self.ch = not self.ch
        elif e.type == pygame.MOUSEMOTION:
            if self.ch:
                self.move(e.rel)

    def move(self, value):
        self.cor[0] += value[0]
        self.cor[1] += value[1]
        if self.cor[0] > 0:
            self.cor[0] = 0
        if self.cor[1] > 0:
            self.cor[1] = 0