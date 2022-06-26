import pygame
from pygame.locals import *
import os
import math
import playerData
import random



itemsToGet = [0,0,0,0,0]

vec = pygame.math.Vector2  # 2 for two dimensional

imgScale = 4
itemScale = 3
itemScale2 = 3
itemScaleTemp = 2
FRIC = -0.2


# Sprite Sheets
skelSheet = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/tilesets/skeleton.png')
tileset = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/tilesets/tileset.png')
items = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/tilesets/items.png')

chests = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/tilesets/chest.png')

items3 = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/tilesets/item3.png')

ledgeId = [78,79,80,81,104,24,25,26,47,49,70,71,72]



# itemArray = [
#     pygame.transform.scale(items.subsurface((16,16,16,16)), (itemScale2*16, itemScale2*16)),
#     pygame.transform.scale(items.subsurface((32,16,16,16)), (itemScale2*16, itemScale2*16)),
#     pygame.transform.scale(items.subsurface((16,32,16,16)), (itemScale2*16, itemScale2*16)), 
#     pygame.transform.scale(items.subsurface((48,16,16,16)), (itemScale2*16, itemScale2*16)), 
#     pygame.transform.scale(items.subsurface((16,64,16,16)), (itemScale2*16, itemScale2*16)), 
# ]


itemArray = [
    pygame.transform.scale(items3.subsurface((0,0,8,8)), (itemScaleTemp*16, itemScaleTemp*16)),
    pygame.transform.scale(items3.subsurface((0,16,8,8)), (itemScaleTemp*16, itemScaleTemp*16)),
    pygame.transform.scale(items3.subsurface((0,32,8,8)), (itemScaleTemp*16, itemScaleTemp*16)), 
    pygame.transform.scale(items3.subsurface((0,40,8,8)), (itemScaleTemp*16, itemScaleTemp*16)), 
    pygame.transform.scale(items3.subsurface((0,56,8,8)), (itemScaleTemp*16, itemScaleTemp*16)), 
    pygame.transform.scale(items3.subsurface((0,72,8,8)), (itemScaleTemp*16, itemScaleTemp*16)), 

]

chestArray = [
    pygame.transform.scale(chests.subsurface((97,46,14,18)), (14*4,18*4)),
    pygame.transform.scale(chests.subsurface((113,46,14,18)), (14*4,18*4)),
    pygame.transform.scale(chests.subsurface((129,46,14,18)), (14*4,18*4)),
    pygame.transform.scale(chests.subsurface((145,46,14,18)), (14*4,18*4)),
    pygame.transform.scale(chests.subsurface((161,46,14,18)), (14*4,18*4)),
    pygame.transform.scale(chests.subsurface((177,46,14,18)), (14*4,18*4))

]

