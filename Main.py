import pygame
import sys
from effect import Effect
import pygame.sprite
import random
import files
import os

os.environ['SDL_VIDEO_CENTERED'] = '1' #Центрування вікна, перед ініціалізацією pygame

PAUSED = False
fileManager = files.fileManager()
pygame.init()

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

BackGround = Background('Rus\\fon.jpg', [0,0])

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
FPS = 60
DARK_BLUE = (35, 31, 60)
GREEN = (0, 255, 0)
fon_verh = pygame.image.load('Rus\\Verh.png')
fon_verh_rect = fon_verh.get_rect(left=0)
anim_id = 0
anim_count = 6
error_text = ''
menu_music = True
pygame.mixer.music.load("Rus\\menu_music.mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.2)
game_music = True
game_music_index = 0

fon_nuz = pygame.image.load('Rus\\Nuz.png')
fon_nuz_rect = fon_nuz.get_rect(left=0)
CLOCK = pygame.time.Clock()
font = pygame.font.Font(None, 30)
logo_font = pygame.font.SysFont('Times New Roman', 80)

canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Knight’s movement')


class Flames:
    def __init__(self):
        self.flames = pygame.image.load('Rus\\fire_ball.png')
        self.flames_img = pygame.transform.scale(self.flames, (20, 20))
        self.flames_img_rect = self.flames_img.get_rect()
        self.flames_img_rect.right = dragon.dragon_img_rect.left
        self.flames_img_rect.top = dragon.dragon_img_rect.top + 50
    def update(self, speed):
        canvas.blit(self.flames_img, self.flames_img_rect)
        if self.flames_img_rect.left > 0:
            self.flames_img_rect.left -= speed


def shopLoop():
    global error_text
    from shop import Shop
    shop = Shop()
    items = shop.items

    back = pygame.image.load("Rus\\back.png")
    back_rect = back.get_rect()
    items_x = 400
    items_y = 50
    effect_list = []

    button_list = []
    balance = font.render("Coins: " + str(shop.getBalance()), 1, (0, 0, 0))
    canvas.fill((236, 204, 43))
    while True:
        canvas.blit(back, back_rect)
        for item in items:
            if items_x >= 150 * 5 + 400:
                items_x = 400
                items_y += 250
            # Кнопки
            if item['inShop'] == '1':
                locals().update({'button{}'.format(item['id']): pygame.image.load("Rus\\buy_button.png")})
                locals().update({'button{}_rect'.format(item['id']): eval("button{}".format(item['id'])).get_rect(top=items_y + 180, right=items_x+60)})
            elif item['file'] == shop.getSkin() or item['file'] == shop.getEffect():
                if item['file'] == shop.getSkin():
                    locals().update({'button{}'.format(item['id']): pygame.transform.scale(pygame.image.load("Rus\\selected.png"), [140, 15])})
                    locals().update({'button{}_rect'.format(item['id']): eval("button{}".format(item['id'])).get_rect(top=items_y + 180, right=items_x+120)})
                if item['file'] == shop.getEffect():
                    locals().update({'button{}'.format(item['id']): pygame.transform.scale(pygame.image.load("Rus\\selected.png"), [140, 15])})
                    locals().update({'button{}_rect'.format(item['id']): eval("button{}".format(item['id'])).get_rect(top=items_y + 180, right=items_x+120)})
            else:
                locals().update({'button{}'.format(item['id']): pygame.image.load("Rus\\equip_button.png")})
                locals().update({'button{}_rect'.format(item['id']): eval("button{}".format(item['id'])).get_rect(top=items_y + 180, right=items_x+60)})
            canvas.blit(font.render("Price: " + str(shop.find(item["id"], 'price')), 1, (0, 0, 0)), [items_x, items_y + 150])
            button_list.append([eval("button{}_rect".format(item['id'])), item['id'], item['inShop'], item['type'], item['file'] == shop.getEffect()])
            # Позиції магазину
            if item['type'] == 'skin':
                canvas.blit(pygame.transform.scale(pygame.image.load("Rus\\{}".format(item['file'])), (112, 150)), [items_x, items_y])
            elif item['type'] == 'effect':
                path = 'Rus/' + item['file'] + '/'
                effect_anim_count = len([f for f in os.listdir(path)
                                            if os.path.isfile(os.path.join(path, f))])
                locals().update({"effect{}".format(item['id']): Effect(path, effect_anim_count, items_x, items_y)})
                effect_list.append(eval("effect{}".format(item['id'])))

            canvas.blit(eval("button{}".format(item['id'])), eval("button{}_rect".format(item['id'])))
            items_x += 150
            items.remove(item)
        for i in effect_list:
            i.update(canvas, 1, True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_rect.collidepoint(pygame.mouse.get_pos()):
                    start_game()
                    break
                for button in button_list:
                    if button[0].collidepoint(pygame.mouse.get_pos()):
                        if button[2] == '1':
                            result = shop.buy(button[1])
                            if not result:
                                error_text = 'Not enough money'
                        else:
                            if button[3] == 'skin':
                                shop.setSkin(button[1])
                            elif button[2] == '0' and button[4]:
                                shop.setEffect('none')
                            else:
                                shop.setEffect(button[1])
                        shopLoop()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start_game()
                    break
        canvas.blit(font.render(error_text, 1, (248, 0, 0)), [20, 130])
        canvas.blit(balance, [20, 100])
        pygame.display.update()
        CLOCK.tick(FPS)


def start_game():
    global error_text, fileManager, menu_music, WINDOW_WIDTH
    if menu_music == 'repeat':
        menu_music = True
        pygame.mixer.music.load("Rus\\menu_music.mp3")
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.2)
        index = 0
    logo = logo_font.render('Knight`s movement', 1, (255, 255, 0))
    index = 0
    dynamic_on = pygame.transform.scale(pygame.image.load("Rus\\sound_on.png"), [160, 43])
    dynamic_off = pygame.transform.scale(pygame.image.load("Rus\\sound_off.png"), [160, 43])
    sound_buttons = [dynamic_on, dynamic_off]
    dynamic = dynamic_on.get_rect()
    error_text = ''
    canvas.fill((245, 245, 245))

    canvas.blit(BackGround.image, BackGround.rect)
    # background = pygame.transform.scale(pygame.image.load("Rus\\menu_background.png"), [WINDOW_WIDTH, WINDOW_HEIGHT])
    # canvas.blit(background, [0, 0])
    start_img = pygame.transform.scale(pygame.image.load('Rus//start_button.png'), [220, 62])
    start_img_rect = start_img.get_rect()
    start_img_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
    dynamic.top = start_img_rect.bottom + 40
    dynamic.left = start_img_rect.left + 30
    canvas.blit(start_img, start_img_rect)
    shop_button = pygame.image.load("Rus\\shop_button.png")
    shop_button_rect = shop_button.get_rect()
    canvas.blit(shop_button, shop_button_rect)
    if fileManager.find("game.csv", "hight_score")[0] != '0':
        hight_score = font.render("Your hight score: " + str(fileManager.find("game.csv", "hight_score")[0]), 1, (240, 0, 0))
    else:
        hight_score = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if shop_button_rect.collidepoint(pygame.mouse.get_pos()):
                    shopLoop()
                    break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_img_rect.collidepoint(pygame.mouse.get_pos()):
                    game_loop()
                if dynamic.collidepoint(pygame.mouse.get_pos()):
                    menu_music = not menu_music
                    if menu_music == False:
                        pygame.mixer.music.pause()
                        index = 1
                    else:
                        pygame.mixer.music.unpause()
                        index = 0
        canvas.blit(sound_buttons[index], dynamic)
        if hight_score != False:
            canvas.blit(hight_score, [start_img_rect.left, start_img_rect.top - 40])
        canvas.blit(logo, [start_img_rect.left - 200, start_img_rect.top - 150])
        pygame.display.update()

def game_over():
    global fileManager, menu_music, PAUSED, game_music_index
    game_over_img = pygame.transform.scale(pygame.image.load('Rus//lose.png'), [350, 312])
    game_over_img_rect = game_over_img.get_rect()
    game_over_img_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50)
    canvas.blit(game_over_img, game_over_img_rect)
    last_score = int(fileManager.find("game.csv", 'last_score')[0])
    hight_score = int(fileManager.find("game.csv", 'hight_score')[0])
    new_record = False
    if hight_score > last_score:
        last_score = font.render("Your score: " + str(last_score), 1, (255, 240, 0))
        hight_score = font.render("Congratulation! Your hight score: " + str(hight_score), 1, (255, 0, 0))
    else:
        new_record = font.render("Your new hight score: " + str(hight_score), 1, (255, 0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    menu_music = 'repeat'
                    PAUSED = not PAUSED
                    game_music_index = 0
                    start_game()
        if new_record != False:
            canvas.blit(new_record, [450, 120])
        else:
            canvas.blit(last_score, [450, 120])
            canvas.blit(hight_score, [450, 150])

        pygame.display.update()

def you_win():
    global  PAUSED, menu_music, game_music_index
    game_over_img = pygame.image.load('Rus//win.png')
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
                    pygame.mixer.music.stop()
                    menu_music = 'repeat'
                    PAUSED = not PAUSED
                    game_music_index = 0
                    start_game()

        pygame.display.update()


def level(SCORE, change = False):
    global LEVEL, rand_level
    if SCORE in range(0, 10):
        fon_verh_rect.bottom = 50
        fon_nuz_rect.top = WINDOW_HEIGHT - 50
        if not change:
            LEVEL = 1
        else:
            LEVEL += 1
            rand_level = 1

    elif SCORE in range(30, 60):
        fon_verh_rect.bottom = 100
        fon_nuz_rect.top = WINDOW_HEIGHT - 100
        if not change:
            LEVEL = 2
        else:
            LEVEL += 1
            rand_level = 2

    elif SCORE in range(60, 100):
        fon_verh_rect.bottom = 150
        fon_nuz_rect.top = WINDOW_HEIGHT - 150
        if not change:
            LEVEL = 3
        else:
            LEVEL += 1
            rand_level = 3


    elif SCORE in range(100, 200):
        fon_verh_rect.bottom = 180
        fon_nuz_rect.top = WINDOW_HEIGHT - 180
        if not change:
            LEVEL = 4
        else:
            LEVEL += 1
            rand_level = 4
    if SCORE >= 200:
        you_win()
    # if LEVEL == 4 and not change:
    #     LEVEL = 5
    fileManager.write({"last_score": SCORE}, "game.csv",)
    if (SCORE > int(fileManager.find("game.csv", 'hight_score')[0])):
        fileManager.write({"hight_score": SCORE}, "game.csv")
    if (str(SCORE)[-1] == '0' and SCORE != 0):
        fileManager.addCoin()


def draw_live_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, (255, 255, 255), outline_rect, 2)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, (0,0,255), fill_rect)
    pygame.draw.rect(surf, (255, 255, 255), outline_rect, 2)

