import pygame
from pygame.locals import *
import os

# NOTE: The level data file format is...
#       ledgeType, pos x, pos y, size x, size y
 
pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

# Global Constants
HEIGHT = 600
WIDTH = 1200
ACC = 0.5
FRIC = -0.12
FPS = 60

# Global Variables
moveRight = False
moveLeft = False
imgScale = 5 
FramePerSec = pygame.time.Clock()

# Sprite Sheets
skelSheet = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/skeleton.png')
tileset = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/tileset.png')


# Images from Sprite Sheet
skeleton = pygame.transform.scale(skelSheet.subsurface((5,25,10,14)), (imgScale*10, imgScale*14))
regLedge = pygame.transform.scale(tileset.subsurface((80,24,7,7)), (imgScale*7, imgScale*7))


# Ledge Type Order: Left Ledge, Reg Ledge, Reg Ledge Pole, Right Ledge, Both Ledge
ledgeTypes = [pygame.transform.scale(tileset.subsurface((72,24,7,7)), (imgScale*7, imgScale*7)), 
pygame.transform.scale(tileset.subsurface((80,24,7,7)), (imgScale*7, imgScale*7)), 
pygame.transform.scale(tileset.subsurface((87,24,10,7)), (imgScale*10, imgScale*7))]


# Initalize Surface
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.Surface((imgScale*10, imgScale*14))
        self.surf.blit(skeleton, (0,0))
        self.rect = self.surf.get_rect(center = (10, 420))

        self.pos = vec((10, 385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def jump(self):
        self.vel.y = -12

    def update(self,newACC):
        # Movements:
        self.acc = newACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        # Check Collisions
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:
            if hits:
                self.pos.y = hits[0].rect.top + 1;
                self.vel.y = 0  
        
        # Update Position
        self.rect.midbottom = self.pos 

 
class platform(pygame.sprite.Sprite):
    def __init__(self,img,pos,size):
        super().__init__()
        size = vec(size.x*imgScale, size.y*imgScale)
        self.surf = pygame.Surface(size)
        self.surf.blit(img, (0,0))
        self.rect = self.surf.get_rect(center = (pos.x + (size.x/2), pos.y + (size.y/2)))

# Make Sprite Groups
P1 = Player()

platforms = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
# all_sprites.add(PT1)
all_sprites.add(P1)
# all_sprites.add(PT2)


# Platform Formation
file = open(os.getcwd() + '/Data/lvl1.txt', 'r')
contents = file.readlines()
for line in contents:
    plat = line.split(',')
    for i in range(0,5):
        plat[i] = (int)(plat[i])
    PT1 = platform(ledgeTypes[plat[0]], vec(plat[1],plat[2]), vec(plat[3],plat[4]))
    platforms.add(PT1)
    all_sprites.add(PT1)

while True:
    accel = vec(0,0.5)
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
                print("JUMP")
                P1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                moveRight = False
                moveLeft = False

    
    if moveRight == True:
        accel.x = ACC
    elif moveLeft == True:
        accel.x = -ACC
    
    P1.update(accel)

    

            
     
    displaysurface.fill((0,0,0))
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
 
    pygame.display.update()
    FramePerSec.tick(FPS)