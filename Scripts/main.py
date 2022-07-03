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
red = pygame.Color(168, 32, 57)
green = pygame.Color(148, 255, 194)
blue = pygame.Color(0, 0, 255)
white = pygame.Color(200, 200, 200)
# empty = pygame.Color(255,255,255,0)

# Global Constants
HEIGHT = 896
WIDTH = 1536 
FRIC = -0.2
FPS = 60
ACC = 0.4


# Global Variables
# moveRight = False
# moveLeft = False
imgScale = 4
itemScale = 3
bgScale = 6
FramePerSec = pygame.time.Clock()

# Music
pygame.mixer.init()
pygame.mixer.music.load(('../Assets/sounds/gamemusic3.mp3'))


#Font Variables
font = pygame.font.Font(('../Assets/font2.TTF'), 16)
fontBIG = pygame.font.Font(('../Assets/font2.TTF'), 36)
# font = pygame.font.SysFont('Comic Sans MS', 16)
# fontBIG = pygame.font.SysFont('Comic Sans MS', 36)



# # Sprite Sheets
# skelSheet = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformerAssets/tilesets/skeleton.png')
# tileset = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformerAssets/tilesets/tileset.png')
# items = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformerAssets/tilesets/items.png')



# # Images from Sprite Sheet
# skeleton = pygame.transform.scale(skelSheet.subsurface((4,25,11,14)), (imgScale*10, imgScale*14))
# regLedge = pygame.transform.scale(tileset.subsurface((80,24,7,7)), (imgScale*7, imgScale*7))

# gameover = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformerAssets/gameover.png'), (700,90))

# background = pygame.transform.scale(tileset.subsurface((112,33,64,31)), (64*bgScale,31*bgScale))


# # Level 2 FIXES: Gets stuck in tunnel and make cliff less wide
# lvlOutline = [
#     pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformerAssets/level1Larger.png'),(WIDTH,HEIGHT)),
#     pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformerAssets/level2Larger.png'),(WIDTH,HEIGHT)), 
#      pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformerAssets/level3Larger.png'),(WIDTH,HEIGHT)), 
#       pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformerAssets/level4Larger.png'),(WIDTH,HEIGHT)), 
#        pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformerAssets/level5Larger.png'),(WIDTH,HEIGHT)), 
# ]



#Sprite Sheets
# skelSheet = pygame.image.load(os.path.dirname(os.getcwd()) + 'Assets/tilesets/skeleton.png')
tileset = pygame.image.load(('../Assets/tilesets/tileset.png'))
# items = pygame.image.load(('../Assets/tilesets/items.png')



# Images from Sprite Sheet
# skeleton = pygame.transform.scale(skelSheet.subsurface((4,25,11,14)), (imgScale*10, imgScale*14))
regLedge = pygame.transform.scale(tileset.subsurface((80,24,7,7)), (imgScale*7, imgScale*7))

gameover = pygame.transform.scale(pygame.image.load(('../Assets/gameover.png')), (700,90))

background = pygame.transform.scale(tileset.subsurface((112,33,64,31)), (64*bgScale,31*bgScale))


# Level 2 FIXES: Gets stuck in tunnel and make cliff less wide
lvlOutline = [
    pygame.transform.scale(pygame.image.load(('../Assets/level1Larger.png')),(WIDTH,HEIGHT)),
    pygame.transform.scale(pygame.image.load(('../Assets/level2Larger.png')),(WIDTH,HEIGHT)), 
    pygame.transform.scale(pygame.image.load(('../Assets/level3Larger.png')),(WIDTH,HEIGHT)), 
    pygame.transform.scale(pygame.image.load(('../Assets/level4Larger.png')),(WIDTH,HEIGHT)), 
    pygame.transform.scale(pygame.image.load(('../Assets/level5Larger.png')),(WIDTH,HEIGHT)), 
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

while(True):
    menus.resetHelp()
    spriteData.removeAllSprites()
    # Go Through Menus
    while menus.startPage(displaysurface,FramePerSec,FPS) == False:
        pass


    while menus.helpScreen(displaysurface,FramePerSec,FPS) == False:
        pass



    def addText():
        i = 0
        for it in spriteData.indicatorGroup:
            txt = font.render((str(spriteData.itemsToGet[it.imgNum])+ "/" + str(it.amount)),False, it.color)
            displaysurface.blit(txt, (it.rect.left+40,it.rect.top+4))
            i += 1




    score = 0

    for level in range(0,5):
        spriteData.initSprites(level)
        count = 0
        while True:
            # print(spriteData.playerSprite.health)
            # For Finding Position of Spots:
            # mouse = pygame.mouse.get_pos()
            # print("(" + str(mouse[0]) + ", " + str(mouse[1]) + ")")

            accel = vec(0,1.2) # Falling Speed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            count += 1




            # FOR MOVEMENT: LEFT, RIGHT & BOOST
            keys = pygame.key.get_pressed()

            if keys[K_c]:
                ACC = 1.2 # Running Speed
            else:
                ACC = 0.8 # Walking Speed

            if keys[K_x]:
                spriteData.playerSprite.jump()

            if keys[K_RIGHT]:
                accel.x = ACC
                if count %3 == 0:
                    spriteData.playerSprite.animate(2)
            elif keys[K_LEFT]:
                accel.x = -ACC
                if count %3 == 0:
                    spriteData.playerSprite.animate(0)
            else:
                if count %10 == 0:
                    spriteData.playerSprite.animate(1)



            if count%5 == 0:
                for human in spriteData.humanSprite:
                    human.animate()
                    human.update()
            else:
                for human in spriteData.humanSprite:
                    human.update()


            spriteData.playerSprite.update(accel, keys[K_z])



            displaysurface.fill(black)

            


            # Background is the mountatins and sky
            pygame.draw.rect(displaysurface, darkPurple, (0,0,WIDTH,125), 0)
            for i in range(0,5,1):
                displaysurface.blit(background, (i*bgScale*64, 125))


            # Level outline will show the trees, bushes, etc..
            displaysurface.blit(lvlOutline[level], (0, 0))

            if(count < 40):
                txt = fontBIG.render("LEVEL " + str(round(level+1)),False, white)
                displaysurface.blit(txt, (WIDTH/2-(txt.get_width()/2),100))
                
            
            #Draw Health Bar
            pygame.draw.rect(displaysurface, red, (spriteData.healthBar.rect.left+44, spriteData.healthBar.rect.top,44*4*(round(spriteData.playerSprite.health)/100),30))


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

        if spriteData.playerSprite.health <= 0:
            score += 0
            break
        score += spriteData.playerSprite.health*20
        spriteData.removeAllSprites()

    tryAgain = False;
    while tryAgain == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_r:
                    tryAgain = True
                
        txt = fontBIG.render("Score: " + str(round(score)),False, white)
        displaysurface.blit(txt, (638,200))

        txt = font.render("Press Q to quit",False, white)
        displaysurface.blit(txt, (700,270))
        txt = font.render("Press R to try again",False, white)
        displaysurface.blit(txt, (700,310))
        
        displaysurface.blit(gameover, (418,100))
        pygame.display.update()
        FramePerSec.tick(FPS)

    

