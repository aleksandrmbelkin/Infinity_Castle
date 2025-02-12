import os
import sys
import pygame
from func import load_image

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

    def update(self):
        if self.animation_flag and self.animation < self.max_animation:
            self.animation += 1
        
            self.image_fin = load_image(f'{self.image}{self.animation}.png', self.where)
            self.image_fin = pygame.transform.scale(self.image_fin, (self.width, self.height))

    def used(self):
        self.image_fin = load_image(f'{self.image}{self.max_animation}.png', self.where)
        self.image_fin = pygame.transform.scale(self.image_fin, (self.width, self.height))

        
def load_im(im, where):
    fullname = os.path.join(fr'data\pictures\{where}', f'{im[0]}.png')
    
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    image = pygame.transform.scale(image, (im[1], im[2]))
    return image


pygame.init()

# Создание экрана
screen_game = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption('Infinity Castle')

# Поля для монет и маны
field_for_coin_long = load_im(['field_for_coin', 250, 60], 'interface')
field_for_coin_short = load_im(['field_for_coin', 200, 60], 'interface')

# Хп
hp_states = [load_im(['filled_cell_HP', 60, 52], 'interface'), 
             load_im(['unfilled_cell_HP', 60, 52], 'interface'),
             load_im(['loced_HP', 30, 40], 'interface')]

# Двери
doors_open = [load_im(['doors/door_open_up', 100, 85], 'map'), 
              load_im(['doors/door_open_down', 100, 85], 'map'),
              load_im(['doors/door_open_left', 85, 100], 'map'),
              load_im(['doors/door_open_right', 85, 100], 'map')]

doors_close = [load_im(['doors/door_close_up', 100, 85], 'map'), 
              load_im(['doors/door_close_down', 100, 85], 'map'),
              load_im(['doors/door_close_left', 85, 100], 'map'),
              load_im(['doors/door_close_right', 85, 100], 'map')]

# Картинки объектов
em_room = load_im(['empty_room', 1355, 660], 'map') # Пустая
big_door = load_im(['doors/big_door', 400, 100], 'map') # Дверь в начальной комнате 1 уровня
stairs_image = load_im(['stairs/up', 120, 120], 'map') # Лестница в начальной комнате
text_field = load_im(['text_field', 740, 140], 'interface') # Поле для текста

# Коллизии объектов
# Комнаты магазинов
trader_shop = Object('shop_', 'map/traders', 1170, 370, 240, 200, 0)
trader_upgrade = Object('upgrade_shop_', 'map/traders', 1170, 370, 240, 200, 0)

table_1 = Object('table_', 'map', 500, 520, 100, 100, 0)
table_2 = Object('table_', 'map', 700, 285, 100, 100, 0)
table_3 = Object('table_', 'map', 900, 520, 100, 100, 0)

# Комната жизни
death = Object('death_com_', 'map/life_room', 1120, 230, 300, 240, 0)

table_life_1 = Object('table_', 'map', 500, 520, 100, 100, 0)
table_life_2 = Object('table_', 'map', 700, 285, 100, 100, 0)
table_life_3 = Object('table_', 'map', 900, 520, 100, 100, 0)

dark_sphere_1 = Object('dark_sphere_', 'map/life_room', 513, 515, 70, 70, 0)
dark_sphere_2 = Object('dark_sphere_', 'map/life_room', 713, 280, 70, 70, 0)
dark_sphere_3 = Object('dark_sphere_', 'map/life_room', 913, 515, 70, 70, 0)

# Аркадная комната
automat = Object('arсada_', 'map', 905, 420, 150, 200, 0)

# Конечная комната
stairs = Object('down_', 'map/stairs', 1350, 195, 200, 200, 0)