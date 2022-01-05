import pygame
from pygame.locals import *
import os
import math
import spriteData

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
HEIGHT = 600
WIDTH = 1200
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
font = pygame.font.SysFont('Comic Sans MS', 30)


# Sprite Sheets
skelSheet = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/skeleton.png')
tileset = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/tileset.png')
items = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/items.png')

# Images from Sprite Sheet
skeleton = pygame.transform.scale(skelSheet.subsurface((4,25,11,14)), (imgScale*10, imgScale*14))
regLedge = pygame.transform.scale(tileset.subsurface((80,24,7,7)), (imgScale*7, imgScale*7))
background = pygame.transform.scale(tileset.subsurface((112,33,64,31)), (64*bgScale,31*bgScale))

skeletonWalking = []

for i in range(0,6):
    skeletonWalking.append(pygame.transform.scale(skelSheet.subsurface((3+(20*i),24,13,15)), (imgScale*13, imgScale*15)))




itemArray = [
    pygame.transform.scale(items.subsurface((16,16,16,16)), (itemScale*16, itemScale*16)),
    pygame.transform.scale(items.subsurface((32,16,16,16)), (itemScale*16, itemScale*16)), 
]


# Initalize Surface
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = skeletonWalking[0]
        self.rect = self.image.get_rect()
        self.rect.center = ((10,420))
        self.health = 100

        self.pos = vec((210, 200))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.index = 0
        self.inventory = None
        self.jumpAllowed = True

    def jump(self):
        if self.jumpAllowed:
            self.vel.y = -8
            self.health -= 0.07

    def update(self,newACC,shiftPress):
        # print("Health: ", self.health)
        self.health -= 0.01
        time = pygame.time.get_ticks()
        # Movements:
        self.acc = newACC
        if(newACC.x != 0 and time%10 == 0 and self.vel.y == 0):
            if(self.index < 5):
                self.index += 1;
            else:
                self.index = 0;
        if(newACC.x < 0):
            self.image = pygame.transform.flip(skeletonWalking[self.index], True, False)
        else:   
            self.image = skeletonWalking[self.index]

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        # Check Collisions
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.jumpAllowed = True
        else:
            self.jumpAllowed = False
        for i in hits:
            if i.id == 8 and self.vel.x > 0:
                self.pos.x = i.rect.left - 24;
            elif i.id == 10 and self.vel.x < 0:
                self.pos.x = i.rect.right +24
            elif i.id == 12 and self.vel.y < 0:
                self.pos.y = i.rect.bottom + 62
                self.vel.y = -self.vel.y/2
            elif (i.id == 11 or i.id ==13) and self.pos.y+60 <= i.rect.bottom:
                self.pos.y = i.rect.bottom + 62
                self.vel.y = -self.vel.y/2
            elif (i.id == 7 or i.id == 13) and self.vel.x < 0 and self.pos.x >= i.rect.right and self.pos.y-2 >= i.rect.top:
                self.pos.x = i.rect.right +24
            elif (i.id == 5 or i.id == 11) and self.vel.x > 0 and self.pos.x <= i.rect.left and self.pos.y-2 >= i.rect.top:
                self.pos.x = i.rect.left -24
            elif self.vel.y > 0 and ((i.id >= 5 and i.id <= 7) or i.id <=4):
                self.health -= math.floor(self.vel.y)/20
                self.pos.y = i.rect.top + 1;
                self.vel.y = 0


        # Check item collision 
        collect = pygame.sprite.spritecollide(self, itemGroup, False)
        for it in collect:
            if self.inventory == None:
                self.inventory = it
            else:
                self.inventory.transform(self)
                
        if self.rect.colliderect(theChest.rect):
            if(self.rect.left > theChest.rect.left and self.vel.x < 0):
                self.pos.x = theChest.rect.right+24
            elif(self.rect.right < theChest.rect.right and self.vel.x > 0):
                self.pos.x = theChest.rect.left-24
            if self.inventory != None:
                itemsToGet[self.inventory.id] -= 1
                itemGroup.remove(self.inventory)
                all_sprites.remove(self.inventory)
                self.inventory = None
                        

        # print(itemsToGet)
        # Update Position
        self.rect.midbottom = self.pos 

class ProgressBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/ProgressBar.png'), (225, 47))
        self.rect = self.image.get_rect()
        self.rect.center = 1050,50


class itemIndicator(pygame.sprite.Sprite):
    def __init__(self,img,num):
        super().__init__()
        self.image = pygame.transform.scale(itemArray[img],(itemScale*11, itemScale*11))
        self.rect = self.image.get_rect()
        
        self.rect.center = (50+(num*100),30)

# Make Sprite Groups
P1 = Player()

platforms = spriteData.getPlatforms()
itemGroup = spriteData.getItems()

healthBar = ProgressBar()
theChest = spriteData.getChestSprite()

all_sprites = pygame.sprite.Group()
# all_sprites.add(PT1)
all_sprites.add(P1)
all_sprites.add(theChest)
all_sprites.add(healthBar)
all_sprites.add(platforms)
all_sprites.add(itemGroup)


# Item Indicator Formation: 
i = 0
for j in range(0,len(itemsToGet)):
    if itemsToGet[j] != 0:
        all_sprites.add(itemIndicator(j,i))
        i += 1


while True:
    accel = vec(0,0.5)
    jump = False
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
                jump == True
                P1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                moveRight = False
                moveLeft = False

    
    if moveRight == True:
        accel.x = ACC
    elif moveLeft == True:
        accel.x = -ACC
    
    # print(pygame.time.get_ticks())
    P1.update(accel,jump)

    displaysurface.fill(black)



    # Blit Background
    pygame.draw.rect(displaysurface, darkPurple, (0,0,WIDTH,75), 0)
    for i in range(0,4,1):
        displaysurface.blit(background, (i*bgScale*64, 75))

    #Draw Health Bar
    pygame.draw.rect(displaysurface, red, (healthBar.rect.left+60, healthBar.rect.top+25,157*(P1.health/100),15))
        
    all_sprites.draw(displaysurface)

 
    pygame.display.update()
    FramePerSec.tick(FPS)