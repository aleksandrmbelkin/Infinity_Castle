import pygame
import os
from func import load_image, terminate
import time
import math
import random
from func import map_generation
from game_load import *

# Группы спрайтов
all_borders = pygame.sprite.Group()
all_objects = pygame.sprite.Group()
button_pause = pygame.sprite.Group()
pause_group = pygame.sprite.Group()
attack_group = pygame.sprite.Group()
magic_group = pygame.sprite.Group()
usual_skeletons_group = pygame.sprite.Group()
attack_usual_skeleton_group = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
items_group = pygame.sprite.Group()
items_this_room_group = pygame.sprite.Group()

FIGHT = False
CANFIRE = True
CANMELEE = True

DIFFICULTY_MULTY = 1.0
OBJECTS = {}
images = [['coin', 1330, 105, 70, 70], ['magic_frame', 1335, 860, 120, 120],
          ['magic_frame', 1495, 860, 120, 120], [
              'weapon_frame', 300, 860, 125, 125],
          ['weapon_frame', 470, 860, 125, 125], [
              'unfilled_HP', 605, 860, 720, 125],
          ['mana_bar', 300, 100, 60, 80], [
              'field_for_coin', 1420, 110, 200, 60],
          ['field_for_coin', 370, 110, 250, 60]]


# Загрузка данных из настроек
def load_settings(channels):
    global SETTINGS
    # загрузка настроек из файла
    # SETTINGS = ['sound 1', 'musik 1', 'forward w', 'left a', 'down s', 'right d', 'melee_weapon q', 'magic_weapon e',
    #             'interaction f', 'menu esc']

    test = open('settings.txt')
    test.seek(0)
    SETTINGS = {}
    for i in test.readlines():
        line = (i.strip().split())
        SETTINGS[line[0]] = line[1]
    test.close()

    if SETTINGS['sound'] == '1':
        for i in range(1, channels + 1):
            pygame.mixer.Channel(i).set_volume(1)
    else:
        for i in range(1, channels + 1):
            pygame.mixer.Channel(i).set_volume(0)
    if SETTINGS['musik'] == '1':
        pygame.mixer.music.set_volume(0.25)
    else:
        pygame.mixer.music.set_volume(0)


# Создание и выведение на экран интерфейса
def interface():
    fon = load_image('background.png', 'interface')
    fon = pygame.transform.scale(fon, (1920, 1080))
    screen_game.blit(fon, (0, 0))

    pygame.draw.rect(screen_game, pygame.Color('black'), (275, 185, 1365, 670))
    pygame.draw.rect(screen_game, pygame.Color('white'), (280, 190, 1355, 660))

    for image in images:
        im = load_image(f'{image[0]}.png', 'interface')
        im = pygame.transform.scale(im, (image[3], image[4]))
        screen_game.blit(im, (image[1], image[2]))


# Обновление изменяемых характеристик героя
def update_hp_mana_coins(**characteristics):
    screen_game.blit(field_for_coin_short, (1420, 110))
    screen_game.blit(field_for_coin_long, (370, 110))

    coin_font = pygame.font.Font('data/shrifts/coins_shrift.ttf', 50)
    coin_text = coin_font.render(
        str(characteristics['coins']), False, (20, 20, 20))
    screen_game.blit(coin_text, (1475, 110))

    magic_font = pygame.font.Font('data/shrifts/coins_shrift.ttf', 50)
    magic_text = magic_font.render(f'{str(characteristics["mana"])}',
                                   False, (20, 20, 20))
    screen_game.blit(magic_text, (395, 110))

    magic_text = magic_font.render(f'/{str(characteristics["unlocked_mana"])}',
                                   False, (20, 20, 20))
    screen_game.blit(magic_text, (485, 110))

    for i in range(characteristics['hp']):
        hp_states_0_x = 643 + i * 64
        screen_game.blit(hp_states[0], (hp_states_0_x, 897))

    for i in range(10 - characteristics['hp']):
        hp_states_1_x = 1219 - i * 64
        screen_game.blit(hp_states[1], (hp_states_1_x, 897))

    for i in range(10 - characteristics['unlocked_hp']):
        hp_states_2_x = 1235 - i * 64
        screen_game.blit(hp_states[2], (hp_states_2_x, 903))


