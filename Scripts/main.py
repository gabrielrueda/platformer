import pygame
from pygame.locals import *
import os
import math
import spriteData
import menus

# NOTE: The level data file format is...
#       ledgeType, pos x, pos y, size x, size y
 
pygame.init()
pygame.font.init() 
vec = pygame.math.Vector2  # 2 for two dimensional

#Colours
black = pygame.Color(0, 0, 0)
darkPurple = pygame.Color(19,12,55)
red = pygame.Color(254, 0, 3)
green = pygame.Color(148, 255, 194)
blue = pygame.Color(0, 0, 255)
# empty = pygame.Color(255,255,255,0)

# Global Constants
HEIGHT = 608
WIDTH = 1216 
FRIC = -0.2
FPS = 60
ACC = 0.4


# Global Variables
# moveRight = False
# moveLeft = False
imgScale = 4
itemScale = 3
bgScale = 8
FramePerSec = pygame.time.Clock()

# Music
pygame.mixer.init()
pygame.mixer.music.load(os.getcwd() + '/Assets/sounds/gamemusic2.mp3')


#Font Variables
font = pygame.font.Font(os.path.dirname(os.getcwd()) + '/platformer/Assets/font2.TTF', 16)
# font = pygame.font.SysFont('Comic Sans MS', 20)


# Sprite Sheets
skelSheet = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/tilesets/skeleton.png')
tileset = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/tilesets/tileset.png')
items = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/tilesets/items.png')

# Images from Sprite Sheet
skeleton = pygame.transform.scale(skelSheet.subsurface((4,25,11,14)), (imgScale*10, imgScale*14))
regLedge = pygame.transform.scale(tileset.subsurface((80,24,7,7)), (imgScale*7, imgScale*7))


background = pygame.transform.scale(tileset.subsurface((112,33,64,31)), (64*bgScale,31*bgScale))

lvlOutline = [
    pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/bg.png'),(WIDTH,HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/bgLVL2.png'),(WIDTH,HEIGHT)), 
]




# NOT USED HERE:

# itemArray = [
#     pygame.transform.scale(items.subsurface((16,16,16,16)), (itemScale*16, itemScale*16)),
#     pygame.transform.scale(items.subsurface((32,16,16,16)), (itemScale*16, itemScale*16)), 
# ]


pygame.mixer.music.play(-1)



# Initalize Surface
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


# Go Through Menus
while menus.update(displaysurface,FramePerSec,FPS) == False:
    pass

while menus.levelSelector(displaysurface,FramePerSec,FPS) == False:
    pass


def addText():
    i = 0
    for it in spriteData.indicatorGroup:
        txt = font.render((str(spriteData.itemsToGet[it.imgNum])+ "/" + str(it.amount)),False, it.color)
        displaysurface.blit(txt, (it.rect.left+40,it.rect.top+4))
        i += 1

count = 0



# level = 0

for level in range(0,2):
    spriteData.initSprites(level)

    while True:
        accel = vec(0,0.5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # FOR JUMPING
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    spriteData.playerSprite.jump()

        count += 1


        # FOR MOVEMENT: LEFT, RIGHT & BOOST
        keys = pygame.key.get_pressed()

        if keys[K_c]:
            ACC = 0.7
        else:
            ACC = 0.4

        if keys[K_RIGHT]:
            accel.x = ACC
            if count %5 == 0:
                spriteData.playerSprite.animate(2)
        elif keys[K_LEFT]:
            accel.x = -ACC
            if count %5 == 0:
                spriteData.playerSprite.animate(0)
        else:
            if count %10 == 0:
                spriteData.playerSprite.animate(1)



        if count%5 == 0:
            for humans in spriteData.humanSprite:
                humans.animate()


        spriteData.playerSprite.update(accel)

        displaysurface.fill(black)

        for human in spriteData.humanSprite:
            human.update()


        # Background is the mountatins and sky
        pygame.draw.rect(displaysurface, darkPurple, (0,0,WIDTH,75), 0)
        for i in range(0,4,1):
            displaysurface.blit(background, (i*bgScale*64, 75))


        # Level outline will show the trees, bushes, etc..
        displaysurface.blit(lvlOutline[level], (0, 0))

        #Draw Health Bar
        pygame.draw.rect(displaysurface, red, (spriteData.healthBar.rect.left+60, spriteData.healthBar.rect.top+25,157*(spriteData.playerSprite.health/100),15))


        for spear in spriteData.spearGroup:
            spear.update()

        spriteData.all_sprites.draw(displaysurface)

        addText()

        pygame.display.update()

        if spriteData.playerSprite.health <= 0:
            break

        if spriteData.itemsToGet.count(0) == len(spriteData.itemsToGet):
            break

        FramePerSec.tick(FPS)

    spriteData.removeAllSprites()






# while True:
#     menus.endMenu(displaysurface, FramePerSec, FPS)