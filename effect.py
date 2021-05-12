import pygame

class Effect():
    def __init__(self, path, count, x, y):
        self.anim_images = []
        for i in range(count):
            print(path + str(i + 1) + '.png')
            self.anim_images.append(pygame.transform.scale(pygame.image.load(path + str(i + 1) + '.png').convert_alpha(), [100, 99]))
        self.anim_id = 0
        self.count = count
        self.image = self.anim_images[self.anim_id//count]
        self.rect = self.image.get_rect(left = x, top = y)
    def update(self, canvas, duration = 2):
        if self.anim_id == self.count:
            self.anim_id = 0
        self.image = self.anim_images[self.anim_id // duration]
        self.anim_id += 1
        canvas.blit(self.image, self.rect)