class Button(pygame.sprite.Sprite):

    # Класс Кнопки в общем виде
    def __init__(self, a, dx, dy, x, y, group):
        super().__init__(group)
        self.button_type = a
        self.image = load_image(self.button_type, 'main')
        self.image = pygame.transform.scale(self.image, (dx, dy))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        global running, pausing, pause_group
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            if self.button_type == 'points3.png':
                pause()
            elif self.button_type == 'continue.png':
                pausing = False
            elif self.button_type == 'menu_back.png':
                for i in pause_group:
                    i.kill()
                pygame.quit()
                os.system('python main.py')
                sys.exit()
            elif self.button_type == 'start_new_game.png':
                pygame.quit()
                os.system('python game.py')
                sys.exit()
            elif self.button_type == 'menu_back.png':
                pygame.quit()
                os.system('python main.py')
                sys.exit()
            elif self.button_type == 'game_stop.png':
                terminate()


class attack_rect(pygame.sprite.Sprite):
    def __init__(self, x, y, k, player):
        super().__init__(attack_group)
        x += 25
        x += 50 * k
        self.image = pygame.Surface((50, 100), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color('Black'), (0, 0, 50, 100))
        self.rect = pygame.Rect(x, y, 50 * k, 100)
        self.timeappear = time.process_time()


class attack_rect_usual_skeleton(pygame.sprite.Sprite):
    def __init__(self, x, y, k):
        super().__init__(attack_usual_skeleton_group)
        x += 25
        x += 40 * k
        self.image = pygame.Surface((40, 60), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color('Black'), (0, 0, 40, 60))
        self.rect = pygame.Rect(x, y, 40 * k, 60)
        self.timeappear = time.process_time()


class fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, x1, y1):
        super().__init__(magic_group)
        x += 50
        y += 50
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"), center=(10, 10), radius=10)
        self.rect = pygame.Rect(x, y, 20, 20)

        self.angle = math.atan2(y1 - y, x1 - x)
        self.speed = 20

    def update(self, *args, **kwargs):
        self.rect = self.rect.move(round(self.speed * math.cos(self.angle)), round(self.speed * math.sin(self.angle)))
        if pygame.sprite.spritecollideany(self, all_borders) or pygame.sprite.spritecollideany(self, all_objects):
            self.kill()


class usual_skeleton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(usual_skeletons_group)
        self.image = load_image('stop.png', r'characters\monsters\skeleton\usual_skeleton')
        self.x = random.randint(280, 1355)
        self.y = random.randint(190, 660)
        self.rect = pygame.Rect(self.x, self.y, 100, 100)
        self.hp = 100 * DIFFICULTY_MULTY
        self.speed = 3
        self.canmelee = True
        self.lastmelee = -1
        self.hitted = []

    def update(self, *args, **kwargs):
        global player, player_group
        if pygame.sprite.spritecollide(self, magic_group, False):
            self.hp -= player.magic1['damage']
            for i in pygame.sprite.spritecollide(self, magic_group, False):
                i.kill()
        if pygame.sprite.spritecollide(self, attack_group, False):
            i = pygame.sprite.spritecollide(self, attack_group, False)[0]
            if i not in self.hitted:
                self.hp -= player.melee1['damage']
                self.hitted.append(i)
        if pygame.sprite.spritecollideany(self, player_group) and self.canmelee:
            attack_rect_usual_skeleton(self.rect.x, self.rect.y, 1)
            self.canmelee = False
            self.lastmelee = time.process_time()
        x = player.rect.x
        y = player.rect.y
        angl = math.atan2(y - self.rect.y, x - self.rect.x)
        self.rect = self.rect.move(round(self.speed * math.cos(angl)), round(self.speed * math.sin(angl)))
        if self.hp <= 0:
            Coin(self.rect.x, self.rect.y)
            self.kill()


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_borders)
        if x1 == x2:  # вертикальная стенка
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(coins_group)
        self.image = load_image('coin.png', r'interface')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args, **kwargs):
        global player_group, player
        if pygame.sprite.spritecollide(self, player_group, False):
            self.kill()
            player.characteristics['coins'] += 1


def show_main_text(size):
    global text_tick, main_text, text_coords

    main_font = pygame.font.Font('data/shrifts/main_shrift.ttf', size)

    if text_tick < max_text_tick:
        final_main_text = main_font.render(main_text, False, (20, 20, 20))
        screen_game.blit(final_main_text, (text_coords[0], text_coords[1]))
        text_tick += 1
    else:
        main_text = ''


