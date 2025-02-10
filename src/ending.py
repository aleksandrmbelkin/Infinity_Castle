import pygame
import os
import sys
from func import terminate, load_image


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
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            if self.button_type == 'start_new_game.png':
                pygame.quit()
                os.system('python game.py')
                sys.exit()
            elif self.button_type == 'menu_back.png':
                pygame.quit()
                os.system('python main.py')
                sys.exit()
            elif self.button_type == 'game_stop.png':
                terminate()


def end():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    screen.fill('Black')

    font = pygame.font.Font(None, 32)
    text = ['Вы погибли, ваш путь окончен...', 'Количество пройденных этажей: ' + 'text']
    text_coord = 10

    button_group = pygame.sprite.Group()
    Button('start_new_game.png', 300, 50, 100, 100, button_group)
    Button('menu_back.png', 250, 50, 120, 160, button_group)
    Button('game_stop.png', 250, 50, 120, 220, button_group)
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            button_group.update(event)

        button_group.draw(screen)

        pygame.display.flip()
