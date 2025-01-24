import pygame
from func import load_image, terminate


def show_image(image):
    im = load_image(f'{image[0]}.png', 'interface')
    im = pygame.transform.scale(im, (image[3], image[4]))
    screen_game.blit(im, (image[1], image[2]))


def interface():
    pygame.init()
    images = [['coin', 1330, 105, 70, 70], ['magic_frame', 1335, 860, 120, 120],
              ['magic_frame', 1495, 860, 120, 120], ['weapon_frame', 300, 860, 125, 125],
              ['weapon_frame', 470, 860, 125, 125], ['unfilled_HP', 605, 860, 720, 125],
              ['mana_bar', 300, 100, 60, 80], ['field_for_coin', 1420, 110, 200, 60],
              ['field_for_coin', 370, 110, 250, 60]]

    fon = load_image('background.png', 'interface')
    fon = pygame.transform.scale(fon, (1920, 1080))
    screen_game.blit(fon, (0, 0))

    pygame.draw.rect(screen_game, pygame.Color('black'), (275, 185, 1365, 670))
    pygame.draw.rect(screen_game, pygame.Color('white'), (280, 190, 1355, 660))

    for i in images:
        show_image(i)


def update_hp_mana_coins(*hp_states, **characteristics):
    coin_font = pygame.font.Font('data/shrifts/coins_shrift.ttf', 50)
    coin_text = coin_font.render(str(characteristics['coins']), False, (20, 20, 20))
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
        show_image(hp_states[0])

    for i in range(10 - characteristics['hp']):
        hp_states[1][1] = 1219 - i * 64
        show_image(hp_states[1])

    for i in range(10 - characteristics['unlocked_hp']):
        hp_states[2][1] = 1235 - i * 64
        show_image(hp_states[2])


def start():
    global screen_game
    screen_game = pygame.display.set_mode((1920, 1080))
    FPS = 60
    screen_game.fill('black')
    pygame.display.set_caption('Infinity Castle')
    clock = pygame.time.Clock()

    characteristics = {'coins': 0,
                       'hp': 4,
                       'unlocked_hp': 4,
                       'mana': 50,
                       'unlocked_mana': 50}
    
    hp_states = [['filled_cell_HP', 643, 897, 60, 52], 
                 ['unfilled_cell_HP', 1219, 897, 60, 52],
                 ['loced_HP', 1235, 903, 30, 40]]

    interface()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
        
        update_hp_mana_coins(*hp_states, **characteristics)

        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()
