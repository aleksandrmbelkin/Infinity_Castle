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

        self.image_fin = load_im([f'{image}{self.animation}', self.width, self.height], where)
        self.mask = pygame.mask.from_surface(self.image_fin)
        self.rect = self.image_fin.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.animation_flag and self.animation < self.max_animation:
            self.animation += 1
            self.image_fin = load_im([f'{self.image}{self.animation}', self.width, self.height], self.where)

    def used(self):
        self.image_fin = load_im([f'{self.image}{self.max_animation}', self.width, self.height], self.where)

        
def load_im(im, where):
    fullname = os.path.join(f'data/pictures/{where}', f'{im[0]}.png')
    
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    image = pygame.transform.scale(image, (im[1], im[2]))
    return image


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
text_field = load_im(['text_field', 710, 140], 'interface') # Поле для текста

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
#-----------------------------------------------------------------------------------

# Монстры:
    # Рыцарь:
        # Лево
enemy_knight_left_0 = load_im(['left/jump_0', 150, 120], 'characters/monsters/enemy_knight')
enemy_knight_left_1 = load_im(['left/jump_1', 150, 120], 'characters/monsters/enemy_knight')
enemy_knight_left_2 = load_im(['left/jump_2', 150, 120], 'characters/monsters/enemy_knight')
enemy_knight_left_3 = load_im(['left/jump_3', 150, 120], 'characters/monsters/enemy_knight')
enemy_knight_left_4 = load_im(['left/jump_4', 150, 120], 'characters/monsters/enemy_knight')
enemy_knight_left_5 = load_im(['left/jump_5', 150, 120], 'characters/monsters/enemy_knight')
        # Право
enemy_knight_right_0 = load_im(['right/jump_0', 150, 120], 'characters/monsters/enemy_knight')
enemy_knight_right_1 = load_im(['right/jump_1', 150, 120], 'characters/monsters/enemy_knight')
enemy_knight_right_2 = load_im(['right/jump_2', 150, 120], 'characters/monsters/enemy_knight')
enemy_knight_right_3 = load_im(['right/jump_3', 150, 120], 'characters/monsters/enemy_knight')
enemy_knight_right_4 = load_im(['right/jump_4', 150, 120], 'characters/monsters/enemy_knight')
enemy_knight_right_5 = load_im(['right/jump_5', 150, 120], 'characters/monsters/enemy_knight')

    # Скелет:
        # Лево
            # Движение
skeleton_left_0 = load_im(['left/walk_0', 150, 120], 'characters/monsters/skeletons/skeleton')
skeleton_left_1 = load_im(['left/walk_1', 150, 120], 'characters/monsters/skeletons/skeleton')
skeleton_left_2 = load_im(['left/walk_2', 150, 120], 'characters/monsters/skeletons/skeleton')
skeleton_left_3 = load_im(['left/walk_3', 150, 120], 'characters/monsters/skeletons/skeleton')
skeleton_left_4 = load_im(['left/walk_4', 150, 120], 'characters/monsters/skeletons/skeleton')
skeleton_left_5 = load_im(['left/walk_5', 150, 120], 'characters/monsters/skeletons/skeleton')
skeleton_left_6 = load_im(['left/walk_6', 150, 120], 'characters/monsters/skeletons/skeleton')
            # Атака
skeleton_left_atack_0 = load_im(['left/attack_0', 150, 120], 'characters/monsters/skeletons/skeleton')
skeleton_left_atack_1 = load_im(['left/attack_1', 150, 120], 'characters/monsters/skeletons/skeleton')
skeleton_left_atack_2 = load_im(['left/attack_2', 150, 120], 'characters/monsters/skeletons/skeleton')
skeleton_left_atack_3 = load_im(['left/attack_3', 150, 120], 'characters/monsters/skeletons/skeleton')
skeleton_left_atack_4 = load_im(['left/attack_4', 150, 120], 'characters/monsters/skeletons/skeleton')
        # Право
            # Движение
