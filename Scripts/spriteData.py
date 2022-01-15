import pygame
from pygame.locals import *
import os
import math
import playerData




itemsToGet = [0,0,0,0,0]

vec = pygame.math.Vector2  # 2 for two dimensional

imgScale = 4
itemScale = 3

# Sprite Sheets
skelSheet = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/skeleton.png')
tileset = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/tileset.png')
items = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/items.png')


ledgeId = [78,79,80,81,104,24,25,26,47,49,70,71,72]



itemArray = [
    pygame.transform.scale(items.subsurface((16,16,16,16)), (itemScale*16, itemScale*16)),
    pygame.transform.scale(items.subsurface((32,16,16,16)), (itemScale*16, itemScale*16)),
    pygame.transform.scale(items.subsurface((16,32,16,16)), (itemScale*16, itemScale*16)), 
    pygame.transform.scale(items.subsurface((48,16,16,16)), (itemScale*16, itemScale*16)), 
    pygame.transform.scale(items.subsurface((16,64,16,16)), (itemScale*16, itemScale*16)), 
]

class chest(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/chest.png'), (60,64))
        self.rect = self.image.get_rect()
        self.rect.center = (40,280)


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
    
    def transform(self, P1):
        self.image = pygame.transform.scale(self.image, (itemScale*8, itemScale*8))
        self.rect.center = (P1.rect.left + 40, P1.rect.top+55)

class ProgressBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/ProgressBar.png'), (225, 47))
        self.rect = self.image.get_rect()
        self.rect.center = 1050,50


class itemIndicator(pygame.sprite.Sprite):
    def __init__(self,img,num,amount):
        super().__init__()
        self.image = pygame.transform.scale(itemArray[img],(itemScale*11, itemScale*11))
        self.rect = self.image.get_rect()
        self.amount = amount
        self.imgNum = img
        self.rect.center = (50+(num*100),30)


platforms = pygame.sprite.Group()
itemGroup = pygame.sprite.Group()
chestSprite = chest()
healthBar = ProgressBar()
all_sprites = pygame.sprite.Group()
playerSprite = playerData.getPlayer()
indicatorGroup = pygame.sprite.Group()
humanSprite = pygame.sprite.Group()
spearGroup = pygame.sprite.Group()

def processPlatformsItems():
    file = open(os.getcwd() + '/Data/lvl1.txt', 'r')
    contents = file.readlines()
    for line in contents:
        plat = line.split(',')
        if plat[0] == 'i':
            for i in range(1,4):
                plat[i] = (int)(plat[i])
            it1 = anItem(plat[1], vec (plat[2], plat[3]))
            itemsToGet[plat[1]] += 1
            itemGroup.add(it1)
        elif plat[0] == 'h':
            for i in range(1,4):
                plat[i] = (int)(plat[i])
            t = playerData.getHuman(plat[1], plat[2],plat[3])
            humanSprite.add(t)


def proPlats():
    file = open(os.getcwd() + '/Data/lvl1Floor.csv', 'r')
    contents = file.readlines()
    x = 0
    y= 0
    for line in contents:
        row = line.split(',')
        for tileStr in row:
            tile = (int)(tileStr)
            # for i in range(0, len(ledgeId)):
            if(tile != -1):
                PT1 = platform(vec(x,y), tile)
                platforms.add(PT1)
            x += 32
        x = 0
        y += 32
    
    print("Count: " + str(len(platforms)))
                    
        



#SpriteList
def initSprites():
    processPlatformsItems()
    proPlats()
    # Item Indicator Formation: 
    i = 0
    for j in range(0,len(itemsToGet)):
        if itemsToGet[j] != 0:
            indicatorGroup.add(itemIndicator(j,i,itemsToGet[j]))
            i += 1
    all_sprites.add(indicatorGroup)
    all_sprites.add(playerSprite)
    all_sprites.add(chestSprite)
    all_sprites.add(healthBar)
    all_sprites.add(platforms)
    all_sprites.add(itemGroup)
    all_sprites.add(humanSprite)

class spear(pygame.sprite.Sprite):
    def __init__(self,pos,dir):
        super().__init__()
        self.pos = vec(pos[0], pos[1]-20)
        if dir > 0:
            self.image = pygame.transform.rotate(pygame.transform.scale(items.subsurface((32,128,16,16)), (itemScale*8, itemScale*8)),-45)
        else:
            self.image = pygame.transform.rotate(pygame.transform.scale(items.subsurface((32,128,16,16)), (itemScale*8, itemScale*8)),135)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.vel = vec(10*dir,0)
        self.acc = vec(-0.2*dir,0)

    def update(self):
        self.acc.x += self.vel.x * 0.001
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # self.image = pygame.transform.rotate( pygame.transform.scale(items.subsurface((32,128,16,16)), (itemScale*8, itemScale*8)), self.rotation)
        self.rect.center = self.pos
        collPlat = pygame.sprite.spritecollide(self, platforms, False)
        if collPlat:
            all_sprites.remove(self)
            spearGroup.remove(self)
        elif self.rect.colliderect(playerSprite):
            playerSprite.removeHealth(2)
            all_sprites.remove(self)
            spearGroup.remove(self)




def createSpear(x,y,dir):
    newSpear = spear((x,y),dir)
    spearGroup.add(newSpear)
    all_sprites.add(newSpear)
