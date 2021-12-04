from types import FrameType
import pygame
import time
import random
import time
import os



frameRate = 60
windowSize = [1200,600]
scale = 8
windowPosition = [0,75]

# defining colors
black = pygame.Color(0, 0, 0)
darkPurple = pygame.Color(19,12,55)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

pygame.init()
tileset = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/tileset.png')
skelSheet = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/skeleton.png')
# background = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/preview.png')

background = pygame.transform.scale(tileset.subsurface((112,33,64,31)), (64*scale,31*scale))

treeTop = tileset.subsurface((39,39,26,26))

leftLedge = pygame.transform.scale(tileset.subsurface((72,24,7,7)), (5*7, 5*7))

regLedge = pygame.transform.scale(tileset.subsurface((80,24,7,7)), (5*7, 5*7))

regLedgePole = pygame.transform.scale(tileset.subsurface((87,24,10,7)), (5*10, 5*7))

rightLedge = tileset.subsurface((97,24,7,7))

bothLedge = tileset.subsurface((96,32,8,8))

treeTrunk = tileset.subsurface((66,48,4,16))

treeTruckBottom = pygame.transform.scale(tileset.subsurface((72,56,8,8)), (5*8, 5*8))

ladder = tileset.subsurface((72,32,8,8))

skeleton = pygame.transform.scale(skelSheet.subsurface((5,25,10,14)), (5*10, 5*14))

#The Grasses:
grass_TL = pygame.transform.scale(tileset.subsurface((8,8,8,8)), (5*8, 5*8))
grass_TC = pygame.transform.scale(tileset.subsurface((16,8,8,8)), (5*8, 5*8))
grass_TR = pygame.transform.scale(tileset.subsurface((24,8,8,8)), (5*8, 5*8))

grass_ML = pygame.transform.scale(tileset.subsurface((8,16,8,8)), (5*8, 5*8))
grass_MC = pygame.transform.scale(tileset.subsurface((16,16,8,8)), (5*8, 5*8))
grass_MR = pygame.transform.scale(tileset.subsurface((24,16,8,8)), (5*8, 5*8))

grass_BL = pygame.transform.scale(tileset.subsurface((8,24,8,8)), (5*8, 5*8))
grass_BC = pygame.transform.scale(tileset.subsurface((16,24,8,8)), (5*8, 5*8))
grass_BR = pygame.transform.scale(tileset.subsurface((24,24,8,8)), (5*8, 5*8))

game_window = pygame.display.set_mode(windowSize)
pygame.display.set_caption('2D Platformer')
fps = pygame.time.Clock()

platforms = []

def bgAndWalkways():
    # Clear canvas
    game_window.fill(black)
    # Generate Mountains
    pygame.draw.rect(game_window, darkPurple, (0,0,windowSize[0],75), 0)
    for i in range(0,4,1):
        game_window.blit(background, (i*scale*64+windowPosition[0], windowPosition[1]))
    #Generate Walkways
    game_window.blit(treeTruckBottom, (375,260))
    game_window.blit(grass_TC, (335,300))
    game_window.blit(grass_TR, (375,300))
    game_window.blit(grass_MR, (375,340))

    game_window.blit(leftLedge,(415,300))
    platforms.append([300,415,450])

    game_window.blit(regLedge,(450,300))
    platforms.append([300,450,485])

    game_window.blit(regLedgePole,(485,300))
    platforms.append([300,485,535])

    game_window.blit(regLedge,(535,300))
    platforms.append([300,535,585])


def overPlatform(midX,botY):
    counter = 0
    for i in platforms:
        # if botY <= i[0]-70 and midX >= i[1] and midX <= i[2]:
        #     over = 1
        print(midX < i[1] or midX > i[2])
        if midX < i[1] or midX > i[2]:
            # print("NOt on platform")
            counter += 1
    if(counter == len(platforms)):
        return 2
    else:
        return 0
            

def main():
    start_ticks=pygame.time.get_ticks()
    pos=229
    jump = False
    x = 450
    speed = 0
    while True: 
        seconds= round((pygame.time.get_ticks()-start_ticks)/1000,2)
        g=170
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    speed =5
                if event.key == pygame.K_LEFT:
                    speed = -5
                if event.key == pygame.K_SPACE and pos >= 230:
                    start_ticks=pygame.time.get_ticks()
                    jump = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    speed = 0
                if event.key == pygame.K_LEFT:
                    speed = 0
                    
        x += speed


        bgAndWalkways()
        pos = g*(seconds*seconds) -200*seconds +230
        test = overPlatform(x+25,pos)
        before = 0
        
        if test == 2:
            if(before == 0):
                start_ticks=pygame.time.get_ticks()
                before = 2
            game_window.blit(skeleton, (x, int(pos)))
        elif test == 1 or jump == True :
             game_window.blit(skeleton, (x, int(pos)))
             jump = False
        else:
            before = 0
            game_window.blit(skeleton, (x, 231))
            
            
        print(seconds)
       
        pygame.display.flip()
        fps.tick(frameRate)

main()