def draw_pause_screen(canvas):
    global PAUSED
    global game_music, game_music_index, menu_music
    surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCCOLORKEY, 24)
    surf.blit(pygame.image.load("Rus\\pause_fon.jpg"), BackGround.rect)
    menu_btn = pygame.transform.scale(pygame.image.load("Rus\\menu_button.png"), [160, 43])
    menu_btn_rect = menu_btn.get_rect()
    menu_btn_rect.left = WINDOW_WIDTH // 2 - 105
    menu_btn_rect.top = WINDOW_HEIGHT // 2 - 150
    dynamic_on = pygame.transform.scale(pygame.image.load("Rus\\sound_on.png"), [160, 43])
    dynamic_off = pygame.transform.scale(pygame.image.load("Rus\\sound_off.png"), [160, 43])
    sound_buttons = [dynamic_on, dynamic_off]
    dynamic = dynamic_on.get_rect()
    dynamic.top = menu_btn_rect.bottom + 25
    dynamic.left = menu_btn_rect.left

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            PAUSED = not PAUSED
            menu_music = 'repeat'
            game_music_index = 0
            start_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                PAUSED = not PAUSED
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if dynamic.collidepoint(pygame.mouse.get_pos()):
                game_music = not game_music
                if game_music == False:
                    pygame.mixer.music.pause()
                    game_music_index = 1
                else:
                    pygame.mixer.music.unpause()
                    game_music_index = 0
            if menu_btn_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.mixer.music.stop()
                menu_music = 'repeat'
                PAUSED = not PAUSED
                game_music_index = 0
                start_game()

    surf.blit(sound_buttons[game_music_index], dynamic)
    surf.blit(menu_btn, menu_btn_rect)
    canvas.blit(surf, (0, 0))


