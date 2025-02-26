import pygame
import os
import sys
from func import load_image, terminate
import sqlite3
from InputBox import InputBox, One_Symbol_InputBox


pygame.init()
screen = pygame.display.set_mode((900, 900))
FPS = 60
screen.fill('black')
pygame.display.set_caption('Infinity Castle')
clock = pygame.time.Clock()
clock.tick(FPS)
# Список с кнопками меню (картинка; ширина, высота, координата левого верхнего угла по x)
buttons_menu = [('infinity.png', 200, 75, 330), ('castle.png', 200, 65, 330), ('game_start.png', 300, 60, 280),
                ('achievenments.png', 250, 60, 300), ('settings.png', 250, 60, 300), ('leader_board.png', 300, 60, 280),
                ('game_stop.png', 300, 60, 280)]
# Список с кнопками, но уже для настроек
buttons_settings = [('sound1.png', 200, 60, 330), ('musik1.png', 200, 60, 330)]
# Группа для кнопок (всех)
button_group = pygame.sprite.Group()
# Ник зарег. человека
NICKNAME = ''
names = ['Вперёд', 'Налево', 'Вниз', 'Направо', 'Взаимодействие', 'Меню']
names_eng = ['forward', 'left', 'down', 'right', 'interaction', 'menu']


def load_settings():
    global SETTINGS
    # загрузка настроек из файла
    SETTINGS = ['sound 1', 'musik 1', 'forward w', 'left a', 'down s', 'right d', 'interaction f', 'menu ']
    try:
        test = open('settings.txt')
    except Exception:
        test = open('settings.txt', 'w+')
        for i in SETTINGS:
            test.write(i + '\n')
    test.seek(0)
    SETTINGS = []
    for i in test.readlines():
        SETTINGS.append(i.strip().split())
    test.close()
    for i in SETTINGS:
        if i[0] == 'sound':
            if i[1] == '1':
                buttons_settings[0] = ('sound1.png', 200, 60, 330)
            else:
                buttons_settings[0] = ('sound0.png', 200, 60, 330)
        elif i[0] == 'musik':
            if i[1] == '1':
                buttons_settings[1] = ('musik1.png', 200, 60, 330)
                pygame.mixer.music.set_volume(1)
            else:
                buttons_settings[1] = ('musik0.png', 200, 60, 330)
                pygame.mixer.music.set_volume(0)


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
        global NICKNAME
        global input_box
        global input_box1
        global input_box2
        global input_box1_regist
        global input_box2_regist
        # Действия при активации разных кнопок. Их отличают по названию картинки
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            if self.button_type == 'game_start.png':
                if NICKNAME:
                    pygame.quit()
                    os.system('python game.py')
                    sys.exit()
                else:
                    account_login()
            elif self.button_type == 'achievenments.png':
                achievenments()
            elif self.button_type == 'settings.png':
                settings()
            elif self.button_type == 'leader_board.png':
                if NICKNAME:
                    leader_board()
                else:
                    account_login()
            elif self.button_type == 'game_stop.png':
                terminate()

            elif self.button_type == 'back.png':
                if START:
                    account_login()
                else:
                    menu()

            elif self.button_type == 'sound1.png':
                self.button_type = 'sound0.png'
                self.image = load_image(self.button_type, 'main')
                self.image = pygame.transform.scale(self.image, self.rect.size)
                settings_change('sound 0')
            elif self.button_type == 'sound0.png':
                self.button_type = 'sound1.png'
                self.image = load_image(self.button_type, 'main')
                self.image = pygame.transform.scale(self.image, self.rect.size)
                settings_change('sound 1')
            elif self.button_type == 'musik1.png':
                self.button_type = 'musik0.png'
                self.image = load_image(self.button_type, 'main')
                self.image = pygame.transform.scale(self.image, self.rect.size)
                settings_change('musik 0')
            elif self.button_type == 'musik0.png':
                self.button_type = 'musik1.png'
                self.image = load_image(self.button_type, 'main')
                self.image = pygame.transform.scale(self.image, self.rect.size)
                settings_change('musik 1')
            elif self.button_type == 'confirm_settings.png':
                for i in range(len(input_box)):
                    settings_change(names_eng[i] + ' ' + input_box[i].returning())
            elif self.button_type == 'settings_reset.png':
                os.remove('settings.txt')
                load_settings()
                settings()
                for i in range(len(input_box)):
                    input_box[i].text = SETTINGS[2 + i][1]
                    input_box[i].render()
                    input_box[i].draw(screen)
            elif self.button_type == 'confirm.png':
                account_check(input_box1.returning(),
                              input_box2.returning(),
                              'login')
            elif self.button_type == 'confirm_regist.png':
                account_check(input_box1_regist.returning(),
                              input_box2_regist.returning(),
                              'regist')
            elif self.button_type == 'register.png':
                account_regist()

            elif self.button_type == 'account_leave.png':
                NICKNAME = ''
                account_login()


