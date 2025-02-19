import pygame
import random
import math
from func import terminate, map_generation
from game_load import *


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
    images = [['coin', 1330, 105, 70, 70], ['magic_frame', 470, 860, 120, 120], ['weapon_frame', 310, 855, 125, 125],
     ['unfilled_HP', 605, 860, 720, 125], ['mana_bar', 300, 100, 60, 80], 
     ['field_for_coin', 1420, 110, 200, 60], ['field_for_coin', 370, 110, 250, 60]]

    fon = load_image('background.png', 'interface')
    fon = pygame.transform.scale(fon, (1920, 1080))
    screen_game.blit(fon, (0, 0))

    pygame.draw.rect(screen_game, pygame.Color('black'), (275, 185, 1365, 670))
    pygame.draw.rect(screen_game, pygame.Color('white'), (280, 190, 1355, 660))

    for image in images:
        im = load_image(f'{image[0]}.png', 'interface')
        im = pygame.transform.scale(im, (image[3], image[4]))
        screen_game.blit(im, (image[1], image[2]))


def check_cursor(cursor_rect):
    cursor_x, cursor_y = pygame.mouse.get_pos()
    if not cursor_rect.collidepoint(cursor_x, cursor_y):
        # Если курсор вышел за границы, возвращаем его обратно
        cursor_x = max(cursor_rect.left, min(cursor_x, cursor_rect.right))
        cursor_y = max(cursor_rect.top, min(cursor_y, cursor_rect.bottom))
        pygame.mouse.set_pos(cursor_x, cursor_y)


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
        self.x = 920
        self.y = 250
        self.width = 100
        self.height = 120
        self.speed = 330

        self.animation_flag = False
        self.time_animation = 0
        self.side_animation = 'right'
        self.walk_animation = 0

        self.form = f'{self.side_animation}/stop'

        self.image = load_im([f'{self.form}', self.width, self.height], 'characters/main_hero')
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.characteristics = {'coins': 999,
                                'hp': 4,
                                'unlocked_hp': 4,
                                'hp_cell': 10,
                                'all_hp': 40,
                                'mana': 50,
                                'unlocked_mana': 50,
                                'damage_sword': 5,
                                'damage_magic': 10}

    def movement(self):
        # Перемещение
        keys = pygame.key.get_pressed()
        if not keys:
            return
        if keys[ord(SETTINGS['forward'])]:
            if self.rect.y - self.speed * delta_time>= 190:
                self.rect.y -= self.speed * delta_time
                self.animation_flag = True
                if pygame.sprite.spritecollideany(self, all_objects):
                    self.rect.y += self.speed * delta_time
        if keys[ord(SETTINGS['down'])]:
            if self.rect.y + self.height + self.speed * delta_time <= 765:
                self.rect.y += self.speed * delta_time
                self.animation_flag = True
                if pygame.sprite.spritecollideany(self, all_objects):
                    self.rect.y -= self.speed * delta_time
        if keys[ord(SETTINGS['left'])]:
            if self.rect.x - self.speed * delta_time >= 350:
                self.rect.x -= self.speed * delta_time
                self.animation_flag = True
                self.side_animation = 'left'
                if pygame.sprite.spritecollideany(self, all_objects):
                    self.rect.x += self.speed * delta_time
        if keys[ord(SETTINGS['right'])]:
            if self.rect.x + self.width + self.speed * delta_time <= 1550:
                self.rect.x += self.speed * delta_time
                self.animation_flag = True
                self.side_animation = 'right'
                if pygame.sprite.spritecollideany(self, all_objects):
                    self.rect.x -= self.speed * delta_time

        # Смена анимации перемещения
        if self.animation_flag:
            self.form = f'{self.side_animation}/walk_{self.walk_animation}'
            if self.time_animation == 7:
                self.walk_animation = (self.walk_animation + 1) % 8
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
        global main_text, text_size
        global text_tick, max_text_tick
        global text_coords

        if event.key == ord(SETTINGS['interaction']):
            # Двери
            can = False
            if self.rect.x >= 1440 and 400 < self.rect.y < 560:
                can = room.change_room_number('right', change=True)
                if can and not room.fight_flag:
                    self.rect.x = 350
            elif self.rect.x <= 360 and 400 < self.rect.y < 550:
                can = room.change_room_number('left', change=True)
                if can and not room.fight_flag:
                    self.rect.x = 1550 - self.width
            elif self.rect.y >= 635 and 840 < self.rect.x < 1000:
                can = room.change_room_number('down', change=True)
                if can and not room.fight_flag:
                    self.rect.y = 190
            elif self.rect.y <= 195 and 840 < self.rect.x < 1000:
                can = room.change_room_number('up', change=True)
                if can and not room.fight_flag:
                    self.rect.y = 765 - self.height

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
                    if not pygame.mixer.Channel(sounds['diffrent']).get_busy() and not pygame.mixer.Channel(sounds['diffrent']).get_busy():
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
                                pygame.mixer.Channel(sounds['diffrent']).play(pygame.mixer.Sound(
                                    'data/music_and_sounds/sounds/map_sounds/automat/loss.mp3'))
                                main_text = 'Упс, не повезло!'
                                text_tick = 0
                                max_text_tick = 50
                                text_size = 55
                                text_coords = [770, 110]
                            else:
                                pygame.mixer.Channel(sounds['diffrent']).play(pygame.mixer.Sound(
                                    'data/music_and_sounds/sounds/map_sounds/automat/victory.mp3'))
                                main_text = 'Вы выиграли!'
                                text_tick = 0
                                max_text_tick = 150
                                text_size = 55
                                text_coords = [790, 110]

                                if 0.55 <= chance < 0.7:
                                    pass # 30 монет
                                if 0.7 <= chance < 0.8:
                                    pass # Оружие
                                if 0.8 <= chance < 0.9:
                                    pass # Магия
                                if 0.9 <= chance < 1:
                                    pass # Зелье

            # Комната жизни
            elif room.this_room[0] == 'life_room':
                if map_list[room.room_number[0]][room.room_number[1]][1] != 'used':
                    if ((395 <= self.rect.x <= 605 and 430 <= self.rect.y <= 565) or 
                        (590 <= self.rect.x <= 810 and 190 <= self.rect.y <= 325) or 
                        (800 <= self.rect.x <= 1010 and 445 <= self.rect.y <= 565)):

                        map_list[room.room_number[0]][room.room_number[1]][1] = 'used'
                        chance = random.random()

                        if chance < 0.01:
                            if chance < 0.16:
                                player.characteristics['unlocked_mana'] += 25
                                player.characteristics['mana'] += 25
                            elif 0.16 <= chance < 0.33:
                                if player.characteristics['unlocked_hp'] + 1 <= 10:
                                    player.characteristics['unlocked_hp'] += 1
                                    player.characteristics['hp_all'] += player.characteristics['hp_cell']
                            
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
                                    player.characteristics['all_hp'] -= player.characteristics['hp_cell']
                            
                            main_text = 'Не повезло)'
                            text_tick = 0
                            max_text_tick = 100
                            text_size = 55
                            text_coords = [840, 110]
                        
                        pygame.mixer.Channel(sounds['diffrent']).play(pygame.mixer.Sound(
                                'data/music_and_sounds/sounds/map_sounds/storm.mp3'))

                        

        elif event.key == pygame.K_z:
            print(self.rect.x, self.rect.y)

        elif event.key == pygame.K_c:
            room.fight_flag = not room.fight_flag

    # Обновление изменяемых характеристик и картинки героя
    def update(self):
        self.characteristics['hp'] = math.ceil(self.characteristics['all_hp'] / self.characteristics['hp_cell'])
        self.update_hp_mana_coins()

        self.image = load_im([f'{self.form}', self.width, self.height], 'characters/main_hero')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        screen_game.blit(self.image, (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
    
    # Обновление изменяемых характеристик героя
    def update_hp_mana_coins(self):
        screen_game.blit(field_for_coin_short, (1420, 110))
        screen_game.blit(field_for_coin_long, (370, 110))

        coin_font = pygame.font.Font('data/shrifts/coins_shrift.ttf', 50)
        coin_text = coin_font.render(
            str(self.characteristics['coins']), False, (20, 20, 20))
        screen_game.blit(coin_text, (1475, 110))

        magic_font = pygame.font.Font('data/shrifts/coins_shrift.ttf', 50)
        magic_text = magic_font.render(f'{str(self.characteristics['mana'])}',
                                    False, (20, 20, 20))
        screen_game.blit(magic_text, (395, 110))

        magic_text = magic_font.render(f'/{str(self.characteristics['unlocked_mana'])}',
                                    False, (20, 20, 20))
        screen_game.blit(magic_text, (485, 110))

        for i in range(self.characteristics['hp']):
            hp_states_0_x = 643 + i * 64
            screen_game.blit(hp_states[0], (hp_states_0_x, 897))

        for i in range(10 - self.characteristics['hp']):
            hp_states_1_x = 1219 - i * 64
            screen_game.blit(hp_states[1], (hp_states_1_x, 897))

        for i in range(10 - self.characteristics['unlocked_hp']):
            hp_states_2_x = 1235 - i * 64
            screen_game.blit(hp_states[2], (hp_states_2_x, 903))


class Room():
    # Инициализация начальных сведений о комнатах
    def __init__(self, map_list, room_number):
        self.room_number = room_number
        self.map_list = map_list
        self.map_size = len(map_list)

        self.fight_flag = False

    # Генерация комнаты
    def create(self):
        global all_objects
        # Группа спрайтов объектов
        all_objects = pygame.sprite.Group()

        # Пустая комната
        screen_game.blit(em_room, (280, 190))
        self.this_room = self.map_list[self.room_number[0]][self.room_number[1]]
        
        # Двери
        if self.fight_flag:
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

        # Аркадная комната
        elif self.this_room[0] == 'arcada':
            all_objects.add(automat)
            screen_game.blit(automat.image_fin, (automat.rect.x, automat.rect.y))

        # Комната жизни
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

        # Магазины
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
        
        # Комната монстров
        elif room.this_room[0] == 'monsters':
            if room.this_room[1] != 'used':
                global all_monsters, arrows
                # Группа спрайтов мостров
                all_monsters = []
                room.fight_flag = True
                room.this_room[1] = 'used'

                for _ in range(random.randint(1, 2)):
                    all_monsters.append(Entmy_Knight())
                    
                for _ in range(random.randint(2, 3)):
                    all_monsters.append((Skeleton()))
                
                for _ in range(random.randint(1, 2)):
                    all_monsters.append((Archer()))
                    arrows = pygame.sprite.Group()
            
            if room.fight_flag:
                for monster in all_monsters:
                    monster.movement()
                
    # Проверка наличия комнаты в месте куда вы хотите перейти и изменение номера вашей комнаты
    def change_room_number(self, where, change):
        global main_text
        can = False

        if where == 'up':
            if (self.room_number[0] - 1 >= 0 and
                    self.map_list[self.room_number[0] - 1][self.room_number[1]][0] != 'no'):
                what = [0, -1]
                can = True
        elif where == 'down':
            if (self.room_number[0] + 1 < self.map_size and
                    self.map_list[self.room_number[0] + 1][self.room_number[1]][0] != 'no'):
                what = [0, 1]
                can = True
        elif where == 'left':
            if (self.room_number[1] - 1 >= 0 and
                    self.map_list[self.room_number[0]][self.room_number[1] - 1][0] != 'no'):
                what = [1, -1]
                can = True
        elif where == 'right':
            if (self.room_number[1] + 1 < self.map_size and
                    self.map_list[self.room_number[0]][self.room_number[1] + 1][0] != 'no'):
                what = [1, 1]
                can = True

        if change and can and not room.fight_flag:
            global all_objects, map_list
            all_objects = pygame.sprite.Group()

            if not pygame.mixer.Channel(sounds['door_open']).get_busy():
                pygame.mixer.Channel(sounds['door_open']).play(pygame.mixer.Sound(
                    'data/music_and_sounds/sounds/map_sounds/door_open.mp3'))
            
            main_text = ''
            self.room_number[what[0]] += what[1]
            print(self.room_number, map_list[self.room_number[0]][self.room_number[1]][2])
            map_list[self.room_number[0]][self.room_number[1]][2] = 'visited'
        return can


# Общий класс монстров
class Monsters(pygame.sprite.Sprite):
    # Инициализация начальных характеристик монстров
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = random.randint(350, 1450)
        self.y = random.randint(190, 645)

        self.animation_flag = False
        self.time_animation = 0
        self.side_animation = 1
        self.walk_animation = 0

        self.attack_wait_tick = 0

        self.run = False

        self.life = True
        self.form = [self.side_animation, self.walk_animation]

    # Получение урона
    def check_damage(self):
        pass
    

class Skeleton(Monsters):
    def __init__(self):
        Monsters.__init__(self)
        self.animations = [[[skeleton_left_0, skeleton_left_1, skeleton_left_2, 
                            skeleton_left_3, skeleton_left_4, skeleton_left_5, skeleton_left_6],
                            [skeleton_left_atack_0, skeleton_left_atack_1,
                             skeleton_left_atack_2, skeleton_left_atack_3, skeleton_left_atack_4]],

                           [[skeleton_right_0, skeleton_right_1, skeleton_right_2, 
                            skeleton_right_3, skeleton_right_4, skeleton_right_5, skeleton_right_6],
                            [skeleton_left_atack_0, skeleton_left_atack_1,
                             skeleton_left_atack_2, skeleton_left_atack_3, skeleton_left_atack_4]]]

        self.mask = pygame.mask.from_surface(self.animations[1][0][0])
        self.rect = self.animations[1][0][0].get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = 250

        self.attack = False
        self.walk_time = 0
        self.max_walk_time = random.randint(60, 200)

        self.walk_wait_tick = 0
        self.max_walk_wait_tick = random.randint(100, 150)

        self.time_animation_attack = 0
        self.max_time_animation_attack = 10
        self.attack_animation = 0

        self.characteristics = {'hp': 4,
                                'damage': 5}

    def movement(self):
        self.player_x = player.rect.x
        self.player_y = player.rect.y

        # Вычисление пути
        dx = self.player_x - self.rect.x
        dy = self.player_y - self.rect.y
        distance = math.hypot(dx, dy)

        if distance > 0:
            self.dis_x = dx / distance
            self.dis_y = dy / distance

        # Окончание ожидания
        if self.walk_wait_tick == self.max_walk_wait_tick:
            self.run = True

        self.max_time_animation = 10

        if self.run:
            # Перемещение к игроку
            if (350 < self.rect.x + self.dis_x * self.speed * delta_time < 1450 and 
                190 < self.rect.y + self.dis_y * self.speed * delta_time < 645):
                    self.rect.x += self.dis_x * self.speed * delta_time
                    self.rect.y += self.dis_y * self.speed * delta_time

            # Анимация ходьбы
            self.form = [self.side_animation, self.walk_animation]
            if self.time_animation == self.max_time_animation:
                self.walk_animation = (self.walk_animation + 1) % 7

            self.walk_time += 1
            # Конец ходьбы
            if self.walk_time == self.max_walk_time:
                self.run = False
                self.walk_time = 0
                self.walk_wait_tick = 0
                self.max_walk_wait_tick = random.randint(100, 300)
                self.max_walk_time = random.randint(60, 200)

            # Атака
            if pygame.sprite.collide_mask(self, player):
                self.run = False
                self.attack = True
                self.walk_wait_tick = 0
                if not pygame.mixer.Channel(sounds['hurt']).get_busy():
                    pygame.mixer.Channel(sounds['hurt']).play(pygame.mixer.Sound(
                        'data/music_and_sounds/sounds/main_hero_sounds/hurt.mp3'))
                    player.characteristics['all_hp'] -= self.characteristics['damage']
        else:
            # Анимация стояния на месте
            self.form = [self.side_animation, 0]
            self.time_animation = 0

        # Поворот к игроку
        if self.rect.x < player.rect.x:
            self.side_animation = 1
        else:
            self.side_animation = 0

        # Анимация атаки
        if self.attack:
            if self.time_animation_attack == self.max_time_animation_attack:
                self.time_animation_attack = 0
                self.attack_animation += 1
                if self.attack_animation % 5 == 0:
                    self.attack_animation %= 5
                    self.attack = False
                    self.time_animation_attack = 0
            self.time_animation_attack += 1

        # Отображение анимации
        if self.attack:
            screen_game.blit(self.animations[self.form[0]][1][self.attack_animation], (self.rect.x, self.rect.y))
            self.mask = pygame.mask.from_surface(self.animations[self.form[0]][1][self.attack_animation])
        else:
            screen_game.blit(self.animations[self.form[0]][0][self.form[1]], (self.rect.x, self.rect.y))
            self.mask = pygame.mask.from_surface(self.animations[self.form[0]][0][self.form[1]])

        self.time_animation = (self.time_animation + 1) % (self.max_time_animation + 1)
        
        if not self.attack:
            self.walk_wait_tick += 1



class Entmy_Knight(Monsters):
    def __init__(self):
        Monsters.__init__(self)
        self.animations = [[enemy_knight_left_0, enemy_knight_left_1, enemy_knight_left_2, 
                            enemy_knight_left_3, enemy_knight_left_4, enemy_knight_left_5],
                           [enemy_knight_right_0, enemy_knight_right_1, enemy_knight_right_2, 
                            enemy_knight_right_3, enemy_knight_right_4, enemy_knight_right_5]]

        self.mask = pygame.mask.from_surface(self.animations[1][0])
        self.rect = self.animations[1][0].get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.speed = 500
        self.max_attack_wait_tick = random.randint(150, 300)

        self.characteristics = {'hp': 4,
                                'damage': 5}

    def movement(self):
        # Окончание ожидания
        if self.attack_wait_tick == self.max_attack_wait_tick:
            self.run = True
            self.player_x = player.rect.x
            self.player_y = player.rect.y

            # Вычисление пути
            dx = self.player_x - self.rect.x
            dy = self.player_y - self.rect.y
            distance = math.hypot(dx, dy)

            if distance > 0:
                self.dis_x = dx / distance
                self.dis_y = dy / distance

            # Вычисление анимации
            self.max_time_animation = int(abs(dx / (self.dis_x * self.speed * delta_time)) / 5)

        if self.run:
            # Перемещение к игроку
            if (350 < self.rect.x + self.dis_x * self.speed * delta_time < 1450 and 
                190 < self.rect.y + self.dis_y * self.speed * delta_time < 645):
                    self.rect.x += self.dis_x * self.speed * delta_time
                    self.rect.y += self.dis_y * self.speed * delta_time

            # Анимация прыжка
            self.form = [self.side_animation, self.walk_animation]
            if self.time_animation == self.max_time_animation:
                self.walk_animation = (self.walk_animation + 1) % 6

            # Конец прыжка
            if not (350 + self.speed * delta_time <= self.rect.x <= 1450 - self.speed * delta_time and
                    190 + self.speed * delta_time <= self.rect.y <= 645 - self.speed * delta_time):
                        self.run = False
                        self.attack_wait_tick = 0
                        self.max_attack_wait_tick = random.randint(150, 300)

            # Атака
            if pygame.sprite.collide_mask(self, player):
                if not pygame.mixer.Channel(sounds['hurt']).get_busy():
                    pygame.mixer.Channel(sounds['hurt']).play(pygame.mixer.Sound(
                        'data/music_and_sounds/sounds/main_hero_sounds/hurt.mp3'))
                    player.characteristics['all_hp'] -= self.characteristics['damage']
                            
            self.time_animation = (self.time_animation + 1) % (self.max_time_animation + 1)
        else:
            # Анимация стояния на месте
            self.form = [self.side_animation, 0]
            self.time_animation = 0

            # Поворот к игроку
            if self.rect.x < player.rect.x:
                self.side_animation = 1
            else:
                self.side_animation = 0

        # Отображение анимации
        screen_game.blit(self.animations[self.form[0]][self.form[1]], (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.animations[self.form[0]][self.form[1]])

        self.attack_wait_tick += 1


class Archer(Monsters):
    def __init__(self):
        Monsters.__init__(self)
        self.animations = [[archer_left_atack_0, archer_left_atack_1, archer_left_atack_2, archer_left_atack_3, 
                            archer_left_atack_4, archer_left_atack_5, archer_left_atack_6, archer_left_atack_7],

                            [archer_right_atack_0, archer_right_atack_1, archer_right_atack_2, archer_right_atack_3, 
                             archer_right_atack_4, archer_right_atack_5, archer_right_atack_6, archer_right_atack_7]]

        self.mask = pygame.mask.from_surface(self.animations[1][0])
        self.rect = self.animations[1][0].get_rect()

        chance = random.random()

        if chance < 0.25:
            self.x = 380
            self.y = 220
        elif 0.25 <= chance < 0.50:
            self.x = 1390
            self.y = 220
        elif 0.50 <= chance < 0.75:
            self.x = 1390
            self.y = 650
        else:
            self.x = 380
            self.y = 650

        self.rect.x = self.x
        self.rect.y = self.y

        self.attack = False
        self.max_attack_wait_tick = random.randint(250, 400)

        self.time_animation_attack = 0
        self.max_time_animation_attack = 10
        self.attack_animation = 0

        self.characteristics = {'hp': 4}

    def movement(self):
        # Поворот к игроку
        if self.rect.x < player.rect.x:
            self.side_animation = 1
        else:
            self.side_animation = 0

        # Атака
        if self.attack_wait_tick == self.max_attack_wait_tick:
            self.attack = True
            self.attack_wait_tick = 0
            self.max_attack_wait_tick = random.randint(250, 400)

        # Анимация атаки
        if self.attack:
            if self.time_animation_attack == self.max_time_animation_attack:
                self.time_animation_attack = 0
                self.attack_animation += 1
                if self.attack_animation % 8 == 0:
                    self.attack_animation %= 8
                    self.attack = False

                    # Создаем стрелу, направленную в цель
                    arrows.add(Arrow(self.rect.center))

            else:
                self.time_animation_attack += 1

        # Отображение анимации
        screen_game.blit(self.animations[self.side_animation][self.attack_animation], (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.animations[self.side_animation][self.attack_animation])
        
        if not self.attack:
            self.attack_wait_tick += 1


class Arrow(Monsters):
    def __init__(self, start_pos):
        Monsters.__init__(self)
        
        self.image = arrow
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.speed = 600

        self.characteristics = {'damage': 5}

        # Вычисляем направление движения
        self.direction = pygame.math.Vector2(player.rect.center) - pygame.math.Vector2(start_pos)
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        # Вычисляем угол поворота и поворачиваем
        angle = math.degrees(math.atan2(-self.direction.y, self.direction.x))
        self.image = pygame.transform.rotate(self.image, angle)

    def update(self):
        # Двигаем стрелу
        self.rect.center += self.direction * self.speed * delta_time

        # Удаляем стрелу, если она вышла за пределы экрана
        if not (350 <= self.rect.x <= 1500 and
                    190 <= self.rect.y <= 720):
            self.kill()

        # Попадание
        if pygame.sprite.collide_mask(self, player):
            if not pygame.mixer.Channel(sounds['hurt']).get_busy():
                pygame.mixer.Channel(sounds['hurt']).play(pygame.mixer.Sound(
                    'data/music_and_sounds/sounds/main_hero_sounds/hurt.mp3'))
                player.characteristics['all_hp'] -= self.characteristics['damage']
                self.kill()
        
        screen_game.blit(self.image, (self.rect.x, self.rect.y))

        
# Уровень
level = 1
# Спрайт игрока
player = Player()


# Начало программы
def start():
    global screen_game, room
    global all_objects, level
    global sounds, map_list
    global main_text,text_size
    global text_tick, max_text_tick
    global text_coords, player
    
    pygame.init()
    channels = 4
    pygame.mixer.init(frequency=44100, size=-16, channels=channels, buffer=4096)

    # Создание экрана
    screen_game = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('Infinity Castle')

    # Фон и интерфейс
    interface()

    FPS = 60
    clock = pygame.time.Clock()

    # Текст сверху
    main_text = ''
    text_tick = 0
    max_text_tick = 0
    text_size = 0
    text_coords = 0

    # Музыка
    pygame.mixer.music.load('data/music_and_sounds/music/game_standart.mp3')
    pygame.mixer.music.play(-1)

    # Звуки
    sounds = {}

    sounds['steps'] = 1
    pygame.mixer.Channel(1)

    sounds['door_open'] = 2
    pygame.mixer.Channel(2)

    sounds['diffrent'] = 3
    pygame.mixer.Channel(3)

    sounds['hurt'] = 4
    pygame.mixer.Channel(4)

    # Генерация карты уровня
    map_list, room_number = map_generation(level, map_size=4)

    # Загрузка интерфейса и настроек
    interface()
    load_settings(channels)

    for i in map_list:
        for j in i:
            print(j[0], end='|')
        print()
    print(room_number)

    # Спрайт игрока
    if level > 1:
        player.rect.x = 1425
        player.rect.y = 280
    player.characteristics['all_hp'] = player.characteristics['hp'] * player.characteristics['hp_cell']

    # Cоздание переменной комнаты
    room = Room(map_list, room_number)
    map_list[room.room_number[0]][room.room_number[1]][2] = 'visited'

    # Курсор
    cursor_rect = pygame.Rect(380, 280, 1150, 470)
    cursor_x, cursor_y = cursor_rect.center
    pygame.mouse.set_pos(cursor_x, cursor_y)

    # Изменение анимации у интерактивных объектов
    global chest
    chest = Object('chest_animation_','map/chest', 900, 450, 150, 150, 5)

    # Основной цикл
    running = True
    while running:
        global delta_time
        delta_time = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            # Выход из программы
            if event.type == pygame.QUIT:
                running = False
                terminate()

            # Взаимодействие
            if event.type == pygame.KEYUP:
                player.action(event)

            if event.type == pygame.MOUSEMOTION:
                check_cursor(cursor_rect)  # Ограничение курсора

        screen_game.blit(text_field, (590, 40))
        room.create()  # Создание комнаты

        player.movement()  # Движение игрока
        player.update()  # Обновление характеристик и спрайта игрока

        try:
            for i in arrows:
                i.update()
        except Exception:
            pass

        # Обновление экрана сверху
        if main_text != '':
            if not(main_text == 'Пути назад уже нет' and map_list[room.room_number[0]][room.room_number[1]][0] != 'door_start'): 
                show_main_text(text_size)

        screen_game.blit(pygame.font.Font('data/shrifts/main_shrift.ttf', 60).render(
            f'Уровень: {level}', False, (20, 20, 20)), (1340, 880))

        pygame.display.flip()

    pygame.quit()


# Активация в тестах
if __name__ == '__main__':
    start()