def game_loop():
        import dragon_class
        import knight_class
        global dragon
        global anim_count
        global anim_id
        global menu_music, game_music
        global PAUSED

        pygame.mixer.music.stop()
        dragon = dragon_class.Dragon(WINDOW_HEIGHT, WINDOW_WIDTH)
        knight = knight_class.Knight()
        flames_list = []
        pygame.mixer.music.load('Rus//muz.mp3')
        pygame.mixer.music.play(-1, 0.0)

        add_new_flame_counter=0
        SCORE = 0
        new_flame_delay = 15
        while True:
            canvas.fill([255, 255, 255])
            canvas.blit(BackGround.image, BackGround.rect)

            fon_verh_rect.bottom = 50
            fon_nuz_rect.top = WINDOW_HEIGHT - 50
            level(SCORE)
            rand_level = 0
            if not PAUSED:
                add_new_flame_counter += 1

                if add_new_flame_counter == new_flame_delay: #визначає протяжність часу протягом якого буде запускатись вогонь
                    add_new_flame_counter = 0
                    new_flame = Flames()
                    flames_list.append(new_flame)
                for f in flames_list:
                    if f.flames_img_rect.left <= 0:
                        flames_list.remove(f)
                        SCORE += 1
                    if LEVEL == 1:
                        f.update(10)
                    elif LEVEL == 2:
                        new_flame_delay = 15
                        f.update(15)
                    elif LEVEL == 3:
                        new_flame_delay = 25
                        f.update(20)
                    elif LEVEL == 4 :
                        new_flame_delay = 35
                        f.update(20)
                    # else:
                    #     levels = [5, 35, 65, 105]
                    #     selected_level = random.choice(levels)
                    #     level(selected_level, True)
                    #     if selected_level == 5:
                    #         new_flame_delay = 15
                    #         f.update(10)
                    #     elif selected_level == 35:
                    #         new_flame_delay = 15
                    #         f.update(15)
                    #     elif selected_level == 65:
                    #         new_flame_delay = 25
                    #         f.update(20)
                    #     elif selected_level == 105:
                    #         new_flame_delay = 35
                    #         f.update(25)
            if not PAUSED:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            PAUSED = not PAUSED
                        if not PAUSED:
                            if event.key == pygame.K_UP:
                                knight.up = True
                                knight.down = False
                            elif event.key == pygame.K_DOWN:
                                knight.down = True
                                knight.up = False
                    if not PAUSED:
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_UP:
                                knight.up = False
                                knight.down = True
                            elif event.key == pygame.K_DOWN:
                                knight.down = True
                                knight.up = False
            for f in flames_list:
                if f.flames_img_rect.colliderect(knight.knight_img_rect):
                    knight.damage(1)
            if knight.life <= 0:
                game_over()
            if knight.shield != False:
                draw_shield_bar(canvas, fon_verh_rect.left + 50, fon_verh_rect.bottom + 75, knight.shield)
            draw_live_bar(canvas, fon_verh_rect.left + 50, fon_verh_rect.bottom + 55, knight.life)

            score_font = font.render('Fireballs:' + str(SCORE), True, GREEN)
            canvas.blit(score_font, (100, fon_verh_rect.bottom + 30))

            level_font = font.render('Level:' + str(LEVEL), True, GREEN)
            canvas.blit(level_font, (245, fon_verh_rect.bottom + 30))
            canvas.blit(fon_verh, fon_verh_rect)
            canvas.blit(fon_nuz, fon_nuz_rect)
            if not PAUSED:
                knight.update(canvas, fon_verh_rect, fon_nuz_rect)
                dragon.update(canvas, fon_verh_rect, fon_nuz_rect, anim_id)
                if anim_id == 7:
                    anim_id = 0
                else:
                    if anim_count == 0:
                        anim_id += 1
                        anim_count = 6
                    elif anim_count > 0:
                        anim_count -= 1
            if PAUSED:
                draw_pause_screen(canvas)
            pygame.display.update()
            CLOCK.tick(FPS)


start_game()

