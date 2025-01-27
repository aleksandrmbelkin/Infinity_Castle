import pygame
import os
import sys
import random


def terminate():
    pygame.quit()
    sys.exit()


def show_image(image, screen_game, where):
    im = load_image(f'{image[0]}.png', where)
    im = pygame.transform.scale(im, (image[3], image[4]))
    screen_game.blit(im, (image[1], image[2]))


def load_image(name, where, colorkey=None):
    fullname = os.path.join(fr'data\pictures\{where}', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

# Генерация карты
def count_rooms(map_list, room): # Подсчет определенных комнат
    how_many = 0
    if room == 'special_room':
        for lst in map_list:
            for i in lst:
                if i in ['chest', 'shop', 'upgrade_shop', 'arcada', 'life_room']:
                    how_many += 1
    else:
        for lst in map_list:
            how_many += lst.count(room)
    return how_many


def room_generation(map_list, level, how_many_rooms, i): # Выбор комнаты по критериям
    if i == how_many_rooms:
        if level % 10 != 0:
            return 'end'
        else:
            return 'boss'
    else:
        while True:
            chance = random.random()
            if chance <= 0.50 and count_rooms(map_list, 'monsters') < how_many_rooms - 2:
                return 'monsters'
            elif (0.50 < chance <= 0.75 and count_rooms(map_list, 'chest') < 1
                  and count_rooms(map_list, 'special_room') < how_many_rooms * 0.5):
                return 'chest'
            elif (0.75 < chance <= 0.85 and count_rooms(map_list, 'shop') < 1
                  and count_rooms(map_list, 'special_room') < how_many_rooms * 0.5):
                return 'shop'
            elif (0.85 < chance <= 0.9 and count_rooms(map_list, 'upgrade_shop') < 1
                  and count_rooms(map_list, 'special_room') < how_many_rooms * 0.5):
                return 'upgrade_shop'
            elif (0.9 < chance <= 0.95 and count_rooms(map_list, 'arcada') < 1
                  and count_rooms(map_list, 'special_room') < how_many_rooms * 0.5):
                return 'arcada'
            elif (0.95 < chance < 1 and count_rooms(map_list, 'life_room') < 1
                  and count_rooms(map_list, 'special_room') < how_many_rooms * 0.5):
                return 'life_room'


def map_generation(level, map_size): # Генерация карты
    how_many_rooms = random.randint(4, 7)
    map_list = [['no'] * map_size for _ in range(map_size)]

    # Генерация начальной комнаты
    cell = [random.randrange(0, 4), random.randrange(0, 4)]
    if level == 1:
        cell = [0, 0]
        map_list[cell[0]][cell[1]] = 'door_start'
    else:
        map_list[cell[0]][cell[1]] = 'start'

    start_cell = cell[::]

    # Генерация остальных комнат
    for i in range(how_many_rooms + 1):
        while True:
            where = random.randrange(0, 4)
            if where == 0:
                if cell[0] - 1 >= 0:
                    cell[0] -= 1
                    if map_list[cell[0]][cell[1]] == 'no':
                        map_list[cell[0]][cell[1]] = room_generation(
                            map_list, level, how_many_rooms, i)
                        break

            elif where == 1:
                if cell[0] + 1 < map_size:
                    cell[0] += 1
                    if map_list[cell[0]][cell[1]] == 'no':
                        map_list[cell[0]][cell[1]] = room_generation(
                            map_list, level, how_many_rooms, i)
                        break

            elif where == 2:
                if cell[1] - 1 >= 0:
                    cell[1] -= 1
                    if map_list[cell[0]][cell[1]] == 'no':
                        map_list[cell[0]][cell[1]] = room_generation(
                            map_list, level, how_many_rooms, i)
                        break

            else:
                if cell[1] + 1 < map_size:
                    cell[1] += 1
                    if map_list[cell[0]][cell[1]] == 'no':
                        map_list[cell[0]][cell[1]] = room_generation(
                            map_list, level, how_many_rooms, i)
                        break
    
    for i in range(len(map_list)):
        for k in range(len(map_list[i])):
            map_list[i][k] = [map_list[i][k], 'unvisited']

    return map_list, start_cell
# -------------------------------------------------------------------------
