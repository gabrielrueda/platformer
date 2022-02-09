import pygame
import os


black = pygame.Color(0, 0, 0)


bg = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/startMenu.png'), (1216,608))
button = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/startUnchecked.png'), (315,72))
button2 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/startChecked.png'), (315,72))

levelOne = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/levelOne.png'), (252,189))

gameover = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/gameover.png'), (700,90))

buttonPos = [623,465]

def update(displaysurface,FramePerSec,FPS):
    clicked = False
    toGame = False
    mouse = pygame.mouse.get_pos()
    displaysurface.fill(black)
    displaysurface.blit(bg, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True


    if mouse[0] >= buttonPos[0] and mouse[0] <= 938 and mouse[1] >= buttonPos[1] and mouse[1] <= 537:
        displaysurface.blit(button2, buttonPos)
        if clicked:
            toGame = True
    else:
        displaysurface.blit(button, buttonPos)


    pygame.display.update()
    FramePerSec.tick(FPS)
    return toGame

def levelSelector(displaysurface, FramePerSec, FPS):
    displaysurface.fill(black)
    displaysurface.blit(bg, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    displaysurface.blit(levelOne, (100,100))
    pygame.display.update()
    FramePerSec.tick(FPS)
    return False

def endMenu(displaysurface, FramePerSec, FPS):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    displaysurface.blit(gameover, (200,200))
    pygame.display.update()
    FramePerSec.tick(FPS)

def storyInstructions(displaysurface, font,FramePerSec, FPS):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    
    pygame.display.update()
    FramePerSec.tick(FPS)

    