def menu():
    # Отображение меню
    for i in button_group:
        i.kill()
    fon = load_image('menu_fon.png', 'main')
    fon = pygame.transform.scale(fon, (900, 900))
    screen.blit(fon, (0, 0))
    for i in range(7):
        Button(buttons_menu[i][0], buttons_menu[i][1], buttons_menu[i][2], buttons_menu[i][3], 100 + 70 * i,
               button_group)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            button_group.update(event)
        button_group.draw(screen)
        pygame.display.flip()

    pygame.quit()


def settings():
    global input_box
    # Отображение настроек
    for i in button_group:
        i.kill()
    screen.fill('black')
    Button('back.png', 200, 70, 10, 10, button_group)
    Button('confirm_settings.png', 200, 70, 330, 700, button_group)
    Button('settings_reset.png', 200, 70, 600, 700, button_group)
    for i in range(2):
        Button(buttons_settings[i][0], buttons_settings[i][1], buttons_settings[i][2],
               buttons_settings[i][3], 70 + 70 * i, button_group)
    input_box = []
    font = pygame.font.Font(None, 30)
    for i in range(6):
        input_box.append(One_Symbol_InputBox(330, 330 + 50 * i, 100, 40, text=SETTINGS[2 + i][1]))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            button_group.update(event)
            for i in input_box:
                i.handle_event(event)
        for i in input_box:
            i.update()
        screen.fill('black')
        for i in range(6):
            string_rendered = font.render(f'{names[i]}', 1, pygame.Color('white'))
            rect_size = pygame.rect.Rect(130, 335 + 50 * i, 70, 40)
            screen.blit(string_rendered, rect_size)
        for i in input_box:
            i.draw(screen)

        button_group.draw(screen)
        pygame.display.flip()

    pygame.quit()


def achievenments():
    global NICKNAME
    for i in button_group:
        i.kill()
    screen.fill('black')
    Button('back.png', 200, 70, 10, 10, button_group)
    running = True

    font = pygame.font.Font(None, 32)
    text = ['Ваши достижения:']
    text_coord_ending = 200

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            button_group.update(event)
        screen.fill('black')
        button_group.draw(screen)
        for line in text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord_ending += 10
            intro_rect.top = text_coord_ending
            intro_rect.x = 400
            text_coord_ending += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        text_coord_ending = 200
        pygame.display.flip()


def account_login():
    # Отображение окна с входом в аккаунт
    global NICKNAME
    global input_box1
    global input_box2
    for i in button_group:
        i.kill()
    screen.fill('black')
    # Если пользователь уже зарег., то этого окна не будет

    if not NICKNAME:
        input_box1 = InputBox(350, 300, 140, 32)
        input_box2 = InputBox(350, 400, 140, 32)
        input_boxes = [input_box1, input_box2]
        running = True

        Button('account_ask.png', 250, 60, 320, 200, button_group)
        Button('confirm.png', 220, 70, 340, 500, button_group)
        if not START:
            Button('back.png', 200, 70, 10, 10, button_group)
        Button('register.png', 220, 70, 340, 600, button_group)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    terminate()
                for box in input_boxes:
                    box.handle_event(event)
                button_group.update(event)

            for box in input_boxes:
                box.update()

            screen.fill('black')
            for box in input_boxes:
                box.draw(screen)

            button_group.draw(screen)
            pygame.display.flip()
        pygame.quit()
    else:
        menu()


