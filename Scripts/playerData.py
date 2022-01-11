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
    
    def removeHealth(self,amount):
        self.health -= amount

    def update(self,newACC,jump):
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

        fireCollion = pygame.sprite.spritecollide(self, spriteData.humanSprite, False)
        if fireCollion:
            self.health -= 0.5
            if(newACC.x < 0):
                self.image = pygame.transform.flip(personWalking[self.index], True, False)
            else:   
                self.image = personWalking[self.index]
        else:
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
        hits = pygame.sprite.spritecollide(self, spriteData.platforms, False)
        if hits:
            self.jumpAllowed = True
        else:
            self.jumpAllowed = False
        for i in hits:
            #For top right
            if i.id == 47 and self.vel.x > 0:
                self.pos.x = i.rect.left - 24
            #For middle right
            elif i.id == 49 and self.vel.x < 0:
                self.pos.x = i.rect.right +24
            # For bottom center
            elif i.id == 71 and self.vel.y < 0:
                self.pos.y = i.rect.bottom + 62
                self.vel.y = -self.vel.y/2
            # For bottom left and bottom right
            elif (i.id == 70 or i.id ==72) and self.pos.y+60 <= i.rect.bottom:
                self.pos.y = i.rect.bottom + 62
                self.vel.y = -self.vel.y/2
            #For top right and bottom right
            elif (i.id == 26 or i.id == 72) and self.vel.x < 0 and self.pos.x >= i.rect.right and self.pos.y-2 >= i.rect.top:
                self.pos.x = i.rect.right +24
            # For top left and bottom left
            elif (i.id == 24 or i.id == 70) and self.vel.x > 0 and self.pos.x <= i.rect.left and self.pos.y-2 >= i.rect.top:
                self.pos.x = i.rect.left -24
            elif self.vel.y > 0 and i.id != 47 and i.id != 48 and i.id != 49 and i.id != 70 and i.id != 71 and i.id != 72:
                self.health -= math.floor(self.vel.y)/20
                self.pos.y = i.rect.top + 1;
                self.vel.y = 0

            # print("Player Y:" + str(self.pos.y) + ", Plat Y: " + str(i.rect.top))
        # Check item collision 
        collect = pygame.sprite.spritecollide(self, spriteData.itemGroup, False)
        for it in collect:
            if self.inventory == None:
                self.inventory = it
            else:
                self.inventory.transform(self)
        
        theChest = spriteData.chestSprite.rect
                
        if self.rect.colliderect(theChest):
            if(self.rect.left > theChest.left and self.vel.x < 0):
                self.pos.x = theChest.right+24
            elif(self.rect.right < theChest.right and self.vel.x > 0):
                self.pos.x = theChest.left-24
            if self.inventory != None:
                spriteData.itemsToGet[self.inventory.id] -= 1
                spriteData.itemGroup.remove(self.inventory)
                spriteData.all_sprites.remove(self.inventory)
                self.inventory = None
        
        
         
        self.rect.midbottom = self.pos 

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

    def update(self):
        time = pygame.time.get_ticks()
        if(self.vel.x > 0):
            self.image = personWalking[self.index]
            if(self.pos.x >= self.max):
                self.vel.x = -self.vel.x
        else:
            self.image = pygame.transform.flip(personWalking[self.index], True, False)
            if(self.pos.x <= self.min):
                self.vel.x = -self.vel.x
        
        if(time % 7 == 0):
            if(self.index == 5):
                self.index = 0
                spriteData.createSpear(self.pos.x, self.pos.y,self.vel.x)
            else:
                self.index += 1
        
        
        print("Position: " + str(self.pos.x))
        self.pos += self.vel

        self.rect.midbottom = self.pos 




        
        
def getHuman(y,min,max):
    return human(y,min,max)

def getPlayer():
    return Player()