class Player(pygame.sprite.Sprite):
    # Инициализация начальных характеристик персонажа
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 900
        self.y = 350
        self.width = 100
        self.height = 120
        self.speed = 5

        self.animation_flag = False
        self.time_animation = 0
        self.side_animation = 'right'
        self.walk_animation = 0

        # Стандартные оружия
        self.melee1 = melee_weapons['usual_sword']
        self.magic1 = magic_weapons['usual_fireball']

        # Выбранное оружие (0 - первое, 1 - второе)
        self.melee_magic = 1

        # Последнее время атаки
        self.lastfire = -5
        self.lastmelee = -1

        # Список с задетыми хит-боксами
        self.hitted = []

        # Анимации
        self.form = f'{self.side_animation}/stop'
        self.attack_animation = ['atack_2.' + str(i) + '.png' for i in range(4)]
        print(self.form)
        self.image = load_image(f'{self.form}.png', 'characters/main_hero')
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.characteristics = {'coins': 999,
                                'hp': 4,
                                'unlocked_hp': 4,
                                'mana': 50,
                                'unlocked_mana': 50}

    def movement(self):
        # Перемещение
        keys = pygame.key.get_pressed()
        if not keys:
            return
        if keys[ord(SETTINGS['forward'])]:
            if self.rect.y - self.speed >= 190:
                self.rect.y -= self.speed
                self.animation_flag = True
                if pygame.sprite.spritecollideany(self, all_objects):
                    self.rect.y += self.speed
        if keys[ord(SETTINGS['down'])]:
            if self.rect.y + self.height + self.speed <= 765:
                self.rect.y += self.speed
                self.animation_flag = True
                if pygame.sprite.spritecollideany(self, all_objects):
                    self.rect.y -= self.speed
        if keys[ord(SETTINGS['left'])]:
            if self.rect.x - self.speed >= 350:
                self.rect.x -= self.speed
                self.animation_flag = True
                self.side_animation = 'left'
                if pygame.sprite.spritecollideany(self, all_objects):
                    self.rect.x += self.speed
        if keys[ord(SETTINGS['right'])]:
            if self.rect.x + self.width + self.speed <= 1550:
                self.rect.x += self.speed
                self.animation_flag = True
                self.side_animation = 'right'
                if pygame.sprite.spritecollideany(self, all_objects):
                    self.rect.x -= self.speed

        # Смена анимации перемещения
        if self.animation_flag:
            self.form = f'{self.side_animation}/walk_{self.walk_animation}'
            if self.time_animation == 7:
                self.walk_animation = (self.walk_animation + 1) % 7
            self.time_animation = (self.time_animation + 1) % 8

            if not pygame.mixer.Channel(sounds['steps']).get_busy():
                pygame.mixer.Channel(sounds['steps']).play(pygame.mixer.Sound(
                    'data/music_and_sounds/sounds/main_hero_sounds/steps.mp3'))
        else:
            # Анимация стояния на месте
            self.form = f'{self.side_animation}/stop'
            self.animation_flag = False
            self.time_animation = 0
            pygame.mixer.Channel(sounds['steps']).stop()

        self.animation_flag = False

    # Взаимодействия
    def action(self, event):
        if event.key == ord(SETTINGS['interaction']):
            # Двери
            can = False
            if self.rect.x >= 1440 and 400 < self.rect.y < 560:
                can = room.change_room_number('right', change=True)
                if can and not FIGHT:
                    self.rect.x = 350
            elif self.rect.x <= 360 and 400 < self.rect.y < 550:
                can = room.change_room_number('left', change=True)
                if can and not FIGHT:
                    self.rect.x = 1550 - self.width
            elif self.rect.y >= 635 and 840 < self.rect.x < 1000:
                can = room.change_room_number('down', change=True)
                if can and not FIGHT:
                    self.rect.y = 190
            elif self.rect.y <= 195 and 840 < self.rect.x < 1000:
                can = room.change_room_number('up', change=True)
                if can and not FIGHT:
                    self.rect.y = 765 - self.height

            if can:
                for i in magic_group:
                    i.kill()
                for i in usual_skeletons_group:
                    i.kill()
                for i in attack_group:
                    i.kill()
                for i in coins_group:
                    i.kill()
                for i in items_this_room_group:
                    i.remove(items_this_room_group)
                if room.this_room[0] in OBJECTS:
                    for i in OBJECTS[room.this_room[0]]:
                        items_this_room_group.add(i)

            # Сундук
            if room.this_room[0] == 'chest':
                if 770 < self.rect.x < 1100 and 320 < self.rect.y < 630:
                    chest.animation_flag = True
                    if map_list[room.room_number[0]][room.room_number[1]][1] != 'used':
                        if not pygame.mixer.Channel(sounds['diffrent']).get_busy():
                            pygame.mixer.Channel(sounds['diffrent']).play(pygame.mixer.Sound(
                                'data/music_and_sounds/sounds/map_sounds/chest_open.mp3'))

            # Стартовая комната 1 уровня
            elif room.this_room[0] == 'door_start':
                if self.rect.y <= 195 and 840 < self.rect.x < 1000:
                    main_text = 'Пути назад уже нет'
                    text_tick = 0
                    max_text_tick = 100
                    text_size = 50
                    text_coords = [710, 110]

            # Конечная комната
            elif room.this_room[0] == 'end':
                if self.rect.x >= 1240 and self.rect.y < 325:
                    br = False
                    visited = False
                    for i in range(len(map_list)):
                        for j in range(len(map_list[i])):
                            if map_list[i][j][2] == 'unvisited' and map_list[i][j][0] != 'no':
                                br = True
                                break
                        if br:
                            break
                    else:
                        visited = True

                    if visited:
                        global level
                        level += 1
                        start()
                    else:
                        main_text = 'Нужно проверить все комнаты'
                        text_tick = 0
                        max_text_tick = 120
                        text_size = 45
                        text_coords = [630, 110]


            # Аркадная комната
            elif room.this_room[0] == 'arcada':
                if 790 < self.rect.x < 1065 and 285 < self.rect.y < 620:
                    if not pygame.mixer.Channel(sounds['diffrent']).get_busy() and not pygame.mixer.Channel(
                            sounds['diffrent']).get_busy():
                        if player.characteristics['coins'] < 10:
                            main_text = 'У вас недостаточно средств!'
                            text_tick = 0
                            max_text_tick = 120
                            text_size = 45
                            text_coords = [650, 110]

                        else:
                            player.characteristics['coins'] -= 10

                            chance = random.random()
                            if chance < 0.65:
                                pygame.mixer.Channel(sounds['diffrent']).play(
                                    pygame.mixer.Sound('data/music_and_sounds/sounds/map_sounds/automat/loss.mp3'))
                                main_text = 'Упс, не повезло!'
                                text_tick = 0
                                max_text_tick = 50
                                text_size = 55
                                text_coords = [770, 110]
                            else:
                                pygame.mixer.Channel(sounds['diffrent']).play(
                                    pygame.mixer.Sound('data/music_and_sounds/sounds/map_sounds/automat/victory.mp3'))
                                main_text = 'Вы выиграли!'
                                text_tick = 0
                                max_text_tick = 150
                                text_size = 55
                                text_coords = [790, 110]

                                if 0.55 <= chance < 0.7:
                                    pass  # 30 монет
                                if 0.7 <= chance < 0.8:
                                    pass  # Оружие
                                if 0.8 <= chance < 0.9:
                                    pass  # Магия
                                if 0.9 <= chance < 1:
                                    pass  # Зелье

            # Комната жизни
            elif room.this_room[0] == 'life_room':
                if map_list[room.room_number[0]][room.room_number[1]][1] != 'used':
                    if ((395 <= self.rect.x <= 605 and 430 <= self.rect.y <= 565) or
                            (590 <= self.rect.x <= 810 and 190 <= self.rect.y <= 325) or
                            (800 <= self.rect.x <= 1010 and 445 <= self.rect.y <= 565)):

                        map_list[room.room_number[0]][room.room_number[1]][1] = 'used'
                        chance = random.random()

                        if chance < 0.33:
                            if chance < 0.16:
                                player.characteristics['unlocked_mana'] += 25
                                player.characteristics['mana'] += 25
                            elif 0.16 <= chance < 0.33:
                                if player.characteristics['unlocked_hp'] + 1 <= 10:
                                    player.characteristics['unlocked_hp'] += 1
                                    player.characteristics['hp'] += 1

                            main_text = 'Повезло...'
                            text_tick = 0
                            max_text_tick = 100
                            text_size = 55
                            text_coords = [860, 110]

                        else:
                            if 0.33 <= chance < 0.66:
                                if player.characteristics['unlocked_mana'] - 25 >= 0:
                                    player.characteristics['unlocked_mana'] -= 25
                                    if player.characteristics['mana'] > player.characteristics['unlocked_mana']:
                                        player.characteristics['mana'] = player.characteristics['unlocked_mana']
                            elif 0.66 <= chance <= 1:
                                player.characteristics['unlocked_hp'] -= 1
                                if player.characteristics['hp'] > player.characteristics['unlocked_hp']:
                                    player.characteristics['hp'] = player.characteristics['unlocked_hp']

                            main_text = 'Не повезло)'
                            text_tick = 0
                            max_text_tick = 100
                            text_size = 55
                            text_coords = [840, 110]

                        pygame.mixer.Channel(sounds['diffrent']).play(pygame.mixer.Sound(
                            'data/music_and_sounds/sounds/map_sounds/storm.mp3'))

        elif event.key == pygame.K_z:
            print(self.rect.x, self.rect.y)

    def attack(self, event):
        global CANFIRE, CANMELEE
        if self.side_animation == 'right':
            k = 1
        else:
            k = -1
        if self.melee_magic == 0:
            if CANMELEE:
                self.melee1['hitbox_type'](self.rect.x, self.rect.y, k, self)
                CANMELEE = False
                self.lastmelee = time.process_time()

        else:
            if CANFIRE and self.characteristics['mana'] >= self.magic1['mana']:
                self.magic1['type'](self.rect.x, self.rect.y, event.pos[0], event.pos[1])
                CANFIRE = False
                self.characteristics['mana'] -= self.magic1['mana']
                self.lastfire = time.process_time()

    # Обновление изменяемых характеристик и картинки героя
    def update(self):
        update_hp_mana_coins(**self.characteristics)
        if not CANMELEE:
            if self.side_animation == 'right':
                self.image = load_image(self.attack_animation[self.anim], r'characters\main_hero\right')
            else:
                self.image = load_image(self.attack_animation[self.anim], r'characters\main_hero\left')
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.anim += 1
            self.anim %= 4
            screen_game.blit(self.image, (self.rect.x, self.rect.y))
        else:
            im = load_image(f'{self.form}.png', 'characters/main_hero')
            im = pygame.transform.scale(im, (self.width, self.height))
            screen_game.blit(im, (self.rect.x, self.rect.y))
            self.anim = 0
        if pygame.sprite.spritecollide(self, attack_usual_skeleton_group, False):
            for i in pygame.sprite.spritecollide(self, attack_usual_skeleton_group, False):
                if i not in self.hitted:
                    self.characteristics['hp'] -= 1
                    self.hitted.append(i)
        if self.characteristics['hp'] <= 0:
            end()


