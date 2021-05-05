import pygame
import random


class Dragon:
    def __init__(self, window_height, window_width):

        self.dragon = pygame.image.load('Rus\\dragon\\dragon-1.png')
        self.dragon_img = pygame.transform.scale(self.dragon, (150, 150))
        self.dragon_img_rect = self.dragon_img.get_rect()
        self.dragon_img_rect.bottom = window_height // 2
        self.dragon_img_rect.right = window_width
        self.up = False
        self.down = False




    def update(self, canvas, fon_verh_rect, fon_nuz_rect, dragon_speed):
        self.random_move = random.randint(0, 101)
        self.move_id = random.randint(0, 1)

        canvas.blit(self.dragon_img, self.dragon_img_rect)

        if self.dragon_img_rect.bottom >= 150 and self.dragon_img_rect.bottom <= 450 and self.random_move >= 97:
            if self.move_id == 0:
                self.up = False
                self.down = True

            elif self.move_id == 1:
                self.up = True
                self.down = False

        elif self.dragon_img_rect.top <= fon_verh_rect.bottom:
            self.up = False
            self.down = True

        elif self.dragon_img_rect.bottom >= fon_nuz_rect.top:
            self.up = True
            self.down = False


        if self.up:
            self.dragon_img_rect.top -= dragon_speed
        elif self.down:
            self.dragon_img_rect.top += dragon_speed


class Flames:
    def __init__(self, dragon):
        self.flames = pygame.image.load('Rus\\fire.png')
        self.flames_img = pygame.transform.scale(self.flames, (40, 40))
        self.flames_img_rect = self.flames_img.get_rect()
        self.flames_img_rect.right = dragon.dragon_img_rect.left
        self.flames_img_rect.top = dragon.dragon_img_rect.top + 50

    def update(self, canvas, flames_speed):
        canvas.blit(self.flames_img, self.flames_img_rect)
        if self.flames_img_rect.left > 0:
            self.flames_img_rect.left -= flames_speed
