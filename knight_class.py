import pygame
from shop import Shop
from effect import Effect
import os

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
        self.life = 100
        self.shield = self.shield(self.__shop.getEffect())
        if self.__shop.getEffect() != 'none':
            self.__path = 'Rus/' + self.__shop.getEffect() + '/'
            self.__effect_anim_count = len([f for f in os.listdir(self.__path)
                                     if os.path.isfile(os.path.join(self.__path, f))])
            self.effect = Effect(self.__path, self.__effect_anim_count, self.knight_img_rect.left, self.knight_img_rect.top)
        else:
            self.effect = False
        self.down = True
        self.up = False
        self.duration = 10

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
        if self.effect:
            self.effect.rect.center = self.knight_img_rect.center
            if self.__effect_anim_count < 10:
                if self.effect:
                    self.effect.update(canvas, 10)
            else:
                self.effect.update(canvas)
        self.regenerate()
    def damage(self, hp):
        if self.shield != False and self.shield > 0:
            self.shield -= hp
        else:
            self.life -= hp

    def regenerate(self):
        effect = self.__shop.getEffect()
        if effect == 'effect_1' or effect == 'effect_2':
            if self.duration == 0:
                if self.life <= 100:
                    self.life += 1
                self.duration = 10
            self.duration -= 1

    def shield(self, effect):
        if effect == 'effect_1':
            return 100
        return False
