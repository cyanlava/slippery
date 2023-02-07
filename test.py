import pygame
import random
import math
from pygame import mixer


pygame.init()


#resolution
resolution = 2
#short for
r = resolution

#display
display_width = 960*r
display_height = 540*r
win = pygame.display.set_mode((display_width, display_height))
overrun = True
while overrun == True:
    #menu variables
    counter = 0
    counter_offset = display_width - 60
    counter_check = 0
    check_tmp = 1

    #character and movement variables
    x = 150*r
    y = 300*r
    vel_y = 10
    jump = False
    scroll = 0
    scroll_bg = 0
    hearts = 2
    heart_frame = 0
    heart_frame_time = 0
    invincible = False
    invincibility_frames = 16
    start = False
    yvel, xvel = 0, 0
    firerate = 0
    balloon_frames = 0
    balloon_frame_time = 0
    bal_velocity = 0
    bal_loc = display_width
    bal_locy = 180*r
    bal_locz = bal_loc
    bal_locyz = bal_locy

    #puddle variables
    x_pud = 400*r
    y_pud = 410*r
    #puddles refers to list of positions
    puddles = []
    puddle_speed = -20*r
    puddle_x = display_width
    tog = 1

    char_frames = ['char1.png','char2.png','char3.png','char4.png','char5.png','char6.png','char7.png','char8.png']

    def loadify(img):
        return pygame.image.load(img).convert_alpha()

    #sprites
    character = pygame.image.load('char1.png')

    bg = loadify('bg.png')
    bg = pygame.transform.scale(bg, (display_width, display_height))
    puddle = pygame.image.load('puddle.png')
    path = loadify('path.png')
    path = pygame.transform.scale(path, (display_width, display_height))
    beach = loadify('beach.png')
    beach = pygame.transform.scale(beach, (display_width, display_height))
    watergun = loadify('watergun.png')
    watergun = pygame.transform.scale(watergun, (42*r, 38*r))
    cursor = loadify('cursor.png')
    cursor = pygame.transform.scale(cursor, (10*r, 15*r))
    droplet = loadify('droplet.png')
    droplet = pygame.transform.scale(droplet, (20*r, 20*r))
    key1 = loadify('key1.png')
    key1 = pygame.transform.scale(key1, (295*r, 95*r))
    key2 = loadify('key2.png')
    key2 = pygame.transform.scale(key2, (295*r, 100*r))



    character = pygame.transform.scale(character, (140*r, 140*r))
    puddle = pygame.transform.scale(puddle, (112*r, 30*r))
    big_puddle = pygame.transform.scale(puddle, (180*r, 30*r))

    #list of types of puddles
    types = [puddle, puddle, big_puddle]



    #functions
    font = pygame.font.SysFont("arialblack", 40)
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        win.blit(img, (x, y))




    bullets=[]
    frame = 0
    frame_time = 0
    fail = False
    run = True
    tmp = 0
    xloc, yloc = 0, 0
    red = False
    green = False
    red_pop = False
    green_pop = False
    ticks = 0
    danger = False

    mixer.music.load('sines.wav')
    mixer.music.play(-1)
    jump_sound = mixer.Sound('jump.wav')
    heartloss_sound = mixer.Sound('heartloss.wav')
    crash_sound = mixer.Sound('crash.wav')
    pop_sound = mixer.Sound('pop.wav')
    spurt_sound = mixer.Sound('spurt.wav')

    textfont = pygame.font.SysFont("terminal", 50*r)


    while run:
        win.fill((255,255,255))
        ticks+=1

        #background scroll
        win.blit(bg, (scroll_bg, 0))
        win.blit(bg, (display_width+scroll_bg, 0))
        if scroll_bg == -display_width:
            win.blit(bg, (display_width+scroll_bg, 0))
            scroll_bg = 0
        if fail is False:
            scroll_bg -= 3*r
        #tracks and beach scroll
        win.blit(beach, (scroll, 0))
        win.blit(beach, (display_width+scroll, 0))
        win.blit(path, (scroll, 0))
        win.blit(path, (display_width+scroll, 0))
        if scroll == -display_width:
            win.blit(beach, (display_width+scroll, 0))
            win.blit(path, (display_width+scroll, 0))
            scroll = 0
        if fail is False:
            scroll -= 20*r

        #balloons
        red_frames = ['rd1.png', 'rd2.png']
        if balloon_frame_time % 70 == 0:
            balloon_frames+=1
        if balloon_frames == 2:
            balloon_frames= 0
            red_pop is False
            green_pop is False
        balloon_frame_time+=1

        if not red_pop:
            red_balloon = loadify('redballoon.png')

        bal = 2
        if ticks%120 == 0:
            if red is False:
                bal = random.randrange(0,3)
                if bal == 0 or bal == 1:
                    red = True
        if red:
            red_balloon = pygame.transform.scale(red_balloon, (65*r, 115*r))
            win.blit(red_balloon, (bal_loc, bal_locy))
            if fail is False:
                bal_loc += puddle_speed
                if bal_loc < -65*r:
                    bal_loc = display_width
                    red = False
            if fail is True:
                bal_locy += puddle_speed
        
        if red_pop:
            red = False
            red_balloon = loadify(red_frames[balloon_frames])
            red_balloon = pygame.transform.scale(red_balloon, (65*r, 115*r))
            win.blit(red_balloon, (bal_loc, bal_locy))
            if fail is False:
                bal_loc += puddle_speed/4
                if bal_loc < -65*r:
                    bal_loc = display_width
                    red_pop = False

        #green
        green_frames = ['gb1.png', 'gb2.png']
        danger_frames = ['rb1.png', 'rb2.png']

        if not green_pop:
            green_balloon = loadify('greenballoon.png')

        ballo = 2

        if ticks % 140 == 0:
            if green is False:
                ballo = random.randrange(0,3)
                if ballo == 0 or ballo == 1:
                    green = True

        if danger:
            green_balloon = loadify(danger_frames[balloon_frames])
            green_balloon = pygame.transform.scale(green_balloon, (80*r, 140*r))
            win.blit(green_balloon, (bal_locz, bal_locyz))
            if not invincible:
                hearts-=1
                if hearts == 1:
                        heartloss_sound.play()
                        invincible = True
                if bal_locz < -80*r:
                    bal_locz = display_width
                    danger = False
        if green:
            green_balloon = pygame.transform.scale(green_balloon, (80*r, 140*r))
            win.blit(green_balloon, (bal_locz, bal_locyz))
            if fail is False:
                bal_locz += puddle_speed
                if bal_locz > 140*r and bal_locz< 220*r:
                    pop_sound.play()
                    danger = True
            if fail is True:
                bal_locyz += puddle_speed
        
        if green_pop:
            green = False
            green_balloon = loadify(green_frames[balloon_frames])
            green_balloon = pygame.transform.scale(green_balloon, (80*r, 140*r))
            win.blit(green_balloon, (bal_locz, bal_locyz))
            if fail is False:
                bal_locz += puddle_speed/4
                if bal_locz < -80*r:
                    bal_locz = display_width
                    green_pop = False

                

        if hearts == 2:
            invincible is False
        if invincible is True:
            invincibility_frames -=1
            if invincibility_frames == 0:
                invincibility_frames = 16
                invincible = False

        char_frames = ['char1.png','char2.png','char3.png','char4.png','char5.png','char6.png','char7.png','char8.png']
        if frame == 8:
            frame = 0

        character = pygame.image.load(char_frames[frame])
        if frame_time % 3 == 0:
            frame_time = 0
            frame+=1
        frame_time+=1
        
        character = pygame.transform.scale(character, (140*r, 140*r))

        #counter
        text1 = textfont.render(str(counter), 1, (255, 255, 255))
        if counter_check % (10 * check_tmp) == 0 and counter_check != 0:
            counter_check = 0
            counter_offset-=30
            check_tmp = check_tmp * 10
        win.blit(text1, (counter_offset , 60))
        


        if hearts ==  2:
            heart_frames = ['heart.png', 'heart2.png', 'heart3.png']
            if heart_frame == 3:
                heart_frame = 0
            heart = pygame.image.load(heart_frames[heart_frame])
            if heart_frame_time % 16 == 0:
                heart_frame_time = 0
                heart_frame+=1
            heart_frame_time+=1
            heart = pygame.transform.scale(heart, (80*r, 80*r))
            win.blit(heart, (60, 60))
        if hearts == 0:
            crash_sound.play()
            fail = True
            hearts = -1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                overrun = False


        if len(puddles) == 0:
            puddles.append([display_width, random.choice(types)])
            print(ticks)

        if tog == 1:
            puddles.append([display_width, random.choice(types)])
        tog = 0
        

        dip = False
        dip2 = False
        delete = []
        for i in range(len(puddles)):
            #type, position
            win.blit(puddles[i][1], (puddles[i][0], 410*r))
            if fail is False:

                puddles[i][0] = puddles[i][0] + puddle_speed



                if puddles[i][1] == puddle:
                    if puddles[i][0] <= 240*r and puddles[i][0] >= x - 112*r:
                        if y+140*r >= 410*r:
                            if not invincible:
                                hearts-=1
                                if hearts == 1:
                                    heartloss_sound.play()
                                    invincible = True
                        
                        
                    if puddles[i][0] == -120*r:
                        puddles.pop(i)
                        counter+=1
                        counter_check+=1
                        dip = True
                        break
                if puddles[i][1] == big_puddle:
                    if puddles[i][0] <= 240*r and puddles[i][0] >= x - 180*r:
                        if y+140*r >= 410*r:
                            if not invincible:
                                hearts-=1
                                if hearts == 1:
                                    heartloss_sound.play()
                                    invincible = True
                
                    if puddles[i][0] == -180*r:
                        puddles.pop(i)
                        counter+=1
                        counter_check+=1
                        dip = True
                        break
                if puddles[i][0] == display_width * (1/4):
                    tog = random.randrange(0, 2)

            #workaround for popping second puddle
            if dip is True:
                for i in range(len(puddles)):
                    win.blit(puddles[i][1], (puddles[i][0], 410*r))

        userInput = pygame.key.get_pressed()
                
        if fail is True:
            character = pygame.image.load('char_fail.png')
            character = pygame.transform.scale(character, (140*r, 140*r))
            text2 = textfont.render("Kliknij Spacje by kontynuować", 1, (255, 255, 255))
            win.blit(text2, (200*r , 150*r))
            if ticks % 100 >= 0 and ticks % 100 < 50:
                win.blit(key1, (display_width/2 - 295*r/2 , 250*r))
            else:
                win.blit(key2, (display_width/2 - 295*r/2 , 245*r))
            
            if userInput[pygame.K_SPACE]:
                run = False
                

        
        # Movement
        userInput = pygame.key.get_pressed()

        if jump is False and fail is False and userInput[pygame.K_SPACE]:
            jump = True
        if jump is True:
            if y == 300*r:
                jump_sound.play()
            y -= vel_y*4*r
            vel_y -= 1
            if vel_y < -10:
                jump = False
                vel_y = 10
        win.blit(cursor, pygame.mouse.get_pos())
        win.blit(character, (x, y))
        if not fail:
            watergun_pos = (x+100*r, y+50*r)
            #print(watergun_pos)
            watergun_rect = watergun.get_rect(center = watergun_pos)

            mx, my = pygame.mouse.get_pos()
            dx, dy = mx - watergun_rect.centerx, my - watergun_rect.centery
            angle = math.degrees(math.atan2(-dy, dx))
            #print(angle)
            rot_image      = pygame.transform.rotate(watergun, angle)
            rot_image_rect = rot_image.get_rect(center = watergun_rect.center)
            #shooting
            velocity = 20*r
            yvel = math.sin(math.radians(angle)) * velocity
            xvel = math.cos(math.radians(angle)) * velocity
            firerate += 1
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0] and len(bullets) < 4 and firerate % 4 == 0:
                spurt_sound.play()
                bullets.append([xvel, yvel, xloc, yloc, 1])
                firerate = 0
            
            
            for j in range(len(bullets)):
            
                win.blit(droplet, (bullets[j][2], bullets[j][3]))
                if bullets[j][4] == 1:
                    bullets[j][2] = x+100*r
                    bullets[j][3] = y+50*r
                    bullets[j][4] = 0
                if bullets[j][4] == 0:
                    bullets[j][2] += bullets[j][0]
                    bullets[j][3] -= bullets[j][1]
                    bullets[j][1] -=1
                if bullets[j][2] <= 0 or bullets[j][2] >= display_width or bullets[j][3] <= 0 or bullets[j][3] >= display_height:
                    bullets.pop(j)
                    dip2 = True
                    break
                if bullets[j][2] + 20*r > bal_loc and bullets[j][2] - 20*r < bal_loc + 65*r:
                    if bullets[j][3] + 20*r > bal_locy and bullets[j][3] -20*r < bal_locy + 65*r:
                        pop_sound.play()
                        if hearts == 1:
                            hearts+=1
                            invincible = False
                        if not red_pop:
                            bullets.pop(j)
                        red_pop = True
                        dip2 = True
                        break
                if bullets[j][2] + 20*r > bal_locz and bullets[j][2] - 20*r < bal_locz + 80*r:
                    if bullets[j][3] + 20*r > bal_locyz and bullets[j][3] -20*r < bal_locyz + 80*r:
                        pop_sound.play()
                        if not green_pop:
                            bullets.pop(j)
                        green_pop = True
                        dip2 = True
                        break
            if dip2 is True:
                for j in range(len(bullets)):
                    win.blit(droplet, (bullets[j][2], bullets[j][3]))
                

    
            
            win.blit(rot_image, rot_image_rect.topleft)
        if resolution == 1:
            pygame.time.delay(8)
        pygame.display.flip()
        pygame.time.Clock().tick(120)

   