skeleton_right_0 = load_im(['right/walk_0', 150, 120], 'characters/monsters/skeletons/skeleton')
skeleton_right_1 = load_im(['right/walk_1', 150, 120], 'characters/monsters/skeletons/skeleton')
skeleton_right_2 = load_im(['right/walk_2', 150, 120], 'characters/monsters/skeletons/skeleton')
skeleton_right_3 = load_im(['right/walk_3', 150, 120], 'characters/monsters/skeletons/skeleton')
skeleton_right_4 = load_im(['right/walk_4', 150, 120], 'characters/monsters/skeletons/skeleton')
skeleton_right_5 = load_im(['right/walk_5', 150, 120], 'characters/monsters/skeletons/skeleton')
skeleton_right_6 = load_im(['right/walk_6', 150, 120], 'characters/monsters/skeletons/skeleton')
            # Атака
skeleton_right_atack_0 = load_im(['right/attack_0', 150, 120], 'characters/monsters/skeletons/skeleton')
skeleton_right_atack_1 = load_im(['right/attack_1', 150, 120], 'characters/monsters/skeletons/skeleton')
skeleton_right_atack_2 = load_im(['right/attack_2', 150, 120], 'characters/monsters/skeletons/skeleton')
skeleton_right_atack_3 = load_im(['right/attack_3', 150, 120], 'characters/monsters/skeletons/skeleton')
skeleton_right_atack_4 = load_im(['right/attack_4', 150, 120], 'characters/monsters/skeletons/skeleton')

    # Скелет-лучник
        # Стрела
arrow = load_im(['arrow', 60, 10], 'characters/monsters/skeletons/archer')
        # Лево
archer_left_atack_0 = load_im(['left/attack_0', 150, 120], 'characters/monsters/skeletons/archer')
archer_left_atack_1 = load_im(['left/attack_1', 150, 120], 'characters/monsters/skeletons/archer')
archer_left_atack_2 = load_im(['left/attack_2', 150, 120], 'characters/monsters/skeletons/archer')
archer_left_atack_3 = load_im(['left/attack_3', 150, 120], 'characters/monsters/skeletons/archer')
archer_left_atack_4 = load_im(['left/attack_4', 150, 120], 'characters/monsters/skeletons/archer')
archer_left_atack_5 = load_im(['left/attack_5', 150, 120], 'characters/monsters/skeletons/archer')
archer_left_atack_6 = load_im(['left/attack_6', 150, 120], 'characters/monsters/skeletons/archer')
archer_left_atack_7 = load_im(['left/attack_7', 150, 120], 'characters/monsters/skeletons/archer')
        # Право
archer_right_atack_0 = load_im(['right/attack_0', 150, 120], 'characters/monsters/skeletons/archer')
archer_right_atack_1 = load_im(['right/attack_1', 150, 120], 'characters/monsters/skeletons/archer')
archer_right_atack_2 = load_im(['right/attack_2', 150, 120], 'characters/monsters/skeletons/archer')
archer_right_atack_3 = load_im(['right/attack_3', 150, 120], 'characters/monsters/skeletons/archer')
archer_right_atack_4 = load_im(['right/attack_4', 150, 120], 'characters/monsters/skeletons/archer')
archer_right_atack_5 = load_im(['right/attack_5', 150, 120], 'characters/monsters/skeletons/archer')
archer_right_atack_6 = load_im(['right/attack_6', 150, 120], 'characters/monsters/skeletons/archer')
archer_right_atack_7 = load_im(['right/attack_7', 150, 120], 'characters/monsters/skeletons/archer')
#--------------------------------------------

# Интерфейс
images = [['coin', 1330, 105, 70, 70], ['magic_frame', 470, 860, 120, 120], ['weapon_frame', 310, 855, 125, 125],
     ['unfilled_HP', 605, 860, 720, 125], ['mana_bar', 300, 100, 60, 80]]

fon = load_im(['background', 1920, 1980], 'interface')

interface_images = []
for image in images:
    im = load_im([image[0], image[3], image[4]], 'interface')
    interface_images.append([im, image[1], image[2]])

# Арки удара некроманта
arc0 = load_im(['arc0', 100, 50], 'characters/bosses/necromancer')
arc1 = load_im(['arc1', 100, 50], 'characters/bosses/necromancer')
# # Спрайты фантомного скелета
# summoned_skeleton_images = [load_im('skeleton_attack' + str(i), 
#                             'characters/bosses/necromancer') for i in range(3)]
# # Спрайты фантомного взрыва
# summoned_flame_images = [load_im('boom' + str(i), 
#                          'characters/bosses/necromancer') for i in range(4)]
