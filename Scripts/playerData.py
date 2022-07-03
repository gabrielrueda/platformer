import pygame
from pygame.locals import *
import os
import math
import spriteData
import random
import sys



vec = pygame.math.Vector2  # 2 for two dimensional

# archer = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/tilesets/Archer-Purple.png')


# wizard = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/tilesets/Mage-Red.png')

archer = pygame.image.load('../Assets/tilesets/Archer-Purple.png')


wizard = pygame.image.load('../Assets/tilesets/Mage-Red.png')


HEIGHT = 896
WIDTH = 1536
ACC = 0.45
FRIC = -0.2
FPS = 60
imgScale = 4
itemScale = 3


walkingPattern = [2,1,3,1]
idlePattern = [0,0,1,1]


shootArrow = [7,8,9,10,11]

skeletonWalking = []

wizardIdle = []


# for i in range(0,6):
#     skeletonWalking.append(pygame.transform.scale(skelSheet.subsurface((3+(20*i),24,13,15)), (imgScale*13, imgScale*15)))


for i in range(0,4):
    skeletonWalking.append(pygame.transform.scale(wizard.subsurface((9+(i*32),37,14,19)), (imgScale*14, imgScale*19)))

for i in range(0,4):
    wizardIdle.append(pygame.transform.scale(wizard.subsurface((9+(i*32),5,14,19)), (imgScale*14, imgScale*19)))


personWalking = []

for i in range(0,12):
    personWalking.append(pygame.transform.scale(archer.subsurface((9+(32*i),68,14,20)), (imgScale*14, imgScale*20)))
    

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__() 
        self.image = skeletonWalking[0]
        self.rect = self.image.get_rect()
        self.rect.center = ((x,y))
        self.health = 100

        self.pos = vec((x, y)) #180,100
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.index = 0
        self.inventory = None
        self.jumpAllowed = True
        self.facing = True # True means right, false means left
        self.onLadder = 0  # 0 for not, 1 for down, 2 for up

    def jump(self):
        if self.jumpAllowed:
            self.vel.y = -15
            self.health -= 0.15
    
    def removeHealth(self,amount):
        self.health -= amount
    
    def animate(self,type):

        if self.vel.y == 0:
            if(self.index < len(walkingPattern)-1):
                self.index += 1
            else:
                self.index = 0
        
        if type == 0:
            self.image = pygame.transform.flip(skeletonWalking[walkingPattern[self.index]], True, False)
        elif type == 2:
            self.image = skeletonWalking[walkingPattern[self.index]]
        else:
            if self.facing:
                self.image = wizardIdle[idlePattern[self.index]]
            else:
                self.image = pygame.transform.flip(wizardIdle[idlePattern[self.index]], True, False)
                

    def update(self,newACC, z_pressed):
        
        self.health -= 0.01
        # Movements:
        self.acc = newACC

        # fireCollion = pygame.sprite.spritecollide(self, spriteData.humanSprite, False)
        # if fireCollion:
        #     self.health -= 0.5

        originalRect = self.rect.copy()


        if z_pressed and self.onLadder == 0:
            self.rect.update(self.rect.left, self.rect.top+76, self.rect.width, 2)
            ladderCollide = pygame.sprite.spritecollide(self, spriteData.ladders, False)
            if ladderCollide:
                self.onLadder = 1
            else:
                self.rect.update(self.rect.left, self.rect.top-11, self.rect.width, 6)
                ladderCollide = pygame.sprite.spritecollide(self, spriteData.ladders, False)
                if ladderCollide:
                    self.onLadder = 2
                else:
                    self.onLadder = 0
        else:
            if self.onLadder == 1:
                self.rect.update(self.rect.left, self.rect.top+76, self.rect.width, 2)
                ladderCollide = pygame.sprite.spritecollide(self, spriteData.ladders, False)
                if ladderCollide:
                    self.acc.x = 0
                    self.vel.y = 6
                else:
                    self.onLadder = 0
            elif self.onLadder == 2:
                self.rect.update(originalRect)
                ladderCollide = pygame.sprite.spritecollide(self, spriteData.ladders, False)
                if ladderCollide:
                    self.acc.x = 0
                    self.vel.y = -8
                else:
                    self.onLadder = 0


        self.rect.update(originalRect)

        # self.pos += self.vel
         

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        dx = self.vel.x + 0.5*self.acc.x
        dy = self.vel.y + 0.5*self.acc.y

        # print(str(self.rect) + " VS " + str(self.rect.inflate(20,20)))

        if self.pos.x+dx > WIDTH-self.rect.width or self.pos.x+dx < 0:
            dx = 0
    
        # New Collision Code
        self.jumpAllowed = False
        if self.onLadder == 0:
            for tile in spriteData.platforms:
                if tile.rect.colliderect(self.pos.x+dx,self.pos.y-1, 52,76):
                    dx = 0
                if tile.rect.colliderect(self.pos.x,self.pos.y+dy, 52,76):
                    self.jumpAllowed = True
                    #check if below the ground, hitting head
                    if self.vel.y < 0:
                        self.vel.y = 0
                        dy = tile.rect.bottom - self.rect.top
                    #check if above ground falling
                    elif self.vel.y >= 0:
                        self.vel.y = 0
                        dy = tile.rect.top - self.rect.bottom


            # Chest collision:
            # Side Collision
            chestSCollide = spriteData.chestSprite.rect.colliderect(self.pos.x+dx-5,self.pos.y-1, 62,76)
            if chestSCollide:
                dx = 0
                if self.inventory != None:
                    spriteData.itemsToGet[self.inventory.id] -= 1
                    spriteData.itemGroup.remove(self.inventory)
                    spriteData.all_sprites.remove(self.inventory)
                    self.inventory = None
            
            spriteData.chestSprite.update(self.rect.centerx)
            # Top collision
            if spriteData.chestSprite.rect.colliderect(self.pos.x,self.pos.y+dy, 52,76):
                self.jumpAllowed = True
                self.vel.y = 0
                dy = spriteData.chestSprite.rect.top - self.rect.bottom

    
        if dx > 0:
            self.facing = True
        elif dx < 0:
            self.facing = False

        # Update Position:
        self.pos.x += dx
        self.pos.y += dy
        self.rect.topleft = self.pos 

        # Check item collision 
        if self.inventory == None:
            collect = pygame.sprite.spritecollide(self, spriteData.itemGroup, False)
            if collect:
                self.inventory = collect[0]
        else:
            self.inventory.transform(self)

