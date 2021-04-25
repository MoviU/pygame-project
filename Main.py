import pygame
import sys

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
FPS = 20
DARK_BLUE = (35, 31, 60)
GREEN = (0, 255, 0)
fon_verh = pygame.image.load('Rus\\Verh.png')
fon_verh_rect = fon_verh.get_rect(left=0)

fon_nuz = pygame.image.load('Rus\\Nuz.png')
fon_nuz_rect = fon_nuz.get_rect(left = 0)
CLOCK = pygame.time.Clock()
font = pygame.font.Font(None, 30)

canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Лицарська епоха')

class Dragon:
    def __init__(self):
        self.dragon_img = pygame.image.load('Rus//Dragon.png')
        self.dragon_img_rect = self.dragon_img.get_rect()
        self.dragon_img_rect.top = WINDOW_HEIGHT//2
        self.dragon_img_rect.right = WINDOW_WIDTH
        self.up = True
        self.down =False

    def update(self):
        canvas.blit(self.dragon_img, self.dragon_img_rect)
        if self.dragon_img_rect.top <= fon_verh_rect.bottom:
            self.up = False
            self.down = True
        elif self.dragon_img_rect.bottom +40>= fon_nuz_rect.top:
            self.up = True
            self.down = False

        if self.up:
            self.dragon_img_rect.top -= 10
        elif self.down:
            self.dragon_img_rect.top += 10

class Flames:
    def __init__(self):
        self.flames = pygame.image.load('Rus\\fire.png')
        self.flames_img = pygame.transform.scale(self.flames, (20, 20))
        self.flames_img_rect = self.flames_img.get_rect()
        self.flames_img_rect.right = dragon.dragon_img_rect.left
        self.flames_img_rect.top = dragon.dragon_img_rect.top + 50

    def update(self):
        canvas.blit(self.flames_img, self.flames_img_rect)
        if self.flames_img_rect.left > 0:
            self.flames_img_rect.left-=20


class Knight_class:
    def __init__(self):
        self.knight_img = pygame.image.load('Rus//Knight.png')
        self.knight_img_rect = self.knight_img.get_rect()
        self.knight_img_rect.left = 20
        self.knight_img_rect.top = WINDOW_HEIGHT//2 - 100
        self.down = True
        self.up = False

    def update(self):
        canvas.blit(self.knight_img, self.knight_img_rect)

        #відловив зіткнення нижніх та верхніх меж хляхом перемішення героя в позицію 100
        #при цьому виникає глюк на 4 рівні при зіткненні з верхом або низом, тому покорегуйте

        if self.knight_img_rect.top <= fon_verh_rect.bottom:
            self.knight_img_rect.top=100

        if self.knight_img_rect.bottom >= fon_nuz_rect.top:
            self.knight_img_rect.top=100

        if self.up:
            self.knight_img_rect.top -= 10
        if self.down:
            self.knight_img_rect.bottom += 10

def start_game():
    canvas.fill(DARK_BLUE)
    start_img = pygame.image.load('Rus//start.png')
    start_img_rect = start_img.get_rect()
    start_img_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
    canvas.blit(start_img, start_img_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                game_loop()
        pygame.display.update()

def game_over():
    game_over_img = pygame.image.load('Rus//The_end.png')
    game_over_img_rect = game_over_img.get_rect()
    game_over_img_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
    canvas.blit(game_over_img, game_over_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                game_loop()
        pygame.display.update()

def level(SCORE):
    global LEVEL
    if SCORE in range(0, 10):
        fon_verh_rect.bottom = 50
        fon_nuz_rect.top = WINDOW_HEIGHT - 50
        LEVEL = 1
    elif SCORE in range(10, 20):
        fon_verh_rect.bottom = 100
        fon_nuz_rect.top = WINDOW_HEIGHT - 100
        LEVEL = 2
    elif SCORE in range(20, 30):
        fon_verh_rect.bottom = 150
        fon_nuz_rect.top = WINDOW_HEIGHT - 150
        LEVEL = 3
    elif SCORE in range(30, 100):
        fon_verh_rect.bottom = 200
        fon_nuz_rect.top = WINDOW_HEIGHT - 200
        LEVEL = 4



def game_loop():
        global dragon
        dragon = Dragon()
        knight = Knight_class()
        flames=Flames()
        flames_list = []
        pygame.mixer.music.load('Rus//muz.mp3')
        pygame.mixer.music.play(-1, 0.0)

        add_new_flame_counter=0
        popav=100
        SCORE=0
        while True:
            canvas.fill(DARK_BLUE)
            fon_verh_rect.bottom = 50
            fon_nuz_rect.top = WINDOW_HEIGHT - 50
            level(SCORE)
            add_new_flame_counter += 1
            if add_new_flame_counter == 20: #визначає протяжність часу протягом якого буде запускатись вогонь
                add_new_flame_counter = 0
                new_flame = Flames()
                flames_list.append(new_flame)
            for f in flames_list:
                if f.flames_img_rect.left <= 0:
                    flames_list.remove(f)
                    SCORE += 1
                f.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        knight.up = True
                        knight.down = False
                    elif event.key == pygame.K_DOWN:
                        knight.down = True
                        knight.up = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        knight.up = False
                        knight.down = True
                    elif event.key == pygame.K_DOWN:
                        knight.down = True
                        knight.up = False

            for f in flames_list:
                if f.flames_img_rect.colliderect(knight.knight_img_rect):
                    popav=popav-5
                    pygame.display.set_caption(str(popav))
                    if popav<=0:
                        game_over()

            score_font = font.render('Кулі:' + str(SCORE), True, GREEN)
            canvas.blit(score_font, (100, fon_verh_rect.bottom + 30))

            level_font = font.render('Рівень:' + str(LEVEL), True, GREEN)
            canvas.blit(level_font, (200, fon_verh_rect.bottom + 30))
            canvas.blit(fon_verh, fon_verh_rect)
            canvas.blit(fon_nuz, fon_nuz_rect)
            knight.update()
            dragon.update()
            pygame.display.update()
            CLOCK.tick(FPS)


start_game()

