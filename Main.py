import pygame
import sys
import files

fileManager = files.fileManager()
pygame.init()

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

fon_nuz = pygame.image.load('Rus\\Nuz.png')
fon_nuz_rect = fon_nuz.get_rect(left=0)
CLOCK = pygame.time.Clock()
font = pygame.font.Font(None, 30)

canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Лицарський двіж')




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
            self.flames_img_rect.left-=10



def shopLoop():
    global error_text
    from shop import Shop
    back = pygame.image.load("Rus\\back.png")
    back_rect = back.get_rect()
    shop = Shop()
    canvas.fill((236, 204, 43))
    items = shop.items
    items_x = 400
    items_y = 50
    button_list = []
    balance = font.render("Ваш баланс: " + str(shop.getBalance()), 1, (0, 0, 0))
    while True:
        canvas.blit(back, back_rect)
        for item in items:
            if items_x >= 150 * 4 + 400:
                items_x = 400
                items_y += 250
            if item['inShop'] == '1':
                locals().update({'button{}'.format(item['id']): pygame.image.load("Rus\\buy_button.png")})
                locals().update({'button{}_rect'.format(item['id']): eval("button{}".format(item['id'])).get_rect(top=items_y + 180, right=items_x+60)})
            elif item['file'] == shop.getSkin():
                locals().update({'button{}'.format(item['id']): pygame.transform.scale(pygame.image.load("Rus\\selected.png"), [140, 15])})
                locals().update({'button{}_rect'.format(item['id']): eval("button{}".format(item['id'])).get_rect(top=items_y + 180, right=items_x+120)})
            else:
                locals().update({'button{}'.format(item['id']): pygame.image.load("Rus\\equip_button.png")})
                locals().update({'button{}_rect'.format(item['id']): eval("button{}".format(item['id'])).get_rect(top=items_y + 180, right=items_x+60)})
            canvas.blit(font.render("Ціна: " + str(shop.find(item["id"], 'price')), 1, (0, 0, 0)), [items_x, items_y + 150])
            button_list.append([eval("button{}_rect".format(item['id'])), item['id'], item['inShop']])
            canvas.blit(pygame.transform.scale(pygame.image.load("Rus\\{}".format(item['file'])), (112, 150)), [items_x, items_y])
            canvas.blit(eval("button{}".format(item['id'])), eval("button{}_rect".format(item['id'])))
            items_x += 150
            items.remove(item)

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
                                error_text = 'Недостатня кількість монет'
                        else:
                            shop.setSkin(button[1])
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
    global error_text
    error_text = ''
    canvas.fill((245, 245, 245))
    start_img = pygame.image.load('Rus//start.png')
    start_img_rect = start_img.get_rect()
    start_img_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
    canvas.blit(start_img, start_img_rect)
    shop_button = pygame.image.load("Rus\\shop_button.png")
    shop_button_rect = shop_button.get_rect()
    canvas.blit(shop_button, shop_button_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if shop_button_rect.collidepoint(pygame.mouse.get_pos()):
                    shopLoop()
                    break
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
                break
        pygame.display.update()

def level(SCORE):
    global LEVEL
    if SCORE in range(0, 10):
        fon_verh_rect.bottom = 50
        fon_nuz_rect.top = WINDOW_HEIGHT - 50
        LEVEL = 1
    elif SCORE in range(30, 60):
        fon_verh_rect.bottom = 100
        fon_nuz_rect.top = WINDOW_HEIGHT - 100
        LEVEL = 2
    elif SCORE in range(60, 100):
        fon_verh_rect.bottom = 150
        fon_nuz_rect.top = WINDOW_HEIGHT - 150
        LEVEL = 3
    elif SCORE in range(100, 180):
        fon_verh_rect.bottom = 200
        fon_nuz_rect.top = WINDOW_HEIGHT - 200
        LEVEL = 4
    fileManager.write({"last_score": SCORE}, "game.csv",)
    if (SCORE > int(fileManager.find("game.csv", 'hight_score')[0])):
        fileManager.write({"hight_score": SCORE}, "game.csv")
    if (str(SCORE)[-1] == '0' and SCORE != 0):
        fileManager.addCoin()

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

BackGround = Background('Rus\\fon.jpg', [0,0])

def game_loop():
        import dragon_class
        import knight_class
        global dragon
        global anim_count
        global anim_id
        dragon = dragon_class.Dragon(WINDOW_HEIGHT, WINDOW_WIDTH)
        knight = knight_class.Knight()
        flames = Flames()
        flames_list = []
        pygame.mixer.music.load('Rus//muz.mp3')
        pygame.mixer.music.play(-1, 0.0)

        add_new_flame_counter=0
        popav=100
        SCORE=0
        while True:
            canvas.fill([255, 255, 255])
            canvas.blit(BackGround.image, BackGround.rect)
            fon_verh_rect.bottom = 50
            fon_nuz_rect.top = WINDOW_HEIGHT - 50
            level(SCORE)
            add_new_flame_counter += 1
            if add_new_flame_counter == 25: #визначає протяжність часу протягом якого буде запускатись вогонь
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
            pygame.display.update()
            CLOCK.tick(FPS)


start_game()

