import pygame
import random
from func import load_image, show_image, terminate
from func import map_generation


# Загрузка данных из настроек
def load_settings():
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
        pass
    else:
        pass
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

    for i in images:
        show_image(i, screen_game, 'interface')


def check_cursor(cursor_rect):
    cursor_x, cursor_y = pygame.mouse.get_pos()
    if not cursor_rect.collidepoint(cursor_x, cursor_y):
        # Если курсор вышел за границы, возвращаем его обратно
        cursor_x = max(cursor_rect.left, min(cursor_x, cursor_rect.right))
        cursor_y = max(cursor_rect.top, min(cursor_y, cursor_rect.bottom))
        pygame.mouse.set_pos(cursor_x, cursor_y)


# Обновление изменяемых характеристик героя
def update_hp_mana_coins(*hp_states, **characteristics):
    show_image(['field_for_coin', 1420, 110, 200, 60],
               screen_game, 'interface')
    show_image(['field_for_coin', 370, 110, 250, 60], screen_game, 'interface')

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


def show_main_text(main_font):
    global text_tick, main_text

    if text_tick < max_text_tick:
        final_main_text = main_font.render(main_text, False, (20, 20, 20))
        screen_game.blit(final_main_text, (710, 110))
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
        self.speed = 15

        self.animation_flag = False
        self.time_animation = 0
        self.side_animation = 'right'
        self.walk_animation = 0

        self.form = [f'{self.side_animation}/stop',
                     self.x, self.y, self.width, 120]

        self.image = load_image(f'{self.form[0]}.png', 'characters\main_hero')
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.characteristics = {'coins': 0,
                                'hp': 4,
                                'unlocked_hp': 4,
                                'mana': 50,
                                'unlocked_mana': 50}

        self.hp_states = [['filled_cell_HP', 643, 897, 60, 52],
                          ['unfilled_cell_HP', 1219, 897, 60, 52],
                          ['loced_HP', 1235, 903, 30, 40]]

    def movement(self):
        # Перемещение
        keys = pygame.key.get_pressed()
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
            self.form = [f'{self.side_animation}/walk_{self.walk_animation}',
                         self.rect.x, self.rect.y, self.width, 120]
            if self.time_animation == 2:
                self.walk_animation = (self.walk_animation + 1) % 7
            self.time_animation = (self.time_animation + 1) % 3

            if not pygame.mixer.Channel(sounds['steps']).get_busy():
                pygame.mixer.Channel(sounds['steps']).play(pygame.mixer.Sound(
                    'data/music_and_sounds/sounds/main_hero_sounds/steps.mp3'))
        else:
            # Анимация стояния на месте
            self.form = [f'{self.side_animation}/stop',
                         self.rect.x, self.rect.y, self.width, 120]
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
                if 770 < self.rect.x < 1100 and 340 < self.rect.y < 630:
                    chest.animation_flag = True
                    map_list[room.room_number[0]
                             ][room.room_number[1]][1] = 'used'

            elif room.this_room[0] == 'door_start':
                if self.rect.y <= 195 and 840 < self.rect.x < 1000:
                    global main_text, text_tick, max_text_tick
                    main_text = 'Пути назад уже нет'
                    text_tick = 0
                    max_text_tick = 30
            
            elif room.this_room[0] == 'end':
                if self.rect.x >= 1240 and self.rect.y < 325:
                    global level
                    level += 1
                    start()

        elif event.key == pygame.K_z:
            print(self.rect.x, self.rect.y)

        elif event.key == pygame.K_c:
            room.fight_flag = not room.fight_flag

        # Обновление изменяемых характеристик и картинки героя

    def update(self):
        update_hp_mana_coins(*self.hp_states, **self.characteristics)
        show_image(self.form, screen_game, 'characters/main_hero')


class Object(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, image, where, x, y, width, height, max_animation):
        pygame.sprite.Sprite.__init__(self)
        self.animation_flag = False
        self.animation = 0
        self.max_animation = max_animation

        self.image = image
        self.where = where
        self.width = width
        self.height = height

        self.image_fin = load_image(f'{image}{self.animation}.png', where)
        self.image_fin = pygame.transform.scale(
            self.image_fin, (width, height))

        self.rect = self.image_fin.get_rect()
        self.rect.x = x
        self.rect.y = y

        all_objects.add(self)

    def update(self):
        if self.animation_flag and self.animation < self.max_animation:
            self.animation += 1

            self.image_fin = load_image(
                f'{self.image}{self.animation}.png', self.where)
            if not pygame.mixer.Channel(sounds['chest_open']).get_busy():
                pygame.mixer.Channel(sounds['chest_open']).play(pygame.mixer.Sound(
                    'data/music_and_sounds/sounds/map_sounds/chest_open.mp3'))
        show_image([f'{self.image}{self.animation}', self.rect.x,
                   self.rect.y, self.width, self.height], screen_game, self.where)


