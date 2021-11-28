from types import FrameType
import pygame
import time
import random
import time
import os



frameRate = 60
windowSize = [1200,600]

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

pygame.init()
tileset = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/tileset.png')
# background = pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/preview.png')
background = tileset.subsurface((112,33,64,31))
treeTop = tileset.subsurface((39,39,26,26))
leftLedge = tileset.subsurface((72,24,7,7))
regLedge = tileset.subsurface((80,24,7,7))
regLedgePole = tileset.subsurface((87,24,10,7))
rightLedge = tileset.subsurface((97,24,7,7))
bothLedge = tileset.subsurface((96,32,8,8))
treeTrunk = tileset.subsurface((66,48,4,16))
treeTruckBottom = tileset.subsurface((72,56,8,8))
ladder = tileset.subsurface((72,32,8,8))

game_window = pygame.display.set_mode(windowSize)
pygame.display.set_caption('2D Platformer')
fps = pygame.time.Clock()

def main():
    scale = 9
    windowPosition = [0,0]
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    windowPosition[0] -= 5
                if event.key == pygame.K_LEFT and dir != 1:
                    windowPosition[0] += 5
                if event.key == pygame.K_UP and dir != 4:
                    windowPosition[1] += 5
                if event.key == pygame.K_DOWN and dir != 3:
                    windowPosition[1] -= 5
        img = pygame.transform.scale(background, (70*scale,32*scale))
        game_window.fill(black)
        
        for i in range(0,4,1):
            game_window.blit(img, (i*scale*70+windowPosition[0], windowPosition[1]))
        
        # game_window.blit(treeTop,(0,0))
        pygame.display.flip()
        fps.tick(frameRate)

main()