class Room:
    # Инициализация начальных сведений о комнатах
    def __init__(self, map_list, room_number):
        self.room_number = room_number
        self.map_list = map_list
        self.map_size = len(map_list)

        self.em_room = ['empty_room', 280, 190, 1355, 660]
        self.this_room = self.map_list[self.room_number[0]][self.room_number[1]]

    # Генерация комнаты
    def create(self):
        global all_objects
        # Группа спрайтов объектов
        self.this_room = self.map_list[self.room_number[0]][self.room_number[1]]
        all_objects = pygame.sprite.Group()

        # Пустая комната
        screen_game.blit(em_room, (280, 190))
        # Двери
        if FIGHT:
            if room.change_room_number('up', change=False):
                screen_game.blit(doors_close[0], (925, 190))
            if room.change_room_number('down', change=False):
                screen_game.blit(doors_close[1], (925, 765))
            if room.change_room_number('left', change=False):
                screen_game.blit(doors_close[2], (285, 480))
            if room.change_room_number('right', change=False):
                screen_game.blit(doors_close[3], (1545, 480))
        else:
            if room.change_room_number('up', change=False):
                screen_game.blit(doors_open[0], (925, 190))
            if room.change_room_number('down', change=False):
                screen_game.blit(doors_open[1], (925, 765))
            if room.change_room_number('left', change=False):
                screen_game.blit(doors_open[2], (285, 480))
            if room.change_room_number('right', change=False):
                screen_game.blit(doors_open[3], (1545, 480))

        # Стартовая комната 1 уровня
        if self.this_room[0] == 'door_start':
            screen_game.blit(big_door, (765, 185))

        # Комната с сундуком
        elif self.this_room[0] == 'chest':
            if self.this_room[1] == 'used':
                chest.animation = 5
                chest.used()

            if chest.animation == chest.max_animation:
                map_list[room.room_number[0]][room.room_number[1]][1] = 'used'

            chest.update()
            all_objects.add(chest)
            screen_game.blit(chest.image_fin, (chest.rect.x, chest.rect.y))

        # Стартовая комната
        elif self.this_room[0] == 'start':
            screen_game.blit(stairs_image, (1425, 275))

        # Конечная комната
        elif self.this_room[0] == 'end':
            all_objects.add(stairs)
            screen_game.blit(stairs.image_fin, (stairs.rect.x, stairs.rect.y))
        # Комната с монстрами
        elif self.this_room[0] == 'monsters':
            if self.this_room[1] != 'used':
                for _ in range(3):
                    usual_skeleton()
                self.this_room[1] = 'used'
        # Аркадная комната
        elif self.this_room[0] == 'arcada':
            all_objects.add(automat)
            screen_game.blit(automat.image_fin, (automat.rect.x, automat.rect.y))

        elif room.this_room[0] == 'life_room':
            all_objects.add(death)
            screen_game.blit(death.image_fin, (death.rect.x, death.rect.y))

            all_objects.add(table_1, table_2, table_3)
            screen_game.blit(table_life_1.image_fin, (table_life_1.rect.x, table_life_1.rect.y))
            screen_game.blit(table_life_2.image_fin, (table_life_2.rect.x, table_life_2.rect.y))
            screen_game.blit(table_life_3.image_fin, (table_life_3.rect.x, table_life_3.rect.y))

            if room.this_room[1] != 'used':
                all_objects.add(dark_sphere_1, dark_sphere_2, dark_sphere_3)
                screen_game.blit(dark_sphere_1.image_fin, (dark_sphere_1.rect.x, dark_sphere_1.rect.y))
                screen_game.blit(dark_sphere_2.image_fin, (dark_sphere_2.rect.x, dark_sphere_2.rect.y))
                screen_game.blit(dark_sphere_3.image_fin, (dark_sphere_3.rect.x, dark_sphere_3.rect.y))

        elif room.this_room[0] == 'shop' or room.this_room[0] == 'upgrade_shop':
            if room.this_room[0] == 'shop':
                all_objects.add(trader_shop)
                screen_game.blit(trader_shop.image_fin, (trader_shop.rect.x, trader_shop.rect.y))
            else:
                all_objects.add(trader_upgrade)
                screen_game.blit(trader_upgrade.image_fin, (trader_upgrade.rect.x, trader_upgrade.rect.y))

            all_objects.add(table_1, table_2, table_3)
            screen_game.blit(table_1.image_fin, (table_1.rect.x, table_1.rect.y))
            screen_game.blit(table_2.image_fin, (table_2.rect.x, table_2.rect.y))
            screen_game.blit(table_3.image_fin, (table_3.rect.x, table_3.rect.y))

    # Проверка наличия комнаты в месте куда вы хотите перейти и изменение номера вашей комнаты
    def change_room_number(self, where, change):
        global main_text
        can = False

        if where == 'up':
            if (self.room_number[0] - 1 >= 0 and
                    self.map_list[self.room_number[0] - 1][self.room_number[1]][0] != 'no'):
                self.room_number[0] -= 1
                what = [0, -1]
                can = True
        elif where == 'down':
            if (self.room_number[0] + 1 < self.map_size and
                    self.map_list[self.room_number[0] + 1][self.room_number[1]][0] != 'no'):
                self.room_number[0] += 1
                what = [0, 1]
                can = True
        elif where == 'left':
            if (self.room_number[1] - 1 >= 0 and
                    self.map_list[self.room_number[0]][self.room_number[1] - 1][0] != 'no'):
                self.room_number[1] -= 1
                what = [1, -1]
                can = True
        elif where == 'right':
            if (self.room_number[1] + 1 < self.map_size and
                    self.map_list[self.room_number[0]][self.room_number[1] + 1][0] != 'no'):
                self.room_number[1] += 1
                what = [1, 1]
                can = True

        if change and can and not FIGHT:
            global all_objects, map_list
            all_objects = pygame.sprite.Group()

            if not pygame.mixer.Channel(sounds['door_open']).get_busy():
                pygame.mixer.Channel(sounds['door_open']).play(pygame.mixer.Sound(
                    'data/music_and_sounds/sounds/map_sounds/door_open.mp3'))

            main_text = ''
            self.room_number[what[0]] += what[1]
            map_list[self.room_number[0]][self.room_number[1]][2] = 'visited'

        if FIGHT:
            return False
        return can


