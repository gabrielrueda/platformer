import pygame
import os

black = pygame.Color(0, 0, 0)


bg = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/startMenu.png'), (1216,608))
button = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/startUnchecked.png'), (315,72))
button2 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/startChecked.png'), (315,72))

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
    