import pygame
import random
import time

pygame.init()

#display
display_width = 960
display_height = 540
win = pygame.display.set_mode((display_width, display_height))

#character and movement variables
x = 150
y = 300
vel_y = 10
jump = False

#puddle variables
x_pud = 400
y_pud = 410

#sprites
character = pygame.image.load('char.png')
red_balloon = pygame.image.load('redballoon.png')
green_baloon = pygame.image.load('greenballoon.png')
bg = pygame.image.load('bg.jpg')
puddle = pygame.image.load('puddle.png')

character = pygame.transform.scale(character, (140, 140))
puddle = pygame.transform.scale(puddle, (112, 30))
big_puddle = pygame.transform.scale(puddle, (180, 30))


#functions
def char(x,y):
    win.blit(character, (x, y))

def puddle_small(x, y):
    win.blit(puddle, (x, y))


run = True
while run:
    win.fill((0, 0, 0))
    win.blit(character, (x, y))
    win.blit(puddle, (x_pud, y_pud))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Movement
    userInput = pygame.key.get_pressed()

    if jump is False and userInput[pygame.K_SPACE]:
        jump = True
    if jump is True:
        y -= vel_y*4
        vel_y -= 1
        if vel_y < -10:
            jump = False
            vel_y = 10

    pygame.time.delay(30)
    pygame.display.update()