# Начало всего
level = 1


def pause():
    global pausing
    pygame.mixer.Channel(sounds['steps']).stop()
    pausing = True


def end():
    global ending
    pygame.mixer.Channel(sounds['steps']).stop()
    ending = True


class weapon_on_ground(pygame.sprite.Sprite):
    def __init__(self, x, y, name, melee_or_not):
        global room, OBJECTS
        super().__init__(items_this_room_group)
        if melee_or_not:
            self.image = load_image(name, r'weapon\edged_weapons')
        else:
            self.image = load_image(name, r'weapon\magic')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if room.this_room[0] in OBJECTS:
            OBJECTS[room.this_room[0]].append(self)
        else:
            OBJECTS[room.this_room[0]] = [self]

    def update(self, *args, **kwargs):
        global player_group, player
        if pygame.sprite.spritecollide(self, player_group, False):
            for i in OBJECTS:
                for j in OBJECTS[i]:
                    if j == self:
                        print('del')
                        OBJECTS[i].remove(j)
            self.kill()


# Типы оружия
melee_weapons = {
    'usual_sword': {'damage': 20, 'CANMELEE': 0.1, 'hitbox_type': attack_rect, 'hitboxtime': 0.1,
                    'picture': 'usual_sword.png'},
    'usual_hammer': {'damage': 40, 'CANMELEE': 1, 'hitbox_type': 'NEED', 'hitboxtime': 0.3,
                     'picture': 'usual_hammer.png'}
}