def account_regist():
    global input_box1_regist
    global input_box2_regist

    for i in button_group:
        i.kill()
    screen.fill('black')

    Button('back.png', 200, 70, 10, 10, button_group)
    Button('confirm_regist.png', 200, 70, 350, 450, button_group)
    input_box1_regist = InputBox(350, 300, 140, 32)
    input_box2_regist = InputBox(350, 400, 140, 32)
    input_boxes = [input_box1_regist, input_box2_regist]

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            for box in input_boxes:
                box.handle_event(event)
            button_group.update(event)

        for box in input_boxes:
            box.update()

        screen.fill('black')
        for box in input_boxes:
            box.draw(screen)

        button_group.draw(screen)
        pygame.display.flip()
    pygame.quit()


def leader_board():
    # отображение лидеров по пройденным этажам
    for i in button_group:
        i.kill()
    screen.fill('black')
    db = sqlite3.connect("data\\InfinityCastle_db")

    cur = db.cursor()
    inf_level_board = list(cur.execute('SELECT accounts.nickname, leaderboard_level.level FROM'
                                       ' leaderboard_level LEFT JOIN accounts on accounts.Id = leaderboard_level.Id')
                           .fetchall())
    db.close()

    Button('back.png', 200, 70, 10, 10, button_group)
    Button('account_leave.png', 300, 60, 580, 820, button_group)

    font = pygame.font.Font(None, 30)
    text_coord = 50
    i = 0
    for line in [i[0] + ' ' + str(i[1]) for i in sorted(inf_level_board, key=lambda x: x[1], reverse=True)][:5]:
        i += 1
        string_rendered = font.render(f'{i}) {line} этажа(ей)', 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 350
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    name_render = font.render('Текущий аккаунт ' + NICKNAME, 1, pygame.Color('white'))
    intro_rect = pygame.rect.Rect(10, 870, 200, 200)
    screen.blit(name_render, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            button_group.update(event)
        button_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def settings_change(a):
    # Обновление настроек
    new_settings = a.split()
    with open('settings.txt') as f:
        aa = list((i.strip().split() for i in f.readlines()))
        for i in range(len(aa)):
            if aa[i][0] == new_settings[0]:
                aa[i][1] = new_settings[1]
                break
    with open('settings.txt', 'w') as f:
        for i in aa:
            f.write(' '.join(i) + '\n')
    load_settings()


def account_check(a, b, tip):
    global START
    db = sqlite3.connect("data\\InfinityCastle_db")

    cur = db.cursor()
    inf = list(cur.execute('SELECT * FROM accounts').fetchall())
    db.close()

    # Проверка существования аккаунта по базе данных
    global NICKNAME
    status = False
    status1 = False
    for i in inf:
        if i[1] == a and a != '':
            status1 = True
            if i[2] == b:
                status = True
    if tip == 'login':
        if status:
            NICKNAME = a
            START = True
            with open('account_info.txt', 'w+') as f:
                f.write(a)
            menu()
        else:
            Button('wrong_name_password.png', 410, 60, 250, 750, button_group)
    elif tip == 'regist':
        if status1 or a == '':
            Button('taken_name.png', 300, 60, 300, 600, button_group)
        else:
            db = sqlite3.connect('data\\InfinityCastle_db')
            cur = db.cursor()
            cur.execute(f'INSERT INTO accounts(nickname, password) VALUES("{a}", "{b}")')
            cur.execute(f'INSERT INTO leaderboard_level(Id, level) '
                        f'VALUES((SELECT Id FROM accounts WHERE nickname="{a}"), 0)')
            cur.execute(f'INSERT INTO savings(Id, level, coins, hp, unlocked_hp, hp_cell, all_hp, '
                        f'mana, unlocked_mana, melee_power, magic_power, '
                        f'protection, critical_damage, melee_weapon, magic_weapon) '
                        f'VALUES((SELECT Id FROM accounts WHERE nickname="{a}"), '
                        f'0, 0, 4, 4, 15, 60, 50, 50, 0, 0, 0, 0, "usual_sword", "usual_fireball")')
            db.commit()
            db.close()
            NICKNAME = a
            START = False
            with open('account_info.txt', 'w+') as f:
                f.write(a)
            menu()


if __name__ == '__main__':
    START = True
    # Музыка
    pygame.mixer.music.load('data/music_and_sounds/music/menu.mp3')
    pygame.mixer.music.play(-1)
    # Активация приложения
    load_settings()

    with open('account_info.txt') as f:
        f = str(f.readline()).strip()
        if f != '':
            NICKNAME = f

    account_login()
