import pygame
import os
from func import load_image, show_image, terminate
from func import map_generation


button_pause = pygame.sprite.Group()
pause_group = pygame.sprite.Group()

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

# Отключено для паузы
# def check_cursor(cursor_rect):
#    cursor_x, cursor_y = pygame.mouse.get_pos()
#    if not cursor_rect.collidepoint(cursor_x, cursor_y):
#        # Если курсор вышел за границы, возвращаем его обратно
#        cursor_x = max(cursor_rect.left, min(cursor_x, cursor_rect.right))
#        cursor_y = max(cursor_rect.top, min(cursor_y, cursor_rect.bottom))
#        pygame.mouse.set_pos(cursor_x, cursor_y)


# Обновление изменяемых характеристик героя
def update_hp_mana_coins(*hp_states, **characteristics):
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
        hp_states[0][1] = 643 + i * 64
        show_image(hp_states[0], screen_game, 'interface')

    for i in range(10 - characteristics['hp']):
        hp_states[1][1] = 1219 - i * 64
        show_image(hp_states[1], screen_game, 'interface')

    for i in range(10 - characteristics['unlocked_hp']):
        hp_states[2][1] = 1235 - i * 64
        show_image(hp_states[2], screen_game, 'interface')


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
                for i in pause_group:
                    i.kill()
            elif self.button_type == 'menu_back.png':
                pygame.quit()
                os.system('python main.py')
            elif self.button_type == 'settings.png':
                pass


class Player(pygame.sprite.Sprite):
    # Инициализация начальных характеристик персонажа
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 900
        self.y = 350
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
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
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

            if not sounds['steps'].get_busy():
                sounds['steps'].play(pygame.mixer.Sound('data/music_and_sounds/sounds/main_hero_sounds/steps.mp3'))
        else:
            # Анимация стояния на месте
            self.form = [f'{self.side_animation}/stop',
                         self.rect.x, self.rect.y, self.width, 120]
            self.animation_flag = False
            self.time_animation = 0
            sounds['steps'].stop()

        self.animation_flag = False

    # Взаимодействия
    def action(self, event):
        if event.key == ord(SETTINGS['interaction']):
            # Двери
            can = False
            if self.rect.x >= 1440 and 400 < self.rect.y < 560:
                can = room.change_room_number('right')
                if can:
                    self.rect.x = 350
            elif self.rect.x <= 360 and 400 < self.rect.y < 550:
                can = room.change_room_number('left')
                if can:
                    self.rect.x = 1550 - self.width
            elif self.rect.y >= 635 and 840 < self.rect.x < 1000:
                can = room.change_room_number('down')
                if can:
                    self.rect.y = 190
            elif self.rect.y <= 195 and 840 < self.rect.x < 1000:
                can = room.change_room_number('up')
                if can:
                    self.rect.y = 765 - self.height

            # Сундук
            if room.this_room[0] == 'chest':
                if 770 < self.rect.x < 1100 and 340 < self.rect.y < 610:
                    chest.animation_flag = True
                    map_list[room.room_number[0]][room.room_number[1]][1] = 'used'

        elif event.key == pygame.K_z:
            print(self.rect.x, self.rect.y)

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
        self.image_fin = pygame.transform.scale(self.image_fin, (width, height))

        self.rect = self.image_fin.get_rect()
        self.rect.x = x
        self.rect.y = y

        all_objects.add(self)

    def update(self):
        if self.animation_flag and self.animation < self.max_animation:
            self.animation += 1

            self.image_fin = load_image(f'{self.image}{self.animation}.png', self.where)
            self.mask = pygame.mask.from_surface(self.image_fin)
        show_image([f'{self.image}{self.animation}', self.rect.x, self.rect.y, self.width, self.height], screen_game,
                   self.where)