class chest(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = chestArray[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.index = 0;
    
    def update(self,playerX):
        diff = abs(self.rect.centerx-playerX)
        if diff < 70 and self.index != 5:
            self.index += 1
            self.image = chestArray[self.index]
        elif diff > 70 and self.index != 0:
            self.index -= 1
            self.image = chestArray[self.index]


            


class platform(pygame.sprite.Sprite):
    def __init__(self,pos,tile):
        super().__init__()
        self.image = pygame.transform.scale(tileset.subsurface(((tile%23)*8, (math.floor(tile/23)*8),8,8)), (imgScale*8, imgScale*8))
        self.id = tile
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos.x, pos.y)


class anItem(pygame.sprite.Sprite):
    def __init__(self, img, pos):
        super().__init__()
        self.id = img
        self.image = itemArray[img]
        self.rect = self.image.get_rect()
        self.rect.center = (pos.x + 8, pos.y + 8)

        self.dx = 0
        self.dy = 0
        self.pos = vec(pos.x+8,pos.y+8)
        self.speed = 10
        

    def transform(self,P1):
        self.image = pygame.transform.scale(self.image, (itemScale*8, itemScale*8))
        if P1.facing:
            dirvect = pygame.math.Vector2(P1.rect.x - 30 - self.rect.x, P1.rect.y - 10 - self.rect.y)
        else:
            dirvect = pygame.math.Vector2(P1.rect.x + 56 - self.rect.x, P1.rect.y - 10 - self.rect.y)

        dist = dirvect.length()
        if(dist > 10):
            dirvect.normalize()
            dirvect.scale_to_length(self.speed * (dist/30))
            self.rect.move_ip(dirvect)
    
    # def toChest(self,chest):




class ProgressBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/newProgressBar2.png'), (56*4, 9*4))
        self.rect = self.image.get_rect()
        self.rect.center = 1370,28


class itemIndicator(pygame.sprite.Sprite):
    def __init__(self,img,num,amount):
        super().__init__()
        self.image = pygame.transform.scale(itemArray[img],(itemScale*11, itemScale*11))
        self.rect = self.image.get_rect()
        pixel = pygame.PixelArray(self.image)
        self.amount = amount
        self.imgNum = img
        self.rect.center = (50+(num*100),30)
        self.color = self.image.unmap_rgb(pixel[(16,18)])


platforms = pygame.sprite.Group()
ladders = pygame.sprite.Group()
itemGroup = pygame.sprite.Group()
healthBar = ProgressBar()
all_sprites = pygame.sprite.Group()


indicatorGroup = pygame.sprite.Group()
humanSprite = pygame.sprite.Group()
spearGroup = pygame.sprite.Group()

def processPlatformsItems(level):
    global chestSprite, playerSprite

    file = open(os.getcwd() + '/Data/lvlData.txt', 'r')
    contents = file.readlines()
    for line in contents:
        temp = line.split(',')
        id = temp[0]
        plat = list(map(int, temp[1:len(temp)]))
        if plat[0] == level:
            if id == 'i':
                it1 = anItem(plat[1], vec (plat[2], plat[3]))
                itemsToGet[plat[1]] += 1
                itemGroup.add(it1)
            elif id == 'h':
                t = playerData.getHuman(plat[1], plat[2],plat[3])
                humanSprite.add(t)
            elif id == 'c':
                chestSprite = chest(plat[1],plat[2])
            elif id == 'p':
                playerSprite = playerData.getPlayer(plat[1], plat[2])



floors = ['/Data/lvl1Big.csv','/Data/lvl2Big.csv','/Data/lvl3Big.csv','/Data/lvl4Big.csv','/Data/lvl5Big.csv']

def proPlats(level):
    file = open(os.getcwd() + floors[level], 'r')
    contents = file.readlines()
    x = 0
    y= 0
    for line in contents:
        row = line.split(',')
        for tileStr in row:
            tile = (int)(tileStr)
            # for i in range(0, len(ledgeId)):
            if(tile == 101):
                lad = platform(vec(x,y), tile)
                ladders.add(lad)
            elif(tile != -1):
                PT1 = platform(vec(x,y), tile)
                platforms.add(PT1)
            x += 32
        x = 0
        y += 32

                    
        



#SpriteList
def initSprites(level):
    processPlatformsItems(level)
    proPlats(level)

    # Item Indicator Formation: 
    i = 0
    for j in range(0,len(itemsToGet)):
        if itemsToGet[j] != 0:
            indicatorGroup.add(itemIndicator(j,j,itemsToGet[j]))
            i += 1
    
    all_sprites.add(indicatorGroup, 
        ladders, 
        playerSprite, 
        chestSprite, 
        healthBar, 
        platforms, 
        itemGroup, 
        humanSprite
    )

def removeAllSprites():
    for sprite in all_sprites.sprites():
        for group in sprite.groups():
            group.remove(sprite)


class spear(pygame.sprite.Sprite):
    def __init__(self,pos,dir):
        super().__init__()
        self.pos = vec(pos[0], pos[1]-23)
        if dir > 0:
            self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + "/platformer/Assets/arrow.png"), (itemScale*7, itemScale*7)),45)
        else:
            self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + "/platformer/Assets/arrow.png"), (itemScale*7, itemScale*7)),-135)

        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.vel = vec(30*dir,0)
        self.acc = vec(2*dir,0)

    def update(self):
        self.acc.x += self.vel.x * 0.001
        self.pos += self.vel 
        self.rect.center = self.pos
        collPlat = pygame.sprite.spritecollide(self, platforms, False)
        if collPlat and (collPlat[0].id > 81 or collPlat[0].id < 78):
            all_sprites.remove(self)
            spearGroup.remove(self)
        if self.rect.colliderect(playerSprite):
            playerSprite.removeHealth(2)
            all_sprites.remove(self)
            spearGroup.remove(self)




def createSpear(x,y,dir):
    newSpear = spear((x,y),dir)
    spearGroup.add(newSpear)
    all_sprites.add(newSpear)
