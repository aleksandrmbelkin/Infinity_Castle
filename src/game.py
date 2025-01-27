import pygame
import os
from func import load_image, show_image, terminate
from func import map_generation


def interface():
    images = [['coin', 1330, 105, 70, 70], ['magic_frame', 1335, 860, 120, 120],
              ['magic_frame', 1495, 860, 120, 120], [
                  'weapon_frame', 300, 860, 125, 125],
              ['weapon_frame', 470, 860, 125, 125], [
                  'unfilled_HP', 605, 860, 720, 125],
              ['mana_bar', 300, 100, 60, 80], [
                  'field_for_coin', 1420, 110, 200, 60],
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
    coin_text = coin_font.render(
        str(characteristics['coins']), False, (20, 20, 20))
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
        self.height_player = 120
        self.speed = 10

        self.animation_flag = False
        self.time_animation = 0
        self.side_animation = 'right'
        self.walk_animation = 0

        self.characteristics = {'coins': 0,
                                'hp': 4,
                                'unlocked_hp': 4,
                                'mana': 50,
                                'unlocked_mana': 50}

        self.hp_states = [['filled_cell_HP', 643, 897, 60, 52],
                          ['unfilled_cell_HP', 1219, 897, 60, 52],
                          ['loced_HP', 1235, 903, 30, 40]]

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if self.y_player - self.speed >= 190:
                self.y_player -= self.speed
                self.animation_flag = True
        elif keys[pygame.K_s]:
            if self.y_player + self.height_player + self.speed <= 765:
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
            self.form = [f'{self.side_animation}/stop',
                         self.x_player, self.y_player, self.width_player, 120]
            self.animation_flag = False
            self.time_animation = 0

        if self.animation_flag:
            self.form = [f'{self.side_animation}/walk_{self.walk_animation}',
                         self.x_player, self.y_player, self.width_player, 120]
            if self.time_animation == 2:
                self.walk_animation = (self.walk_animation + 1) % 8
            self.time_animation = (self.time_animation + 1) % 3

        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_f:
                    if self.x_player + self.width_player >= 1500 and 400 < self.y_player < 560:
                        can = room.change_room_number('right')
                        if can:
                            self.x_player = 350
                    elif self.x_player <= 400 and 400 < self.y_player < 550:
                        can = room.change_room_number('left')
                        if can:
                            self.x_player = 1550 - self.width_player
                    elif self.y_player + self.height_player >= 715 and 840 < self.x_player < 1000:
                        can = room.change_room_number('down')
                        if can:
                            self.y_player = 190
                    elif self.y_player <= 240 and 840 < self.x_player < 1000:
                        can = room.change_room_number('up')
                        if can:
                            self.y_player = 765 - self.height_player

        update_hp_mana_coins(*self.hp_states, **self.characteristics)
        show_image(self.form, screen_game, 'characters/main_hero')


class Room():
    def __init__(self, map_list, room_number):
        self.em_room = ['empty_room', 280, 190, 1355, 660]
        self.room_number = room_number
        self.map_list = map_list
        self.map_size = len(map_list)

    def create(self):
        show_image(self.em_room, screen_game, 'map')

    def change_room_number(self, where):
        can = False

        if where == 'up':
            if (self.room_number[0] - 1 >= 0 and
                    self.map_list[self.room_number[0] - 1][self.room_number[1]][0] != 'no'):
                self.room_number[0] -= 1
                can = True
        elif where == 'down':
            if (self.room_number[0] + 1 < self.map_size and
                    self.map_list[self.room_number[0] + 1][self.room_number[1]][0] != 'no'):
                self.room_number[0] += 1
                can = True
        elif where == 'left':
            if (self.room_number[1] - 1 >= 0 and
                    self.map_list[self.room_number[0]][self.room_number[1] - 1][0] != 'no'):
                self.room_number[1] -= 1
                can = True
        elif where == 'right':
            if (self.room_number[1] + 1 < self.map_size and
                    self.map_list[self.room_number[0]][self.room_number[1] + 1][0] != 'no'):
                self.room_number[1] += 1
                can = True

        print(self.room_number)
        return can


def start():
    global screen_game, room
    pygame.init()
    screen_game = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('Infinity Castle')

    # os.environ['SDL_VIDEO_CENTERED'] = '0'

    FPS = 60
    clock = pygame.time.Clock()

    interface()
    map_list, room_number = map_generation(level=1, map_size=4)

    for i in map_list:
        for j in i:
            print(j[0], end='|')
        print()
    print(room_number)

    # all_sprites = pygame.sprite.Group()
    player = Player()
    room = Room(map_list, room_number)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()

        room.create()
        player.update()

        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()


# Активация в тестах
if __name__ == '__main__':
    start()
