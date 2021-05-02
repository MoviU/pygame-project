import pygame
import random

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1200

fon_verh = pygame.image.load('Rus\\Verh.png')
fon_verh_rect = fon_verh.get_rect(left=0)

fon_nuz = pygame.image.load('Rus\\Nuz.png')
fon_nuz_rect = fon_nuz.get_rect(left=0)

canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

class Dragon:
    def __init__(self):
        self.dragon_img = pygame.image.load('Rus//Dragon.png')
        self.dragon_img_rect = self.dragon_img.get_rect()
        self.dragon_img_rect.top = WINDOW_HEIGHT//2
        self.dragon_img_rect.right = WINDOW_WIDTH
        self.up = False
        self.down = True

    def update(self):
        canvas.blit(self.dragon_img, self.dragon_img_rect)
        if self.dragon_img_rect.top <= fon_verh_rect.bottom:
            self.up = False
            self.down = True
        elif self.dragon_img_rect.bottom + 40 >= fon_nuz_rect.top:
            self.up = True
            self.down = False

        if self.up:
            self.dragon_img_rect.top -= 10
        elif self.down:
            self.dragon_img_rect.top += 10