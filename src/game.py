import pygame
from func import load_image, show_image, terminate
from func import map_generation


def interface():
    images = [['coin', 1330, 105, 70, 70], ['magic_frame', 1335, 860, 120, 120],
              ['magic_frame', 1495, 860, 120, 120], ['weapon_frame', 300, 860, 125, 125],
              ['weapon_frame', 470, 860, 125, 125], ['unfilled_HP', 605, 860, 720, 125],
              ['mana_bar', 300, 100, 60, 80], ['field_for_coin', 1420, 110, 200, 60],
              ['field_for_coin', 370, 110, 250, 60]]

    fon = load_image('background.png', 'interface')
    fon = pygame.transform.scale(fon, (1920, 1080)) 
    screen_game.blit(fon, (0, 0))

    pygame.draw.rect(screen_game, pygame.Color('black'), (275, 185, 1365, 670))
    pygame.draw.rect(screen_game, pygame.Color('white'), (280, 190, 1355, 660))

    for i in images:
        show_image(i, screen_game, 'interface')


def update_hp_mana_coins(*hp_states, **characteristics):
    coin_font = pygame.font.Font('data/shrifts/coins_shrift.ttf', 50)
    coin_text = coin_font.render(str(characteristics['coins']), False, (20, 20, 20))
    screen_game.blit(coin_text, (1475, 110))

    magic_font = pygame.font.Font('data/shrifts/coins_shrift.ttf', 50)
    magic_text = magic_font.render(f'{str(characteristics['mana'])}', 
                                   False, (20, 20, 20))
    screen_game.blit(magic_text, (395, 110))
    magic_text = magic_font.render(f'/{str(characteristics['unlocked_mana'])}', 
                                   False, (20, 20, 20))
    screen_game.blit(magic_text, (485, 110))

    for i in range(characteristics['hp']):
        hp_states[0][1] = 643 + i * 64
        show_image(hp_states[0], screen_game, 'interface')

    for i in range(10 - characteristics['hp']):
        hp_states[1][1] = 1219 - i * 64
        show_image(hp_states[1], screen_game, 'interface')

    for i in range(10 - characteristics['unlocked_hp']):
        hp_states[2][1] = 1235 - i * 64
        show_image(hp_states[2], screen_game, 'interface')



class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x_player = 900
        self.y_player = 480

        self.width_player = 100
        self.height = 120
        self.speed = 10

        self.animation_flag = False
        self.time_animation = 0
        self.side_animation = 'right'
        self.walk_animation = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if self.y_player - self.speed >= 190:
                self.y_player -= self.speed
                self.animation_flag = True
        elif keys[pygame.K_s]:
            if self.y_player + self.height + self.speed <= 765:
                self.y_player += self.speed
                self.animation_flag = True
        elif keys[pygame.K_a]:
            if self.x_player - self.speed >= 350:
                self.x_player -= self.speed
                self.animation_flag = True
                self.side_animation = 'left'
        elif keys[pygame.K_d]:
            if self.x_player + self.width_player + self.speed <= 1550:
                self.x_player += self.speed
                self.animation_flag = True
                self.side_animation = 'right'
        else:
            self.form = [f'main_hero_{self.side_animation}_stop', self.x_player, self.y_player, self.width_player, 120]
            self.animation_flag = False
            self.time_animation = 0

        if self.animation_flag:
            self.form = [f'main_hero_{self.side_animation}_walk_{self.walk_animation}', self.x_player, self.y_player, self.width_player, 120]
            if self.time_animation == 4:
                        self.walk_animation = (self.walk_animation + 1) % 4
            self.time_animation = (self.time_animation + 1) % 5

        show_image(self.form, screen_game, 'characters/main_hero')


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)


def start():
    global screen_game
    pygame.init()
    screen_game = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('Infinity Castle')

    FPS = 60
    clock = pygame.time.Clock()
    
    characteristics = {'coins': 0,
                       'hp': 4,
                       'unlocked_hp': 4,
                       'mana': 50,
                       'unlocked_mana': 50}
    
    hp_states = [['filled_cell_HP', 643, 897, 60, 52], 
                 ['unfilled_cell_HP', 1219, 897, 60, 52],
                 ['loced_HP', 1235, 903, 30, 40]]

    em_room = ['empty_room', 280, 190, 1355, 660]
    

    map_generation(level=1, map_size=4)
    interface()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()

        show_image(em_room, screen_game, 'map')        

        update_hp_mana_coins(*hp_states, **characteristics)
        all_sprites.update()

        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()
