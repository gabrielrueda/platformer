import pygame
from pygame.locals import *
import os
import math
import spriteData

vec = pygame.math.Vector2  # 2 for two dimensional

skelSheet = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/skeleton.png')

HEIGHT = 600
WIDTH = 1200
ACC = 0.4
FRIC = -0.2
FPS = 60
imgScale = 4



skeletonWalking = []

for i in range(0,6):
    skeletonWalking.append(pygame.transform.scale(skelSheet.subsurface((3+(20*i),24,13,15)), (imgScale*13, imgScale*15)))



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

def getPlayer():
    return Player()