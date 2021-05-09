import pygame
from shop import Shop

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
class Knight:
    def __init__(self):
        self.__shop = Shop()
        self.knight_img = pygame.image.load('Rus\\{}'.format(self.__shop.getSkin()))
        self.knight_img = pygame.transform.scale(self.knight_img, (52, 85))
        self.knight_img_rect = self.knight_img.get_rect()
        self.knight_img_rect.left = 20
        self.knight_img_rect.top = WINDOW_HEIGHT//2 - 100
        self.down = True
        self.up = False

    def update(self, canvas, fon_verh_rect, fon_nuz_rect):
        canvas.blit(self.knight_img, self.knight_img_rect)

        if self.knight_img_rect.top <= fon_verh_rect.bottom:
            self.knight_img_rect.top = fon_verh_rect.bottom + 25

        if self.knight_img_rect.bottom >= fon_nuz_rect.top:
            self.knight_img_rect.bottom = fon_nuz_rect.top - 25

        if self.up:
            self.knight_img_rect.top -= 5
        if self.down:
            self.knight_img_rect.bottom += 5