class Room():
    # Инициализация начальных сведений о комнатах
    def __init__(self, map_list, room_number):
        self.room_number = room_number
        self.map_list = map_list
        self.map_size = len(map_list)

        self.fight_flag = True

        # Дверь в начальной комнате
        self.big_door = ['doors/big_door', 765, 185, 400, 100]

        # Комнаты
        self.em_room = ['empty_room', 280, 190, 1355, 660]

    # Генерация комнаты
    def create(self):
        # Пустая комната
        show_image(self.em_room, screen_game, 'map')
        self.this_room = self.map_list[self.room_number[0]][self.room_number[1]]
        
        if self.fight_flag:
            door_state = 'close'
        else:
            door_state = 'open'

        door_up = [f'doors/door_{door_state}_up', 925, 190, 100, 85]
        door_down = [f'doors/door_{door_state}_down', 925, 765, 100, 85]
        door_left = [f'doors/door_{door_state}_left', 285, 480, 85, 100]
        door_right = [f'doors/door_{door_state}_right', 1545, 480, 85, 100]


        if room.change_room_number('up', change=False):
            show_image(door_up, screen_game, 'map')
        if room.change_room_number('down', change=False):
            show_image(door_down, screen_game, 'map')
        if room.change_room_number('left', change=False):
            show_image(door_left, screen_game, 'map')
        if room.change_room_number('right', change=False):
            show_image(door_right, screen_game, 'map')

        # Начальная комната игры
        if self.this_room[0] == 'door_start':
            show_image(self.big_door, screen_game, 'map')

        # Комната с сундуком
        elif self.this_room[0] == 'chest':
            global chest
            try:
                if not chest in all_objects:
                    if self.this_room[1] != 'used':
                        chest = Object('chest_animation_',
                                       'map/chest', 900, 450, 150, 150, 5)
                    else:
                        chest = Object('chest_animation_',
                                       'map/chest', 900, 450, 150, 150, 5)
                        chest.animation = 5
            except:
                chest = Object('chest_animation_', 'map/chest',
                               900, 450, 150, 150, 5)
            chest.update()

        elif self.this_room[0] == 'start':
            stairs_image = ['stairs/up', 1425, 275, 120, 120]
            show_image(stairs_image, screen_game, 'map')

        elif self.this_room[0] == 'end':
            global stairs
            stairs = Object('down_', 'map/stairs', 1350, 180, 200, 200, 0)
            stairs.update()


    # Проверка наличия комнаты в месте куда вы хотите перейти и изменение номера вашей комнаты
    def change_room_number(self, where, change):
        global main_text
        can = False
        main_text = ''

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
            global all_objects
            all_objects = pygame.sprite.Group()

            if not pygame.mixer.Channel(sounds['door_open']).get_busy():
                pygame.mixer.Channel(sounds['door_open']).play(pygame.mixer.Sound(
                    'data/music_and_sounds/sounds/map_sounds/door_open.mp3'))
            self.room_number[what[0]] += what[1]
            print(self.room_number)
        return can

# Начало программы
level = 1

def start():
    global screen_game, room
    global all_objects, level
    global sounds, map_list
    global main_text, text_tick, max_text_tick

    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=3, buffer=4096)
    # Создание экрана
    screen_game = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('Infinity Castle')

    # Фон и интерфейс
    fon = load_image('background.png', 'interface')
    fon = pygame.transform.scale(fon, (1920, 1080))
    screen_game.blit(fon, (0, 0))

    interface()

    FPS = 60
    clock = pygame.time.Clock()

    # Текст и шрифт сверху
    main_font = pygame.font.Font('data/shrifts/main_shrift.ttf', 50)
    main_text = ''
    text_tick = 0
    max_text_tick = 0

    # Музыка
    pygame.mixer.music.load('data/music_and_sounds/music/game_standart.mp3')
    pygame.mixer.music.play(-1)

    # Звуки
    sounds = {}

    sounds['steps'] = 1
    pygame.mixer.Channel(1)

    sounds['door_open'] = 2
    pygame.mixer.Channel(2)

    sounds['chest_open'] = 3
    pygame.mixer.Channel(3)

    # Генерация карты уровня
    map_list, room_number = map_generation(level, map_size=4)

    for i in map_list:
        for j in i:
            print(j[0], end='|')
        print()
    print(room_number)

    # Группы спрайтов
    all_objects = pygame.sprite.Group()

    # Спрайт игрока и создание переменной комнаты
    player = Player()
    if level > 1:
        player.rect.x = 1425
        player.rect.y = 280

    room = Room(map_list, room_number)

    # Координаты игрока

    # Курсор
    cursor_rect = pygame.Rect(380, 280, 1150, 470)
    cursor_x, cursor_y = cursor_rect.center
    pygame.mouse.set_pos(cursor_x, cursor_y)

    # Основной цикл
    running = True
    while running:
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

        interface() # Загрузка интерфейса
        load_settings()  # Загрузка настроек
        room.create()  # Создание комнаты

        player.movement()  # Движение игрока
        player.update()  # Обновление характеристик и спрайта игрока

        # Обновление экрана сверху
        if main_text != '':
            show_main_text(main_font)

        screen_game.blit(pygame.font.Font('data/shrifts/main_shrift.ttf', 60).render(
            f'Уровень: {level}', False, (20, 20, 20)), (1350, 880))

        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()


# Активация в тестах
if __name__ == '__main__':
    start()
