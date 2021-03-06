import pygame
import random


class Dragon:
    def __init__(self, window_height, window_width, anim_count=0):

        self.dragon_fly_img = [pygame.image.load('Rus//dragon//dragon_fly1.png'),
                              pygame.image.load('Rus//dragon//dragon_fly2.png'),
                              pygame.image.load('Rus//dragon//dragon_fly3.png'),
                              pygame.image.load('Rus//dragon//dragon_fly4.png'),
                              pygame.image.load('Rus//dragon//dragon_fly5.png'),
                              pygame.image.load('Rus//dragon//dragon_fly6.png'),
                              pygame.image.load('Rus//dragon//dragon_fly7.png'),
                              pygame.image.load('Rus//dragon//dragon_fly8.png')]
        self.dragon_img = self.dragon_fly_img[anim_count//8]
        self.dragon_img_rect = self.dragon_img.get_rect()
        self.dragon_img_rect.bottom = window_height // 2
        self.dragon_img_rect.right = window_width
        self.up = False
        self.down = False
        self.dragon_fly = True



    def update(self, canvas, fon_verh_rect, fon_nuz_rect, anim_id):
        self.random_move = random.randint(0, 101)
        self.move_id = random.randint(0, 1)

        canvas.blit(self.dragon_img, self.dragon_img_rect)
        self.dragon_img = self.dragon_fly_img[anim_id]

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
            self.dragon_img_rect.top -= 7
        elif self.down:
            self.dragon_img_rect.top += 7
