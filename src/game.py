import pygame
from func import load_image, terminate


images = []


def interface():
    pygame.init()
    screen_game = pygame.display.set_mode((1920, 1080))
    FPS = 60
    screen_game.fill('black')
    pygame.display.set_caption('Infinity Castle')
    clock = pygame.time.Clock()
    clock.tick(FPS)

    fon = load_image('background.png', 'interface')
    fon = pygame.transform.scale(fon, (1920, 1080))
    screen_game.blit(fon, (0, 0))

    coin = load_image('coin.png', 'interface')


def start():
    interface()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
        pygame.display.flip()
