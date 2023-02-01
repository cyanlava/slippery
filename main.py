import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 960
screen_height = 540

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Slippery')

#images
character = pygame.image.load('char.png')
red_balloon = pygame.image.load('redballoon.png')
green_baloon = pygame.image.load('greenballoon.png')
bg = pygame.image.load('bg.jpg')

character = pygame.transform.scale(character, (200, 200))



def game_loop():

    clock.tick(fps)

    #bg
    screen.blit(bg, (0, 0))
    screen.blit(character, (0, 0))

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
        pygame.display.update()


game_loop()
pygame.quit()
quit()