class Room:
    # Инициализация начальных сведений о комнатах
    def __init__(self, map_list, room_number):
        self.room_number = room_number
        self.map_list = map_list
        self.map_size = len(map_list)

        self.em_room = ['empty_room', 280, 190, 1355, 660]

    # Генерация комнаты
    def create(self):
        # Пустая комната
        show_image(self.em_room, screen_game, 'map')
        self.this_room = self.map_list[self.room_number[0]][self.room_number[1]]

        # Комната с сундуком
        if self.this_room[0] == 'chest':
            global chest
            try:
                if chest not in all_objects:
                    if self.this_room[1] != 'used':
                        chest = Object('chest_animation_', 'map/chest', 900, 450, 150, 150, 5)
                    else:
                        chest = Object('chest_animation_', 'map/chest', 900, 450, 150, 150, 5)
                        chest.animation = 5
            except Exception:
                chest = Object('chest_animation_', 'map/chest', 900, 450, 150, 150, 5)
            chest.update()

    # Проверка наличия комнаты в месте куда вы хотите перейти и изменение номера вашей комнаты
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

        if can:
            global all_objects
            all_objects = pygame.sprite.Group()

            if not sounds['door_open'].get_busy():
                sounds['door_open'].play(pygame.mixer.Sound('data/music_and_sounds/sounds/map_sounds/door_open.mp3'))

        print(self.room_number)
        return can


def pause():
    global pausing
    points3 = Button('points3.png', 250, 100, 1620, 20, button_pause)
    cont = Button('continue.png', 300, 100, 800, 220, pause_group)
    menu_back = Button('menu_back.png', 300, 100, 800, 400, pause_group)
    settings_pause = Button('settings.png', 300, 100, 800, 500, pause_group)
    pausing = True


# Начало программы
def start():
    global screen_game, room
    global all_borders, all_objects
    global sounds, map_list
    global running, pausing
    global pause_group

    pygame.init()
    # Создание экрана
    screen_game = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('Infinity Castle')

    FPS = 60
    clock = pygame.time.Clock()

    # Музыка
    pygame.mixer.music.load('data/music_and_sounds/music/game_standart.mp3')
    pygame.mixer.music.play(-1)

    # Звуки
    sounds = {}

    sounds['steps'] = pygame.mixer.find_channel()
    sounds['door_open'] = pygame.mixer.find_channel()

    points3 = Button('points3.png', 250, 100, 1620, 20, button_pause)
    cont = Button('continue.png', 300, 100, 800, 220, pause_group)
    menu_back = Button('menu_back.png', 300, 100, 800, 400, pause_group)
    settings_pause = Button('settings.png', 300, 100, 800, 500, pause_group)
    pausing = False

    # Отрисовка интерфейса и генерация карты уровня
    interface()
    map_list, room_number = map_generation(level=1, map_size=4)

    for i in map_list:
        for j in i:
            print(j[0], end='|')
        print()
    print(room_number)

    # Группы спрайтов
    all_borders = pygame.sprite.Group()
    all_objects = pygame.sprite.Group()

    # Спрайт игрока и создание переменной комнаты
    player = Player()
    room = Room(map_list, room_number)

    # Курсор
    cursor_rect = pygame.Rect(280, 190, 1355, 660)
    cursor_x, cursor_y = cursor_rect.center
    pygame.mouse.set_pos(cursor_x, cursor_y)

    # Основной цикл
    running = True
    while running:
        # Выход из программы
        for event in pygame.event.get():
            if not pausing:
                if event.type == pygame.QUIT:
                    terminate()

                if event.type == pygame.KEYUP:
                    player.action(event)
                button_pause.update(event)
            else:
                if event.type == pygame.QUIT:
                    terminate()

                pause_group.update(event)
        # Загрузка настроек, создание комнтаты, обновление персонажа
        if not pausing:
            load_settings()
    #        check_cursor(cursor_rect)
            room.create()
            player.movement()
            player.update()
            all_borders.draw(screen_game)
            button_pause.draw(screen_game)
            clock.tick(FPS)
            pygame.display.flip()
        else:
            pygame.draw.rect(screen_game, 'Black', (600, 200, 700, 700), 0)
            pause_group.draw(screen_game)
            pygame.display.flip()
    pygame.quit()


# Активация в тестах
if __name__ == '__main__':
    start()
