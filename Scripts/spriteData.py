import pygame
from pygame.locals import *
import os
import math

platforms = pygame.sprite.Group()
itemGroup = pygame.sprite.Group()

itemsToGet = [0,0]

vec = pygame.math.Vector2  # 2 for two dimensional

imgScale = 4
itemScale = 3

# Sprite Sheets
skelSheet = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/skeleton.png')
tileset = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/tileset.png')
items = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/items.png')

# Ledge Type Order: Left Ledge, Reg Ledge, Reg Ledge Pole, Right Ledge, Both Ledge
ledgeTypes = [pygame.transform.scale(tileset.subsurface((72,24,8,8)), (imgScale*8, imgScale*8)), 
pygame.transform.scale(tileset.subsurface((80,24,8,8)), (imgScale*8, imgScale*8)), 
pygame.transform.scale(tileset.subsurface((88,24,8,8)), (imgScale*8, imgScale*8)),
pygame.transform.scale(tileset.subsurface((96,24,8,8)), (imgScale*8, imgScale*8)),
pygame.transform.scale(tileset.subsurface((96,32,8,8)), (imgScale*8, imgScale*8)),  # Both Ledge (4)
pygame.transform.scale(tileset.subsurface((8,8,8,8)), (imgScale*8, imgScale*8)),  #grass_TL (5)
pygame.transform.scale(tileset.subsurface((16,8,8,8)), (imgScale*8, imgScale*8)),  # grass_TC (6)
pygame.transform.scale(tileset.subsurface((24,8,8,8)), (imgScale*8, imgScale*8)),  #grass_TR (7)
pygame.transform.scale(tileset.subsurface((8,16,8,8)), (imgScale*8, imgScale*8)),  #grass_ML (8)
pygame.transform.scale(tileset.subsurface((16,16,8,8)), (imgScale*8, imgScale*8)),   #grass_MC (9)
pygame.transform.scale(tileset.subsurface((24,16,8,8)), (imgScale*8, imgScale*8)),   #grass_MR (10)
pygame.transform.scale(tileset.subsurface((8,24,8,8)), (imgScale*8, imgScale*8)),   #grass_BL (11)
pygame.transform.scale(tileset.subsurface((16,24,8,8)), (imgScale*8, imgScale*8)),    #grass_BC (12)
pygame.transform.scale(tileset.subsurface((24,24,8,8)), (imgScale*8, imgScale*8)),    #grass_BR (13)
pygame.transform.scale(tileset.subsurface((8,32,8,8)), (imgScale*8, imgScale*8)),    #Corner_BR (14)
pygame.transform.scale(tileset.subsurface((16,32,8,8)), (imgScale*8, imgScale*8)),    #Corner_BL (15)
pygame.transform.scale(tileset.subsurface((8,40,8,8)), (imgScale*8, imgScale*8)),    #Corner TR  (16)
pygame.transform.scale(tileset.subsurface((16,40,8,8)), (imgScale*8, imgScale*8)),   #Corner_TL  (17)
   
]

itemArray = [
    pygame.transform.scale(items.subsurface((16,16,16,16)), (itemScale*16, itemScale*16)),
    pygame.transform.scale(items.subsurface((32,16,16,16)), (itemScale*16, itemScale*16)), 
]

class chest(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/chest.png'), (60,64))
        self.rect = self.image.get_rect()
        self.rect.center = (40,280)


class platform(pygame.sprite.Sprite):
    def __init__(self,img,pos):
        super().__init__()
        size = vec(8*imgScale, 8*imgScale)
        self.image = ledgeTypes[img]
        self.id = img
        self.rect = self.image.get_rect()
        self.rect.center = (pos.x + (size.x/2), pos.y + (size.y/2))


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

def getChestSprite():
    return chest()

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
        else:
            for i in range(0,3):
                plat[i] = (int)(plat[i])
            PT1 = platform(plat[0], vec(plat[1],plat[2]))
            platforms.add(PT1)

def getPlatforms():
    processPlatformsItems()
    return platforms

def getItems():
    return itemGroup