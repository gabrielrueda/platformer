import pygame
import os


black = pygame.Color(0, 0, 0)


bg = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/startMenu.png'), (1216,608))
bg2 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/levelSelector/levelSBG.png'), (1216,608))

button = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/startUnchecked.png'), (315,72))
button2 = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/startChecked.png'), (315,72))

levelOne = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/levelSelector/levelOne.png'), (154,154))
levelOneD = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/levelSelector/levelOneD.png'), (154,154))

levelTwo = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/levelSelector/levelTwo.png'), (154,154))
levelTwoD = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/levelSelector/levelTwoD.png'), (154,154))

levelThree = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/levelSelector/levelThree.png'), (154,154))
levelThreeD = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/levelSelector/levelThreeD.png'), (154,154))

levelFour = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/levelSelector/levelFour.png'), (154,154))
levelFourD = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/levelSelector/levelFourD.png'), (154,154))

levelFive = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/levelSelector/levelFive.png'), (154,154))
levelFiveD = pygame.transform.scale(pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/levelSelector/levelFiveD.png'), (154,154))





helpScreenIMG = [
    pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/story1.png'),
    pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/story2.png'),
    pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/help1.png'),
    pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/help2.png'),
    pygame.image.load(os.path.dirname(os.getcwd()) + '/platformer/Assets/helpBG.png')
]



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
    clicked = False
    displaysurface.fill(black)
    displaysurface.blit(bg2, (0,0))
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
    
    # Level One Check:
    
    if (mouse[0] >= 143 and mouse[0] <= 297 and mouse[1] >= 150 and mouse[1] <= 304):
        if(clicked):
            return True
        else:
            displaysurface.blit(levelOne, (143,150))
    else:
        displaysurface.blit(levelOneD, (143,150))


    displaysurface.blit(levelTwoD, (337,150))
    displaysurface.blit(levelThreeD, (531,150))
    displaysurface.blit(levelFourD, (725,150))
    displaysurface.blit(levelFiveD, (919,150))



    pygame.display.update()
    FramePerSec.tick(FPS)
    return False

 
helpIndex = 0

def helpScreen(displaysurface,FramePerSec, FPS):
    global helpIndex
    clicked = False
    displaysurface.fill(black)
    
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                helpIndex += 1
                if helpIndex == 4:
                    return True


    
    displaysurface.blit(helpScreenIMG[4], (0,0))
    displaysurface.blit(helpScreenIMG[helpIndex], (0,0))


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

    