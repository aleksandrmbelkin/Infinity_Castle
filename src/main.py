import pygame
import os
import sys
from func import load_image, terminate
import sqlite3
from InputBox import InputBox


pygame.init()
screen = pygame.display.set_mode((900, 900))
FPS = 60
screen.fill('black')
pygame.display.set_caption('Infinity Castle')
clock = pygame.time.Clock()
clock.tick(FPS)
# Список с кнопками меню (картинка; ширина, высота, координата левого верхнего угла по x)
buttons_menu = [('infinity.png', 200, 60, 330), ('castle.png', 200, 60, 330), ('game_start.png', 300, 60, 280),
                ('training.png', 200, 60, 330), ('settings.png', 250, 60, 300), ('leader_board.png', 300, 60, 280),
                ('game_stop.png', 300, 60, 280)]
# Список с кнопками, но уже для настроек
buttons_settings = [('sound1.png', 200, 60, 330), ('musik1.png', 200, 60, 330)]
# Группа для кнопок (всех)
button_group = pygame.sprite.Group()
# Ник зарег. человека
NICKNAME = ''


def load_settings():
    # загрузка настроек из файла
    try:
        test = open('settings.txt')
    except Exception:
        test = open('settings.txt', 'w+')
        test.write('sound 1\n')
        test.write('musik 1\n')
    test.seek(0)
    SETTINGS = []
    for i in test.readlines():
        SETTINGS.append(i.strip().split())
    test.close()
    print(SETTINGS)
    for i in SETTINGS:
        if i[0] == 'sound':
            if i[1] == '1':
                buttons_settings[0] = ('sound1.png', 200, 60, 330)
            else:
                buttons_settings[0] = ('sound0.png', 200, 60, 330)
        elif i[0] == 'musik':
            if i[1] == '1':
                buttons_settings[1] = ('musik1.png', 200, 60, 330)
            else:
                buttons_settings[1] = ('musik0.png', 200, 60, 330)


class Button(pygame.sprite.Sprite):
    # Класс Кнопки в общем виде
    def __init__(self, a, dx, dy, x, y, group):
        super().__init__(group)
        self.button_type = a
        self.image = load_image(self.button_type)
        self.image = pygame.transform.scale(self.image, (dx, dy))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        global inf
        global input_box1
        global input_box2
        # Действия при активации разных кнопок. Их отличают по названию картинки
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            if self.button_type == 'game_start.png':
                pass
            elif self.button_type == 'training.png':
                pass
            elif self.button_type == 'settings.png':
                settings()
            elif self.button_type == 'leader_board.png':
                account_login()
            elif self.button_type == 'game_stop.png':
                terminate()

            elif self.button_type == 'back.png':
                menu()

            elif self.button_type == 'sound1.png':
                self.button_type = 'sound0.png'
                self.image = load_image(self.button_type)
                self.image = pygame.transform.scale(self.image, self.rect.size)
                settings_change('sound 0')
            elif self.button_type == 'sound0.png':
                self.button_type = 'sound1.png'
                self.image = load_image(self.button_type)
                self.image = pygame.transform.scale(self.image, self.rect.size)
                settings_change('sound 1')
            elif self.button_type == 'musik1.png':
                self.button_type = 'musik0.png'
                self.image = load_image(self.button_type)
                self.image = pygame.transform.scale(self.image, self.rect.size)
                settings_change('musik 0')
            elif self.button_type == 'musik0.png':
                self.button_type = 'musik1.png'
                self.image = load_image(self.button_type)
                self.image = pygame.transform.scale(self.image, self.rect.size)
                settings_change('musik 1')

            elif self.button_type == 'confirm.png':
                account_check(input_box1.returning(),
                              input_box2.returning(),
                              inf)


def menu():
    # Отображение меню
    for i in button_group:
        i.kill()
    fon = load_image('menu_fon.png')
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
            button_group.update(event)
        button_group.draw(screen)
        pygame.display.flip()

    pygame.quit()


def settings():
    # Отображение настроек
    for i in button_group:
        i.kill()
    screen.fill('black')
    Button('back.png', 200, 70, 10, 10, button_group)
    for i in range(2):
        Button(buttons_settings[i][0], buttons_settings[i][1], buttons_settings[i][2],
               buttons_settings[i][3], 70 + 70 * i, button_group)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            button_group.update(event)
        button_group.draw(screen)
        pygame.display.flip()

    pygame.quit()


def account_login():
    # Отображение окна с входом в аккаунт
    global NICKNAME
    global input_box1
    global input_box2
    global inf
    for i in button_group:
        i.kill()
    screen.fill('black')
    # Если пользователь уже зарег., то этого окна не будет
    if not NICKNAME:
        input_box1 = InputBox(350, 300, 140, 32)
        input_box2 = InputBox(350, 400, 140, 32)
        input_boxes = [input_box1, input_box2]
        running = True

        Button('account_ask.png', 200, 70, 350, 200, button_group)
        Button('confirm.png', 200, 70, 350, 500, button_group)
        Button('back.png', 200, 70, 10, 10, button_group)

        db = sqlite3.connect("InfinityCastle_db")

        cur = db.cursor()
        inf = list(cur.execute('SELECT * FROM accounts').fetchall())
        db.close()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
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
        leader_board()


def leader_board():
    # отображение лидеров по пройденным этажам
    for i in button_group:
        i.kill()
    screen.fill('black')
    db = sqlite3.connect("InfinityCastle_db")

    cur = db.cursor()
    inf_level_board = list(cur.execute('SELECT accounts.nickname, leaderboard_level.level FROM'
                                       ' leaderboard_level LEFT JOIN accounts on accounts.Id = leaderboard_level.Id')
                           .fetchall())
    db.close()

    Button('back.png', 200, 70, 10, 10, button_group)
    
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
    with open('settings.txt', 'w') as f:
        for i in aa:
            f.write(' '.join(i) + '\n')
    load_settings()


def account_check(a, b, c):
    # Проверка существования аккаунта по базе данных при входе
    global NICKNAME
    status = False
    for i in c:
        if i[1] == a:
            if i[2] == b:
                status = True
    if status:
        print('YES')
        NICKNAME = a
        leader_board()
    else:
        print('NO')


if __name__ == '__main__':
    # Активация приложения
    load_settings()
    menu()