class human(pygame.sprite.Sprite):
    def __init__(self,y,min,max):
        super().__init__()
        self.min = min
        self.max = max
        self.image = personWalking[0]
        self.rect = self.image.get_rect()
        self.rect.center = (((max-min)/2), y)
        self.pos = vec (((max+min)/2), y)
        self.vel = vec(1,0)
        self.index = 0
        self.animateArrow = False

    def animate(self):
        if(self.index < len(walkingPattern)-1):
            self.index += 1
        elif (random.randint(0, 1) == 1):
            self.index = 0
            self.animateArrow = True;
        else:
            self.index = 0

    def updateWithArrow(self):
        self.image = personWalking[shootArrow[self.index]] if self.vel.x >= 0 else pygame.transform.flip(personWalking[shootArrow[self.index]],True, False)

        if self.index == 3:
            self.index = 0
            self.animateArrow = False
            spriteData.createSpear(self.pos.x, self.pos.y,self.vel.x)

    def update(self):    
        if self.animateArrow == True:
            self.updateWithArrow()
        else:
            if(self.vel.x > 0):
                self.image = personWalking[walkingPattern[self.index]]
                if(self.pos.x >= self.max):
                    self.vel.x = -self.vel.x
            else:
                self.image = pygame.transform.flip(personWalking[walkingPattern[self.index]], True, False)
                if(self.pos.x <= self.min):
                    self.vel.x = -self.vel.x


            # print("Position: " + str(self.pos.x))
            self.pos += self.vel

            self.rect.midbottom = self.pos 




        
        
def getHuman(y,min,max):
    return human(y,min,max)

def getPlayer(x,y):
    return Player(x,y)
