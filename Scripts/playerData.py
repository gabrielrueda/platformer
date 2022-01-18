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
                self.image = skeletonWalking[idlePattern[self.index]]

    def update(self,newACC):
        # print("Health: ", self.health)
        self.health -= 0.01
        time = pygame.time.get_ticks()
        # Movements:
        self.acc = newACC

        fireCollion = pygame.sprite.spritecollide(self, spriteData.humanSprite, False)
        if fireCollion:
            self.health -= 0.5

       
        # self.pos += self.vel
         
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        # Old Collision Code
        # hits = pygame.sprite.spritecollide(self, spriteData.platforms, False)
        # if hits:
        #     # print(hits[0].id)
        #     self.jumpAllowed = True
        #     for i in hits:
        #         # Left Collisions
        #         if (i.id == 24 or i.id == 47 or i.id == 70) and self.pos.x+21 <= i.rect.left and self.vel.x > 0 and self.pos.y != i.rect.top+1:
        #             self.pos.x = i.rect.left -24
        #         # Right Collisions
        #         elif (i.id == 26 or i.id == 49 or i.id == 72) and self.pos.x-21 >= i.rect.right and self.vel.x < 0 and self.pos.y != i.rect.top+1.75:
        #             self.pos.x = i.rect.right +24
        #         # Bottom Collisions
        #         elif (i.id <= 72 and i.id >= 70) and self.vel.y < 0:
        #             self.pos.y = i.rect.bottom + 62
        #             self.vel.y = -self.vel.y/2
        #         #Top Collisions
        #         elif ((i.id <= 26 and i.id >= 24) or i.id >= 78) and self.vel.y > 0:
        #             self.pos.y = i.rect.top+1
        #             self.vel.y = 0
        #             self.health -= math.floor(self.vel.y)/20
        #         print("Player Y:" + str(self.pos.y) + ", Plat Y: " + str(i.rect.top))      
        # else:
        #     self.jumpAllowed = False

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        dx = self.vel.x + 0.5*self.acc.x
        dy = self.vel.y + 0.5*self.acc.y


        # New Collision Code
        for tile in spriteData.platforms:
            if tile.rect.colliderect(self.pos.x+dx,self.pos.y-1, 52,60):
                dx = 0
            if tile.rect.colliderect(self.pos.x,self.pos.y+dy, 52,60):
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

        self.pos.x += dx
        self.pos.y += dy
           

        # Check item collision 
            # print(self.pos.y <= i.rect.top+16)

        collect = pygame.sprite.spritecollide(self, spriteData.itemGroup, False)
        for it in collect:
            if self.inventory == None:
                self.inventory = it
            else:
                self.inventory.transform(self)
        

        # Old Chest Collision    
        # if self.rect.colliderect(theChest):
        #     if(self.rect.left > theChest.left and self.vel.x < 0):
        #         self.pos.x = theChest.right+24
        #     elif(self.rect.right < theChest.right and self.vel.x > 0):
        #         self.pos.x = theChest.left-24
        #     if self.inventory != None:
        #         spriteData.itemsToGet[self.inventory.id] -= 1
        #         spriteData.itemGroup.remove(self.inventory)
        #         spriteData.all_sprites.remove(self.inventory)
        #         self.inventory = None
        
        
        # print("Player Y:" + str(self.pos.y))
        # self.rect.midbottom = self.pos
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
