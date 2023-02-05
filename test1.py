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
puddles = []
puddle_speed = -20
puddle_x = display_width

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    if len(puddles) == 0:
        toggle = random.randrange(0,3)
        puddles.append(1)
        
    if toggle == 0 or toggle == 1:
        win.blit(puddle, (puddle_x, 410))
        puddle_x += puddle_speed
        if puddle_x == 0:
            puddles=[]
            puddle_x = display_width
            print(puddles)

    if toggle == 2:
        win.blit(big_puddle, (puddle_x, 410))
        puddle_x += puddle_speed
        if puddle_x == 0:
            puddles = []
            puddle_x = display_width
            print(puddles)
        


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
