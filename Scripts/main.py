import pygame
from pygame.locals import *
import os
import math
import spriteData
import startMenu

# NOTE: The level data file format is...
#       ledgeType, pos x, pos y, size x, size y
 
pygame.init()
pygame.font.init() 
vec = pygame.math.Vector2  # 2 for two dimensional

#Colours
black = pygame.Color(0, 0, 0)
darkPurple = pygame.Color(19,12,55)
red = pygame.Color(254, 0, 3)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
# empty = pygame.Color(255,255,255,0)

# Global Constants
HEIGHT = 608
WIDTH = 1216
ACC = 0.4
FRIC = -0.2
FPS = 60

# Global Variables
moveRight = False
moveLeft = False
imgScale = 4
itemScale = 3
bgScale = 8
FramePerSec = pygame.time.Clock()

itemsToGet = [0,0]

#Font Variables
# font = pygame.font.Font(os.path.dirname(os.getcwd()) + '/platformer/Assets/arial.ttf', 16)
font = pygame.font.SysFont('Comic Sans MS', 20)


# Sprite Sheets
skelSheet = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/skeleton.png')
tileset = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/tileset.png')
items = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/items.png')

# Images from Sprite Sheet
skeleton = pygame.transform.scale(skelSheet.subsurface((4,25,11,14)), (imgScale*10, imgScale*14))
regLedge = pygame.transform.scale(tileset.subsurface((80,24,7,7)), (imgScale*7, imgScale*7))
background = pygame.transform.scale(tileset.subsurface((112,33,64,31)), (64*bgScale,31*bgScale))
bg2 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/bg.png'),(WIDTH,HEIGHT))



itemArray = [
    pygame.transform.scale(items.subsurface((16,16,16,16)), (itemScale*16, itemScale*16)),
    pygame.transform.scale(items.subsurface((32,16,16,16)), (itemScale*16, itemScale*16)), 
]


# Initalize Surface
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

while startMenu.update(displaysurface,FramePerSec,FPS) == False:
    pass




spriteData.initSprites()

def addText():
    i = 0
    for it in spriteData.indicatorGroup:
        txt = font.render((str(spriteData.itemsToGet[it.imgNum])+ "/" + str(it.amount)),False,green)
        displaysurface.blit(txt, (it.rect.left+40,it.rect.top+4))
        i += 1

count = 0

while True:
    accel = vec(0,0.5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                moveRight = True
                moveLeft = False
            if event.key == pygame.K_LEFT:
                moveLeft = True
                moveRight = False
            if event.key == pygame.K_SPACE:
                spriteData.playerSprite.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                moveRight = False
                moveLeft = False

    count += 1
    
    if moveRight == True:
        accel.x = ACC
    elif moveLeft == True:
        accel.x = -ACC

    # print(count)
    if count %5 == 0:
        spriteData.playerSprite.animate(moveLeft, moveRight)
        for i in spriteData.humanSprite:
            i.animate()
    
    # print(pygame.time.get_ticks())
    spriteData.playerSprite.update(accel)

    displaysurface.fill(black)

    for human in spriteData.humanSprite:
        human.update()


    # Blit Background
    pygame.draw.rect(displaysurface, darkPurple, (0,0,WIDTH,75), 0)
    for i in range(0,4,1):
        displaysurface.blit(background, (i*bgScale*64, 75))

    
    displaysurface.blit(bg2, (0, 0))

    #Draw Health Bar
    pygame.draw.rect(displaysurface, red, (spriteData.healthBar.rect.left+60, spriteData.healthBar.rect.top+25,157*(spriteData.playerSprite.health/100),15))
    


    # pygame.draw.lines(displaysurface,red, True, [(50,100), (100,50), (150,100)])
    for spear in spriteData.spearGroup:
        spear.update()
    
    spriteData.all_sprites.draw(displaysurface)

    addText()
 
    pygame.display.update()
    FramePerSec.tick(FPS)