magic_weapons = {
    'usual_fireball': {'damage': 5, 'CANMELEE': 0.5, 'type': fireball, 'mana': 5, 'picture': 'fireball.png'},
    'usual_thunderbolt': {'damage': 15, 'CANMELEE': 0.3, 'type': 'NEED', 'mana': 10, 'picture': 'thunderbolt.png'}
}


# Начало программы
def start():
    global screen_game, room
    global all_borders, all_objects
    global sounds, map_list
    global running, pausing, ending
    global pause_group, player_group
    global player
    global FIGHT, CANFIRE, CANMELEE
    global main_text, text_size
    global text_tick, max_text_tick
    global text_coords, player

    pygame.init()
    # Создание экрана
    width, height = 1920, 1080
    screen_game = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('Infinity Castle')

    # Фон и интерфейс
    interface()

    FPS = 120
    clock = pygame.time.Clock()

    # Музыка
    pygame.mixer.music.load('data/music_and_sounds/music/game_standart.mp3')
    pygame.mixer.music.play(-1)

    # Текст сверху
    main_text = ''
    text_tick = 0
    max_text_tick = 0
    text_size = 0
    text_coords = 0

    # Звуки
    sounds = {}
    channels = 3
    pygame.mixer.init(frequency=44100, size=-16, channels=channels, buffer=4096)

    sounds['steps'] = 1
    pygame.mixer.Channel(1)

    sounds['door_open'] = 2
    pygame.mixer.Channel(2)

    sounds['diffrent'] = 3
    pygame.mixer.Channel(3)

    sounds['battle_start'] = pygame.mixer.find_channel()

    # Начало меню конца
    font = pygame.font.Font(None, 32)
    text = ['Вы погибли, ваш путь окончен...', 'Количество пройденных этажей: ' + 'text']
    text_coord_ending = 200

    button_end_group = pygame.sprite.Group()
    Button('start_new_game.png', 300, 50, 800, 300, button_end_group)
    Button('menu_back.png', 250, 50, 820, 360, button_end_group)
    Button('game_stop.png', 250, 50, 820, 420, button_end_group)
    # Конец меню конца

    points3 = Button('points3.png', 200, 100, 1670, 20, button_pause)
    cont = Button('continue.png', 300, 100, 800, 300, pause_group)
    menu_back = Button('menu_back.png', 300, 100, 800, 500, pause_group)
    pausing = False
    ending = False

    map_list, room_number = map_generation(level=1, map_size=4)

    for i in map_list:
        for j in i:
            print(j[0], end='|')
        print()
    print(room_number)

    # Спрайт игрока и создание переменной комнаты
    player = Player()
    player_group = pygame.sprite.Group(player)

    if level > 1:
        player.rect.x = 1425
        player.rect.y = 280

    room = Room(map_list, room_number)

    # Курсор
    cursor_rect = pygame.Rect(280, 190, 1355, 660)
    cursor_x, cursor_y = cursor_rect.center
    pygame.mouse.set_pos(cursor_x, cursor_y)

    # Границы (1920, 1080)
    Border(300, 200, width - 300, 300)  # горизонт
    Border(300, height - 250, width - 300, height - 250)  # горизонт
    Border(300, 200, 300, height - 250)  # вертик
    Border(width - 300, 200, width - 300, height - 250)  # вертик

    usual_skeleton()
    weapon_on_ground(500, 500, 'usual_hammer.png', True)

    # Изменение анимации у интерактивных объектов
    global chest
    chest = Object('chest_animation_', 'map/chest', 900, 450, 150, 150, 5)

    # Основной цикл
    running = True
    while running:
        # Выход из программы
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if pausing:
                if event.type == pygame.KEYDOWN:
                    if event.unicode == SETTINGS['menu']:
                        pausing = False
                pause_group.update(event)

            elif ending:
                button_end_group.update(event)
            else:
                if event.type == pygame.KEYDOWN:
                    if event.unicode == SETTINGS['melee_weapon']:
                        player.melee_magic = 0
                    if event.unicode == SETTINGS['magic_weapon']:
                        player.melee_magic = 1
                    if event.unicode == SETTINGS['menu']:
                        pause()
                if event.type == pygame.KEYUP:
                    player.action(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    player.attack(event)

                button_pause.update(event)
                items_group.update(event)
        # Загрузка настроек, создание комнтаты, обновление персонажа
        if pausing:
            pygame.draw.rect(screen_game, 'Black', (600, 200, 700, 500), 0)
            pause_group.draw(screen_game)
        elif ending:
            pygame.draw.rect(screen_game, 'Black', (600, 200, 700, 500), 0)
            button_end_group.draw(screen_game)
            for line in text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord_ending += 10
                intro_rect.top = text_coord_ending
                intro_rect.x = 700
                text_coord_ending += intro_rect.height
                screen_game.blit(string_rendered, intro_rect)
            text_coord_ending = 200

        else:
            if len(usual_skeletons_group) == 0:
                FIGHT = False

            if time.process_time() - player.lastfire >= player.magic1['CANMELEE']:
                CANFIRE = True
            if time.process_time() - player.lastmelee >= player.melee1['CANMELEE']:
                CANMELEE = True
            for i in usual_skeletons_group:
                if time.process_time() - i.lastmelee >= 1:
                    i.canmelee = True
            for i in attack_group:
                if time.process_time() - i.timeappear >= 0.1:
                    i.kill()
            for i in attack_usual_skeleton_group:
                if time.process_time() - i.timeappear >= 0.3:
                    i.kill()
            load_settings(channels)
            #        check_cursor(cursor_rect)
            room.create()
            player.movement()
            player.update()

            screen_game.blit(text_field, (590, 40))

            # Обновление экрана сверху
            if main_text != '':
                if not (main_text == 'Пути назад уже нет' and map_list[room.room_number[0]][room.room_number[1]][
                                      0] != 'door_start'):
                    show_main_text(text_size)

            screen_game.blit(pygame.font.Font('data/shrifts/main_shrift.ttf', 60).render(
                f'Уровень: {level}', False, (20, 20, 20)), (1340, 880))

            all_borders.draw(screen_game)
            button_pause.draw(screen_game)

            magic_group.update()
            usual_skeletons_group.update()
            attack_group.update()
            coins_group.update()
            attack_usual_skeleton_group.update()
            items_this_room_group.update()

            magic_group.draw(screen_game)
            usual_skeletons_group.draw(screen_game)
            attack_group.draw(screen_game)
            coins_group.draw(screen_game)
            attack_usual_skeleton_group.draw(screen_game)

            items_group.draw(screen_game)
            items_this_room_group.draw(screen_game)
        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()


# Активация в тестах
if __name__ == '__main__':
    start()
