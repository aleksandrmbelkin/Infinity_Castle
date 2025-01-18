import pygame as pg


pg.init()
COLOR_INACTIVE = pg.Color('White')
COLOR_ACTIVE = pg.Color('lightskyblue3')
FONT = pg.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # Контроль: активно ли поле для ввода
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Смена цвета при перемещении мыши от поля
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Рендер текста
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Увеличение коробки ввода текста при большом вводе
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Текст
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Прямоугольник
        pg.draw.rect(screen, self.color, self.rect, 2)

    def returning(self):
        return self.text
