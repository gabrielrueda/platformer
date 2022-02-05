import pygame
from pygame.locals import *
import os
import math
import spriteData

vec = pygame.math.Vector2  # 2 for two dimensional

skelSheet = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/skeleton.png')
fireSkelSheet = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/skeleton_flame.png')

HEIGHT = 600
WIDTH = 1200
ACC = 0.45
FRIC = -0.2
FPS = 60
imgScale = 4
itemScale = 3


walkingPattern = [0,1,0,2]
idlePattern = [0,0,2,2]



skeletonWalking = []

for i in range(0,6):
    skeletonWalking.append(pygame.transform.scale(skelSheet.subsurface((3+(20*i),24,13,15)), (imgScale*13, imgScale*15)))

personWalking = []

for i in range(0,6):
    personWalking.append(pygame.transform.scale(fireSkelSheet.subsurface((3+(20*i),24,13,15)), (imgScale*13, imgScale*15)))
    

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = skeletonWalking[0]
        self.rect = self.image.get_rect()
        self.rect.center = ((210,150))
        self.health = 100

        self.pos = vec((180, 100))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.index = 0
        self.inventory = None
        self.jumpAllowed = True
        self.facing = True # True means right, false means left

    def jump(self):
        if self.jumpAllowed:
            self.vel.y = -10
            self.health -= 0.07
    
    def removeHealth(self,amount):
        self.health -= amount
    
    def animate(self,type):
        if(self.index < len(walkingPattern)-1):
            self.index += 1
        else:
            self.index = 0
        
        if self.vel.y == 0:
            if type == 0:
                self.image = pygame.transform.flip(skeletonWalking[walkingPattern[self.index]], True, False)
            elif type == 2:
                self.image = skeletonWalking[walkingPattern[self.index]]
            else:
                if self.facing:
                    self.image = skeletonWalking[idlePattern[self.index]]
                else:
                    self.image = pygame.transform.flip(skeletonWalking[idlePattern[self.index]], True, False)
                

    def update(self,newACC):
        # print("Health: ", self.health)
        self.health -= 0.01
        time = pygame.time.get_ticks()
        # Movements:
        self.acc = newACC

        fireCollion = pygame.sprite.spritecollide(self, spriteData.humanSprite, False)
        if fireCollion:
            self.health -= 0.5

        ladderCollide = pygame.sprite.spritecollide(self, spriteData.ladders, False)
        if ladderCollide:
            self.vel.y = -4

        # self.pos += self.vel
         
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        dx = self.vel.x + 0.5*self.acc.x
        dy = self.vel.y + 0.5*self.acc.y


        # New Collision Code
        self.jumpAllowed = False
        if not ladderCollide:
            for tile in spriteData.platforms:
                if tile.rect.colliderect(self.pos.x+dx,self.pos.y-1, 52,60):
                    dx = 0
                if tile.rect.colliderect(self.pos.x,self.pos.y+dy, 52,60):
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
        if spriteData.chestSprite.rect.colliderect(self.pos.x+dx,self.pos.y-1, 52,60):
            dx = 0
            if self.inventory != None:
                spriteData.itemsToGet[self.inventory.id] -= 1
                spriteData.itemGroup.remove(self.inventory)
                spriteData.all_sprites.remove(self.inventory)
                self.inventory = None
        if spriteData.chestSprite.rect.colliderect(self.pos.x,self.pos.y+dy, 52,60):
            self.jumpAllowed = True
            self.vel.y = 0
            dy = spriteData.chestSprite.rect.top - self.rect.bottom

       

        # Check item collision 
        if self.inventory == None:
            collect = pygame.sprite.spritecollide(self, spriteData.itemGroup, False)
            if collect:
                self.inventory = collect[0]
        else:
            self.inventory.transform(self,self.acc)

        if dx > 0:
            self.facing = True
        elif dx < 0:
            self.facing = False

        # Update Position:
        self.pos.x += dx
        self.pos.y += dy
        self.rect.topleft = self.pos 

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

    def animate(self):
        if(self.index < len(walkingPattern)-1):
            self.index += 1
        else:
            spriteData.createSpear(self.pos.x, self.pos.y,self.vel.x)
            self.index = 0

    def update(self):
        time = pygame.time.get_ticks()
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

def getPlayer():
    return Player()
